import importlib.util
import os
import re
import json
from datetime import datetime
from urllib.parse import quote_plus
from typing import Optional, Tuple

import streamlit as st
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential
import pandas as pd


load_dotenv()


# ==================== CONSTANTS ====================
PLACEHOLDER_API_KEYS = {
    "",
    "your_gemini_api_key_here",
    "your_api_key_here",
    "replace_me",
}
READ_ONLY_PREFIXES = ("select", "with", "show", "describe", "desc", "explain")
BLOCKED_SQL_KEYWORDS = (
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "replace",
    "grant",
    "revoke",
)

EXAMPLE_QUESTIONS = [
    "📊 How many White Nike shirts are in stock?",
    "💰 What is the average price of Adidas shirts?",
    "🏷️ Show all discounts currently available",
    "⭐ Which brand has the highest total stock?",
    "🔍 List all Red shirts under $30",
    "📈 What's the total inventory value?",
    "👕 How many different sizes of Levi shirts do we have?",
]

BRANDS = ["Van Heusen", "Levi", "Nike", "Adidas"]
COLORS = ["Red", "Blue", "Black", "White"]
SIZES = ["XS", "S", "M", "L", "XL"]


# ==================== PAGE CONFIG ====================
def configure_page():
    st.set_page_config(
        page_title="Atliq Tees SQL Assistant",
        page_icon="👔",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        /* Main theme colors */
        :root {
            --primary-color: #FF6B6B;
            --secondary-color: #4ECDC4;
            --accent-color: #FFE66D;
            --dark-bg: #1A1A2E;
            --light-text: #FFFFFF;
        }
        
        /* Custom styling */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin: 10px 0;
        }
        
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.1rem;
            font-weight: 600;
        }
        
        .question-chip {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            margin: 5px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .question-chip:hover {
            transform: translateY(-2px);
        }
        
        .success-box {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
        }
        
        .info-box {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)


# ==================== SETTINGS & CONFIG ====================
def get_settings():
    return {
        "google_api_key": os.getenv("GOOGLE_API_KEY", "").strip(),
        "google_model": os.getenv("GOOGLE_MODEL", "gemini-1.5-flash").strip() or "gemini-1.5-flash",
        "db_user": os.getenv("DB_USER", "root").strip(),
        "db_password": os.getenv("DB_PASSWORD", "").strip(),
        "db_host": os.getenv("DB_HOST", "localhost").strip(),
        "db_port": os.getenv("DB_PORT", "3306").strip(),
        "db_name": os.getenv("DB_NAME", "atliq_tshirts").strip(),
    }


def has_real_api_key(api_key):
    return api_key.strip().lower() not in PLACEHOLDER_API_KEYS


def build_db_uri(settings):
    quoted_password = quote_plus(settings["db_password"])
    return (
        f"mysql+pymysql://{settings['db_user']}:{quoted_password}"
        f"@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"
    )


def driver_is_available():
    return importlib.util.find_spec("pymysql") is not None


def get_setup_issues(settings):
    issues = []

    if not has_real_api_key(settings["google_api_key"]):
        issues.append("🔑 Set a real GOOGLE_API_KEY in .env")

    for key in ("db_user", "db_host", "db_port", "db_name"):
        if not settings[key]:
            issues.append(f"⚙️ Set {key.upper()} in .env")

    if not driver_is_available():
        issues.append("📦 Install PyMySQL in the active virtual environment")

    return issues


# ==================== DATABASE & LLM ====================
@st.cache_resource(show_spinner=False)
def init_database(db_uri):
    return SQLDatabase.from_uri(db_uri)


@st.cache_resource(show_spinner=False)
def init_llm(model_name, api_key):
    return GoogleGenerativeAI(
        model=model_name,
        temperature=0,
        google_api_key=api_key,
    )


# ==================== QUERY PROCESSING ====================
def clean_sql_query(query):
    cleaned_query = query.strip()

    for prefix in (
        "SQLQuery:",
        "SQL Query:",
        "Query:",
        "SQL:",
        "sql:",
        "Here is the SQL query:",
        "The SQL query is:",
        "Answer:",
    ):
        if cleaned_query.startswith(prefix):
            cleaned_query = cleaned_query[len(prefix):].strip()

    if cleaned_query.startswith("```sql"):
        cleaned_query = cleaned_query[6:]
    elif cleaned_query.startswith("```"):
        cleaned_query = cleaned_query[3:]

    if cleaned_query.endswith("```"):
        cleaned_query = cleaned_query[:-3]

    cleaned_query = cleaned_query.strip().rstrip(";").strip()
    cleaned_query = re.sub(r"\s+", " ", cleaned_query)
    return cleaned_query


def validate_read_only_query(query):
    if not query:
        raise ValueError("The model did not return a query.")

    if ";" in query:
        raise ValueError("Only a single SQL statement is allowed.")

    lowered = query.lower().strip()
    if not lowered.startswith(READ_ONLY_PREFIXES):
        raise ValueError("Only read-only queries are allowed.")

    for keyword in BLOCKED_SQL_KEYWORDS:
        if re.search(rf"\b{keyword}\b", lowered):
            raise ValueError(f"Blocked unsafe SQL keyword: {keyword}")


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
def generate_sql_query(question, db, llm):
    table_info = db.get_table_info()

    prompt = PromptTemplate.from_template(
        """
You convert business questions into one safe, read-only MySQL query.

Available schema:
{table_info}

Rules:
- Return exactly one MySQL query and nothing else
- Only use SELECT, WITH, SHOW, DESCRIBE, DESC, or EXPLAIN
- Never use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, REPLACE, GRANT, or REVOKE
- Use only the tables and columns shown in the schema
- If the question cannot be answered from the schema, return:
  SELECT 'The available tables do not contain that information.' AS message
- Match enum values exactly when filtering brand, color, or size
- Do not wrap the answer in markdown

Question:
{question}

SQL:
"""
    )

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"table_info": table_info, "question": question})


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
def generate_response(question, sql_query, result, llm):
    prompt = PromptTemplate.from_template(
        """
You are a helpful retail data assistant for Atliq Tees.

User question:
{question}

SQL query:
{sql_query}

SQL result:
{result}

Write a concise, professional answer in plain English for a non-technical store user.
- If the result is empty, say that clearly
- If the result contains multiple rows, provide key insights and summary
- Make it actionable and business-focused
- Keep it under 150 words
"""
    )

    chain = prompt | llm | StrOutputParser()
    return chain.invoke(
        {
            "question": question,
            "sql_query": sql_query,
            "result": result,
        }
    ).strip()


