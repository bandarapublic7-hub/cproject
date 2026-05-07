import importlib.util
import os
import re
from urllib.parse import quote_plus

import streamlit as st
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import GoogleGenerativeAI
from langchain_classic.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tenacity import retry, stop_after_attempt, wait_exponential


load_dotenv()


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
        issues.append("Set a real GOOGLE_API_KEY in .env.")

    for key in ("db_user", "db_host", "db_port", "db_name"):
        if not settings[key]:
            issues.append(f"Set {key.upper()} in .env.")

    if not driver_is_available():
        issues.append("Install PyMySQL in the active virtual environment.")

    return issues


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
You are a helpful retail data assistant.

User question:
{question}

SQL query:
{sql_query}

SQL result:
{result}

Write a concise answer in plain English for a non-technical store user.
If the result is empty, say that clearly.
If the result contains multiple rows, summarize the most important takeaways.
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


def render_setup_help(settings, issues):
    st.warning("Setup is incomplete. The app can load, but it cannot answer questions yet.")

    for issue in issues:
        st.write(f"- {issue}")

    with st.expander("Expected .env values", expanded=False):
        st.code(
            "\n".join(
                [
                    "GOOGLE_API_KEY=your_real_gemini_api_key",
                    f"GOOGLE_MODEL={settings['google_model']}",
                    f"DB_USER={settings['db_user'] or 'root'}",
                    "DB_PASSWORD=your_mysql_password",
                    f"DB_HOST={settings['db_host'] or 'localhost'}",
                    f"DB_PORT={settings['db_port'] or '3306'}",
                    f"DB_NAME={settings['db_name'] or 'atliq_tshirts'}",
                ]
            ),
            language="bash",
        )


def render_sidebar(settings):
    with st.sidebar:
        st.header("Connection")
        st.write(f"Database: `{settings['db_name']}`")
        st.write(f"Host: `{settings['db_host']}:{settings['db_port']}`")
        st.write(f"User: `{settings['db_user']}`")
        st.write(f"Model: `{settings['google_model']}`")
        st.write(f"PyMySQL installed: `{'yes' if driver_is_available() else 'no'}`")


def main():
    st.set_page_config(page_title="Atliq Tees SQL Assistant", page_icon="👕", layout="wide")

    settings = get_settings()
    issues = get_setup_issues(settings)

    st.title("Atliq Tees Natural Language to SQL Assistant")
    st.caption(
        "Ask retail questions in plain English. The app generates a safe read-only SQL query, "
        "runs it on MySQL, and explains the result in simple language."
    )

    render_sidebar(settings)

    if issues:
        render_setup_help(settings, issues)

    with st.expander("Example questions", expanded=False):
        st.write("- How many White Nike shirts are in stock?")
        st.write("- What is the average price of Adidas shirts?")
        st.write("- Show all discounts currently available.")
        st.write("- Which brand has the highest total stock?")

    question = st.text_input(
        "Ask a question about inventory or discounts",
        placeholder="How many White Nike shirts are in stock?",
    )
    ask_button = st.button("Ask", type="primary", disabled=bool(issues))

    if not ask_button:
        return

    if not question.strip():
        st.warning("Enter a question before running the query.")
        return

    try:
        db = init_database(build_db_uri(settings))
    except Exception as exc:
        st.error(f"Database connection failed: {exc}")
        return

    try:
        llm = init_llm(settings["google_model"], settings["google_api_key"])
    except Exception as exc:
        st.error(f"Model initialization failed: {exc}")
        return

    try:
        with st.spinner("Generating SQL query..."):
            raw_sql = generate_sql_query(question, db, llm)

        sql_query = clean_sql_query(raw_sql)
        validate_read_only_query(sql_query)

        with st.expander("Generated SQL", expanded=True):
            st.code(sql_query, language="sql")

        with st.spinner("Executing SQL query..."):
            result = db.run(sql_query)

        with st.expander("Raw database result", expanded=True):
            st.code(str(result))

        with st.spinner("Writing final answer..."):
            answer = generate_response(question, sql_query, result, llm)

        st.subheader("Answer")
        st.write(answer)
    except Exception as exc:
        st.error(f"Request failed: {exc}")


if __name__ == "__main__":
    main()
