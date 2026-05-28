# 👔 Atliq Tees - Natural Language to SQL Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-Active-success?style=for-the-badge)

### 🚀 Transform Natural Language into SQL Queries Instantly

A modern, intelligent web application that converts everyday business questions into SQL queries for seamless inventory management. Perfect for non-technical users to query their t-shirt store database without writing SQL code.

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-system-architecture) • [Documentation](#-documentation)

</div>

---

## ✨ Features

### 🔍 Core Capabilities

| Feature | Description | Benefit |
|---------|-------------|---------|
| 🤖 **AI-Powered NL2SQL** | Converts English to SQL automatically | No SQL knowledge needed |
| 🔒 **Read-Only Safety** | Blocks dangerous operations | Data protection guaranteed |
| ⚡ **Real-Time Execution** | Instant query processing | Fast business insights |
| 📊 **Smart Analytics** | Built-in inventory dashboard | Quick decision-making |
| 💾 **Query Caching** | Optimized performance | Faster subsequent queries |
| 📜 **Query History** | Track last 20 queries | Easy reference & audit trail |
| 📥 **CSV Export** | Download results instantly | Seamless integration with Excel |
| 🎨 **Modern UI** | Clean, intuitive interface | Better user experience |

---

## 🏗️ System Architecture

### 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
│                    (Streamlit Web App)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Query      │  │  Analytics   │  │   History    │       │
│  │  Assistant   │  │  Dashboard   │  │   Manager    │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
┌─────────┴──────────────────┴──────────────────┴──────────────┐
│               APPLICATION LOGIC LAYER                         │
│  ┌──────────────────┐      ┌──────────────────┐              │
│  │  NL2SQL Engine   │◄────►│  Query Validator │              │
│  │  (LangChain)     │      │  (Security)      │              │
│  └──────────────────┘      └──────────────────┘              │
│  ┌──────────────────┐      ┌──────────────────┐              │
│  │  Response Gen    │◄────►│  Error Handler   │              │
│  │  (AI Formatting) │      │  (Retry Logic)   │              │
│  └──────────────────┘      └──────────────────┘              │
└────────────────────────────────────┬──────────────────────────┘
                                     │
┌────────────────────────────────────┴──────────────────────────┐
│               DATA ACCESS LAYER                               │
│  ┌──────────────────────┐      ┌──────────────────────┐       │
│  │  Database Connection │      │  Connection Pool     │       │
│  │  (PyMySQL Driver)    │      │  (Caching)           │       │
│  └──────────────────────┘      └──────────────────────┘       │
└────────────────────────────────────┬──────────────────────────┘
                                     │
┌────────────────────────────────────┴──────────────────────────┐
│               EXTERNAL SERVICES                               │
│  ┌──────────────────────┐      ┌──────────────────────┐       │
│  │ Google Gemini API    │      │ MySQL Database       │       │
│  │ (AI Model)           │      │ (Data Storage)       │       │
│  └──────────────────────┘      └──────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### 🔄 Request Flow Diagram

```
START → User Types Question → Input Validation → NL → SQL Generation
                                                      ↓
                                            (with Retry Logic: 3 attempts)
                                                      ↓
                                            Security Validation
                                                      ↓
                          ┌─ BLOCKED → Error Message
                          │
                    VALID ↓
                          
                    MySQL Database (Execute SELECT)
                          ↓
                    Format Results
                          ↓
                    AI Response Generation
                          ↓
            Display Results (Answer, SQL, Raw Data, Export)
                          ↓
            Store in Query History
                          ↓
                        END
```

### 📊 Component Hierarchy

```
ATLIQ TEES APPLICATION
│
├── 🎨 FRONTEND LAYER
│   ├── Query Assistant Tab
│   │   ├── Question Input Box
│   │   ├── Quick Filter Buttons (📊📈💰🏷️)
│   │   └── Example Questions
│   ├── Analytics Tab
│   │   ├── Inventory by Brand
│   │   ├── Price Statistics
│   │   └── Stock Distribution
│   ├── History Tab
│   │   ├── Query List
│   │   └── Details View
│   └── Export Options
│       ├── Download CSV
│       ├── View Raw Data
│       └── Copy SQL
│
├── 🧠 LOGIC LAYER
│   ├── NL2SQL Engine (LangChain + Gemini)
│   ├── Security Module (Keyword Validator, Injector Detector)
│   ├── Query Executor (Database Connection, Execution, Retry)
│   └── Response Formatter (Parser, AI Generator, Export)
│
├── 💾 DATA LAYER
│   ├── MySQL Connection Manager
│   ├── Database Tables (t_shirts, discounts)
│   ├── Database Views (inventory_summary, discount_details)
│   └── Session Storage (Query History Cache)
│
└── 🔌 EXTERNAL SERVICES
    ├── Google Gemini API (NL2SQL, Response Formatting)
    └── MySQL Database (Data Storage & Retrieval)
```

---

## 🚀 Quick Start

### ⚙️ Prerequisites

```bash
✅ Python 3.8+
✅ MySQL Server (local or remote)
✅ Google Gemini API Key (free at aistudio.google.com)
✅ 2GB RAM minimum
✅ Internet connection
```

### 📥 Installation (5 Minutes)

#### 1️⃣ Clone Repository
```bash
git clone <repository-url>
cd atliq-tees-assistant
```

#### 2️⃣ Setup Python Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements_updated.txt
```

#### 4️⃣ Setup Database
```bash
mysql -u root -p < db_creation_enhanced.sql
```

#### 5️⃣ Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

#### 6️⃣ Run Application
```bash
streamlit run main_enhanced.py
```

✅ Opens at http://localhost:8501

---

## 📖 Usage Guide

### 🔍 Basic Workflow

```
Ask Question → Click Ask → View Results → Export/Share → Check History
```

### 💡 Example Questions

```
✅ "How many XL Black Adidas shirts are in stock?"
✅ "What's the average price of Nike shirts?"
✅ "Show all items with more than 20% discount"
✅ "Which size has the most inventory?"
```

### 📊 Quick Filters

| Button | Action | Use Case |
|--------|--------|----------|
| 📊 Stock Overview | Total inventory by brand | Identify overstocked |
| 💰 Price Range | Average price by size | Pricing strategy |
| 🏷️ Discounts | Current discounts info | Promotion tracking |
| 📈 Top Seller | Brand with most inventory | Reordering |

---

## 📂 Project Structure

```
atliq-tees-assistant/
├── 📄 main_enhanced.py              # Main Streamlit app
├── 📄 db_creation_enhanced.sql      # Database setup
├── 📄 requirements_updated.txt      # Python dependencies
├── 📄 .env.example                  # Config template
├── 📄 README.md                     # This file
└── 📁 docs/
    ├── FEATURES.md                  # Feature guide
    ├── SETUP_GUIDE.md              # Setup instructions
    └── TROUBLESHOOTING.md          # Common issues
```

---

## 🔒 Security Features

```
✅ Read-Only Enforcement (SELECT only)
✅ Input Validation & Sanitization
✅ SQL Injection Prevention
✅ Keyword Filtering (blocks INSERT, DELETE, DROP)
✅ Graceful Error Handling
✅ API Key Protection (.env storage)
✅ Session Isolation
```

---

## 🗄️ Database Schema

### T-Shirts Table
```sql
t_shirt_id (PK) | brand | color | size | price | stock_quantity | created_at | updated_at
```

### Discounts Table
```sql
discount_id (PK) | t_shirt_id (FK) | pct_discount | discount_name | start_date | end_date
```

### Sample Data
- **80+ T-shirt records** across 4 brands (Nike, Adidas, Levi, Van Heusen)
- **5 colors**: Red, Blue, Black, White, Green
- **5 sizes**: XS, S, M, L, XL
- **Price range**: $15-50
- **15+ discount records** with 5%-25% off

---

## ⚡ Performance Metrics

```
Cold Start (First Query):     2-3 seconds (model initialization)
Cached Queries:               <1 second
Large Result Sets:            1-2 seconds
Export (CSV):                 <500ms
```

---

## 🛠️ Configuration

### Environment Variables (.env)

```env
GOOGLE_API_KEY=AIzaSy_YOUR_KEY_HERE
GOOGLE_MODEL=gemini-1.5-flash
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=atliq_tshirts
```

---

## 📊 Features at a Glance

### Analytics Dashboard
```
Inventory by Brand | Price Statistics | Stock Distribution
Nike: 450         | Min: $15         | Red: 180
Adidas: 380       | Max: $50         | Blue: 160
Levi: 285         | Avg: $32.50      | Black: 200
Van Heusen: 320   |                  | White: 120
```

### Export Options
```
📥 Download CSV → Open in Excel/Google Sheets
📋 View Raw Data → Copy & paste anywhere
📄 Copy SQL → Modify & reuse
```

### Query History
```
[2024-01-15 14:30] Nike stock details          View
[2024-01-15 14:28] Adidas average price        View
[2024-01-15 14:25] Current discounts           View
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Database connection failed | Check MySQL running, verify .env credentials |
| GOOGLE_API_KEY not set | Create .env file with your API key |
| ModuleNotFoundError | Activate venv, reinstall dependencies |
| Port 8501 already in use | Use different port: `--server.port 8502` |

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | Overview & quick start |
| **FEATURES.md** | Detailed feature guide |
| **SETUP_GUIDE.md** | Step-by-step setup |
| **TROUBLESHOOTING.md** | Issues & solutions |

---

## 🎓 Technology Stack

```
Frontend:     Streamlit, HTML/CSS
AI/ML:        Google Gemini API, LangChain
Database:     MySQL 8.0+, PyMySQL
Backend:      Python 3.8+
Security:     Input validation, Keyword filtering
```

---

## 📊 Use Cases

### 🏪 Retail Manager
Daily: Check stock → Query low items → Export for ordering → Track discounts

### 📈 Data Analyst
Weekly: Generate reports → Analyze trends → Create visualizations → Share insights

### 🛍️ Store Owner
Monthly: Review inventory → Analyze by brand → Plan promotions → Forecast restocking

---

## ✅ Verification Checklist

```bash
☑️ Python 3.8+:           python --version
☑️ Virtual environment:    which python (shows venv path)
☑️ Dependencies:           pip show streamlit, pymysql
☑️ MySQL connection:       mysql -u root -p
☑️ Database setup:         SELECT COUNT(*) FROM atliq_tshirts.t_shirts;
☑️ API key in .env:        Check GOOGLE_API_KEY
☑️ Application runs:       streamlit run main_enhanced.py
```

---

## 📝 License

MIT License © 2024 Atliq Tees

---

## 🤝 Contributing

```
1. Fork repository
2. Create feature branch: git checkout -b feature/AmazingFeature
3. Commit changes: git commit -m 'Add AmazingFeature'
4. Push to branch: git push origin feature/AmazingFeature
5. Open Pull Request
```

---

## 📞 Support & Resources

### Quick Links
- 🎓 [Google Gemini Docs](https://ai.google.dev/docs)
- 📚 [Streamlit Docs](https://docs.streamlit.io/)
- 🗄️ [MySQL Reference](https://dev.mysql.com/doc/)
- 🔗 [LangChain Docs](https://python.langchain.com/)

### Get Help
- 📖 Read documentation in `/docs`
- 🐛 Check TROUBLESHOOTING.md
- 💬 Open GitHub issues
- 📧 Contact support

---

## 📊 Version History

| Version | Features |
|---------|----------|
| **v2.0** | 🎨 Redesigned UI, 📊 Analytics, 📜 History, 📥 Export |
| **v1.0** | 🔍 NL2SQL, ⚡ Real-time execution |

---

## 🎉 Getting Started

### 🚀 Next Steps
1. ✅ Complete Quick Start setup
2. 🎯 Try example questions
3. 📊 Explore Analytics tab
4. 📖 Read detailed docs
5. 💡 Ask your own questions
6. 📥 Export & analyze results

### 💡 Pro Tips
- Use Quick Filter buttons for fast queries
- Check Analytics before detailed queries
- Review Query History to reuse past queries
- Export results for further analysis

---

<div align="center">

### 🌟 Ready to Transform Your Data?

**Start querying with natural language today!**

Made with ❤️ for inventory management excellence

*Last Updated: January 2024*

</div>