# ==================== HISTORY MANAGEMENT ====================
def load_query_history():
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    return st.session_state.query_history


def add_to_history(question, sql_query, result, answer):
    history = load_query_history()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "sql": sql_query,
        "result": result,
        "answer": answer,
    })
    # Keep only last 20 queries
    if len(history) > 20:
        st.session_state.query_history = history[-20:]


def clear_history():
    st.session_state.query_history = []


# ==================== UI COMPONENTS ====================
def render_header():
    col1, col2 = st.columns([0.7, 0.3])
    
    with col1:
        st.title("👔 Atliq Tees Assistant")
        st.markdown(
            "**Ask questions in English. Get SQL results instantly.** "
            "Powered by Gemini AI"
        )
    
    with col2:
        st.markdown("### Quick Stats")
        if st.session_state.get("stats"):
            stats = st.session_state.stats
            col2a, col2b = st.columns(2)
            with col2a:
                st.metric("📊 Queries", stats.get("total_queries", 0))
            with col2b:
                st.metric("⚡ Success Rate", f"{stats.get('success_rate', 0):.0%}")


def render_sidebar(settings):
    with st.sidebar:
        st.header("⚙️ Connection Settings")
        
        with st.expander("Database Config", expanded=True):
            st.markdown(f"**Database:** `{settings['db_name']}`")
            st.markdown(f"**Host:** `{settings['db_host']}:{settings['db_port']}`")
            st.markdown(f"**User:** `{settings['db_user']}`")
            st.markdown(f"**Model:** `{settings['google_model']}`")
            
            driver_status = "✅ Installed" if driver_is_available() else "❌ Not Installed"
            st.markdown(f"**PyMySQL:** {driver_status}")
        
        st.divider()
        
        # Query History
        if st.button("🗑️ Clear Query History", key="clear_history_btn"):
            clear_history()
            st.toast("History cleared!")
        
        st.divider()
        
        # About
        with st.expander("ℹ️ About"):
            st.markdown("""
            **Atliq Tees SQL Assistant v2.0**
            
            Natural language to SQL converter for inventory management.
            
            - 🔒 Read-only queries only
            - 🚀 Real-time execution
            - 📊 Result visualization
            - 📜 Query history
            """)


