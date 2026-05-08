# 👔 Atliq Tees — NL to SQL Assistant

Ask questions in plain English. Get instant answers from your inventory database — powered by Google Gemini AI.

![Version](https://img.shields.io/badge/version-v2.0%20stable-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![MySQL](https://img.shields.io/badge/MySQL-orange)
![Gemini](https://img.shields.io/badge/Google-Gemini%20AI-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![UI](https://img.shields.io/badge/UI-Streamlit-blue)

---

# ✨ Features

- 🔍 **Natural language queries**  
  Type questions in plain English — AI converts them to SQL automatically.

- 🛡️ **Read-only safety**  
  Only SELECT queries run. INSERT, DROP, DELETE are blocked by design.

- 📊 **Analytics dashboard**  
  Inventory stats, brand breakdowns, and price distribution at a glance.

- 📜 **Query history**  
  Track your last 20 queries with timestamps.

- 📥 **CSV export**  
  Download query results instantly.

- ⚡ **Smart caching**  
  Model and DB connections cached for faster responses.

---

# 🏗️ Architecture

```text
User
  ↓
Streamlit Web UI
  ↓
LangChain Orchestration
  ↔ Gemini AI
  ↓
MySQL Database
  ↓
Formatted Response + Data Table
```

---

# 🔄 Request Flow

```text
User Question
      ↓
LangChain Prompt Build
      ↓
Gemini Generates SQL
      ↓
Safety Validation
      ↓
Execute on MySQL
      ↓
Format & Respond
```

---

# 📁 Project Structure

```bash
atliq-tees-assistant/
│
├── main_enhanced.py
├── db_creation.sql
├── requirements.txt
├── .env.example
├── README.md
│
└── docs/
    ├── SETUP_GUIDE.md
    ├── FEATURES.md
    └── TROUBLESHOOTING.md
```

---

# 🚀 Quick Start

## 1. Clone the Repository

```bash
git clone <repository-url>
cd atliq-tees-assistant
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements_updated.txt
```

---

## 4. Setup MySQL Database

```bash
mysql -u root -p < db_creation_enhanced.sql
```

Creates `atliq_tshirts` database with sample records.

---

## 5. Configure Environment Variables

Copy:

```bash
.env.example
```

to:

```bash
.env
```

---

## 6. Run the App

```bash
streamlit run main_enhanced.py
```

Open:

```text
http://localhost:8501
```

---

# 🔐 Environment Variables

```env
# ===== Google AI =====
GOOGLE_API_KEY=AIzaSy_your_key_here
GOOGLE_MODEL=gemini-1.5-flash

# ===== MySQL =====
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=atliq_tshirts
```

---

# 💬 Example Questions

- How many White Nike shirts are in stock?
- What is the average price of Adidas shirts?
- Show all discounts currently available
- Which brand has the highest total stock?
- List all Red shirts under $30
- What's the total inventory value?
- How many different sizes of Levi shirts do we have?
- Show shirts with discounts greater than 20%

---

# 🗄️ Database Schema

## `t_shirts`

| Column | Type | Description |
|---|---|---|
| t_shirt_id | INT PK | Unique identifier |
| brand | ENUM | Van Heusen, Levi, Nike, Adidas |
| color | ENUM | Red, Blue, Black, White |
| size | ENUM | XS, S, M, L, XL |
| price | DECIMAL | $15–50 range |
| stock_quantity | INT | Available units |
| created_at | TIMESTAMP | Record creation time |

---

## `discounts`

| Column | Type | Description |
|---|---|---|
| discount_id | INT PK | Unique identifier |
| t_shirt_id | INT FK | References t_shirts |
| pct_discount | DECIMAL | 5%–25% range |
| discount_name | VARCHAR | Discount label |
| start_date | DATE | Start date |
| end_date | DATE | End date |

---

# 🛡️ Security

- ✅ Read-only queries only
- ✅ INSERT, DELETE, DROP blocked
- ✅ Input validation before SQL execution
- ✅ API keys never exposed
- ✅ Safe error handling
- ✅ `.env` credentials outside source code

---

# 🐛 Common Issues

## Database connection failed

- Ensure MySQL is running
- Verify `.env` credentials
- Test manually:

```bash
mysql -u root -p
```

---

## GOOGLE_API_KEY not set

- Get key from Google AI Studio
- Add to `.env`
- Restart Streamlit

---

## ModuleNotFoundError

```bash
pip install -r requirements_updated.txt --upgrade
```

---

## Port 8501 already in use

```bash
streamlit run main_enhanced.py --server.port 8502
```

---

# ❤️ Built With

- Google Gemini AI
- LangChain
- Streamlit
- MySQL

---

# 📜 License

Licensed under MIT.

Contributions welcome.