def render_setup_help(settings, issues):
    st.warning("⚠️ Setup Incomplete")
    st.markdown("The app can load, but it cannot answer questions yet. Please fix:")
    
    for issue in issues:
        st.markdown(f"- {issue}")

    with st.expander("📝 Expected .env values"):
        env_content = """GOOGLE_API_KEY=your_real_gemini_api_key
GOOGLE_MODEL=gemini-1.5-flash
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=atliq_tshirts"""
        st.code(env_content, language="bash")
        
        st.info(
            "💡 **Tip:** Copy this to your `.env` file and fill in your actual credentials."
        )


def render_quick_filters(db):
    """Render quick filter buttons for common queries"""
    st.subheader("🎯 Quick Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Stock Overview", use_container_width=True):
            st.session_state.quick_query = "Show total stock quantity by brand"
    
    with col2:
        if st.button("💰 Price Range", use_container_width=True):
            st.session_state.quick_query = "What is the average price by size?"
    
    with col3:
        if st.button("🏷️ Discounts", use_container_width=True):
            st.session_state.quick_query = "Show all available discounts"
    
    with col4:
        if st.button("📈 Top Seller", use_container_width=True):
            st.session_state.quick_query = "Which brand has the most inventory?"


def render_example_questions():
    st.subheader("💡 Example Questions")
    
    cols = st.columns(2)
    for idx, question in enumerate(EXAMPLE_QUESTIONS):
        with cols[idx % 2]:
            if st.button(question, key=f"example_{idx}", use_container_width=True):
                st.session_state.selected_question = question.split(" ", 1)[1]


def render_query_history():
    st.subheader("📜 Query History")
    history = load_query_history()
    
    if not history:
        st.info("No queries yet. Try asking a question!")
        return
    
    with st.expander(f"View last {len(history)} queries", expanded=False):
        for idx, record in enumerate(reversed(history), 1):
            col1, col2 = st.columns([0.7, 0.3])
            
            with col1:
                st.markdown(f"**{idx}. {record['question'][:50]}...**")
                st.caption(f"⏰ {record['timestamp']}")
            
            with col2:
                if st.button("📋 View", key=f"history_{idx}", use_container_width=True):
                    st.session_state.selected_history = record


def render_results(question, sql_query, result, answer):
    """Render query results in tabs"""
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Answer", "🔍 SQL Query", "📊 Data", "💾 Export"])
    
    with tab1:
        st.success("✅ Query executed successfully!")
        st.markdown(f"### Answer\n{answer}")
    
    with tab2:
        st.code(sql_query, language="sql")
        st.caption("🔒 This is a read-only query")
    
    with tab3:
        try:
            # Try to parse and display as dataframe
            if isinstance(result, str):
                st.code(result)
            else:
                st.dataframe(result, use_container_width=True)
        except:
            st.code(str(result))
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download as CSV", use_container_width=True):
                try:
                    # Convert result to CSV
                    csv_data = pd.DataFrame([{"Result": str(result)}]).to_csv(index=False)
                    st.download_button(
                        "⬇️ Download CSV",
                        csv_data,
                        file_name=f"query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                except:
                    st.error("Could not generate CSV")
        
        with col2:
            if st.button("📋 Copy SQL", use_container_width=True):
                st.code(sql_query)
                st.toast("SQL copied!")


# ==================== ANALYTICS ====================
def render_analytics(db):
    """Show database analytics"""
    st.subheader("📊 Inventory Analytics")
    
    try:
        # Get basic stats
        brand_query = "SELECT brand, COUNT(*) as count, SUM(stock_quantity) as total_stock FROM t_shirts GROUP BY brand"
        brand_result = db.run(brand_query)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("📦 Total Inventory by Brand", icon="📊")
            st.code(brand_result)
        
        with col2:
            # Price range
            price_query = "SELECT MIN(price) as min_price, MAX(price) as max_price, AVG(price) as avg_price FROM t_shirts"
            price_result = db.run(price_query)
            st.info("💰 Price Statistics", icon="💵")
            st.code(price_result)
    except Exception as e:
        st.warning(f"Could not load analytics: {e}")


# ==================== MAIN APP ====================
def main():
    configure_page()
    
    # Initialize session state
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    if "stats" not in st.session_state:
        st.session_state.stats = {"total_queries": 0, "success_rate": 0}
    
    settings = get_settings()
    issues = get_setup_issues(settings)
    
    render_header()
    render_sidebar(settings)
    
    # Main content
    if issues:
        render_setup_help(settings, issues)
        return
    
    # Tabs for different sections
    tab_main, tab_analytics, tab_history = st.tabs(["🔍 Query Assistant", "📊 Analytics", "📜 History"])
    
    with tab_main:
        st.divider()
        
        # Quick filters
        render_quick_filters(None)
        
        st.divider()
        
        # Question input
        st.subheader("❓ Ask a Question")
        
        col1, col2 = st.columns([0.85, 0.15])
        
        with col1:
            question = st.text_input(
                "Enter your question",
                placeholder="How many White Nike shirts are in stock?",
                key="main_question_input"
            )
        
        with col2:
            ask_button = st.button("🚀 Ask", type="primary", use_container_width=True)
        
        st.divider()
        
        # Example questions
        render_example_questions()
        
        st.divider()
        
        # Process question
        if ask_button or st.session_state.get("selected_question"):
            final_question = st.session_state.get("selected_question") or question
            st.session_state.selected_question = None
            
            if not final_question.strip():
                st.warning("⚠️ Please enter a question before running the query.")
                return
            
            try:
                # Initialize database and LLM
                with st.spinner("🔗 Connecting to database..."):
                    db = init_database(build_db_uri(settings))
                
                with st.spinner("🤖 Initializing AI model..."):
                    llm = init_llm(settings["google_model"], settings["google_api_key"])
                
                # Generate SQL
                with st.spinner("✍️ Generating SQL query..."):
                    raw_sql = generate_sql_query(final_question, db, llm)
                
                sql_query = clean_sql_query(raw_sql)
                validate_read_only_query(sql_query)
                
                # Execute query
                with st.spinner("⚡ Executing query..."):
                    result = db.run(sql_query)
                
                # Generate response
                with st.spinner("📝 Writing answer..."):
                    answer = generate_response(final_question, sql_query, result, llm)
                
                # Add to history
                add_to_history(final_question, sql_query, result, answer)
                
                # Update stats
                st.session_state.stats["total_queries"] += 1
                st.session_state.stats["success_rate"] = 1.0
                
                st.divider()
                
                # Render results
                render_results(final_question, sql_query, result, answer)
                
            except Exception as exc:
                st.error(f"❌ Error: {str(exc)}")
                st.info(
                    "💡 **Tip:** Make sure your database is running and credentials are correct."
                )
    
    with tab_analytics:
        st.divider()
        try:
            db = init_database(build_db_uri(settings))
            render_analytics(db)
        except Exception as e:
            st.error(f"Could not load analytics: {e}")
    
    with tab_history:
        st.divider()
        render_query_history()


if __name__ == "__main__":
    main()
