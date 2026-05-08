# 👔 Atliq Tees — NL to SQL Assistant

Ask questions in plain English. Get instant answers from your inventory database — powered by Google Gemini AI.

![Version](https://img.shields.io/badge/version-v2.0%20stable-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![MySQL](https://img.shields.io/badge/MySQL-orange)
![Gemini](https://img.shields.io/badge/Google-Gemini%20AI-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![UI](https://img.shields.io/badge/UI-Streamlit-blue)


Complete step-by-step setup instructions for all platforms.

---


1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Database Setup](#database-setup)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.8+** → [Download](https://www.python.org/downloads/)
- **MySQL Server** → [Download](https://dev.mysql.com/downloads/mysql/)
- **Git** (optional) → [Download](https://git-scm.com/)

### Required Accounts
- **Google Gemini API** (Free) → [Get Key](https://aistudio.google.com/)

### System Requirements
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 500MB for dependencies
- **Internet**: Required for Google Gemini API
- **OS**: Windows, macOS, or Linux

---

**Installation Steps**

### Step 1: Download Project Files

**Option A: Using Git** (Recommended)
```bash
git clone <repository-url>
cd atliq-tees-assistant
```

**Option B: Manual Download**
1. Download ZIP from repository
2. Extract to desired location
3. Open terminal/CMD in that folder

### Step 2: Create Python Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

 You should see `(venv)` prefix in terminal


.\.venv\Scripts\python.exe -m pip install -r requirements_updated.txt
.\.venv\Scripts\python.exe -m pip install -r requirements_updated.txt

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all packages
pip install -r requirements_updated.txt
```


**Verify Installation:**
```bash
pip list | grep streamlit
pip list | grep langchain
pip list | grep pymysql
```

### Step 4: Get Google Gemini API Key

1. Go to https://aistudio.google.com/
2. Click **"Get API Key"** button
3. Click **"Create new API key"**
4. Copy the key (starts with `AIzaSy...`)


### Step 5: Database Setup

#### Windows - Using MySQL Command Prompt
```bash
# Connect to MySQL
mysql -u root -p

# You'll be prompted for password, enter it

# Then paste the SQL commands from db_creation_enhanced.sql
```

#### macOS/Linux - Using Terminal
```bash
mysql -u root -p < db_creation_enhanced.sql
```

#### GUI Method - MySQL Workbench
1. Open MySQL Workbench
2. Double-click your MySQL connection
3. Menu: **File** → **Open SQL Script**
4. Select `db_creation_enhanced.sql`


**Verify Database Created:**
```bash
mysql -u root -p
SHOW DATABASES;
USE atliq_tshirts;
SELECT COUNT(*) FROM t_shirts;
```

Should show a number > 0

### Step 6: Create .env Configuration File

1. **Copy template:**
```bash
cp .env.example .env
```

2. **Edit .env file:**
```env
GOOGLE_API_KEY=AIzaSy_YOUR_KEY_HERE
GOOGLE_MODEL=gemini-1.5-flash

DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=atliq_tshirts
```

3. **Save and close**

### Step 7: Run Application

```bash
streamlit run main_enhanced.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

 Browser opens at `http://localhost:8501`

---

## Database Setup Details

### What Gets Created

The SQL script creates:

1. **Database**: `atliq_tshirts`
2. **Tables**:
   - `t_shirts` - 80+ sample records
   - `discounts` - 15+ sample records
3. **Views**:
   - `v_inventory_summary` - Brand/color statistics
   - `v_discount_details` - Discount information
   - `v_low_stock_alert` - Low stock items
4. **Indexes** - For fast queries

### Sample Data

**T-Shirts:**
- Brands: Van Heusen, Levi, Nike, Adidas
- Colors: Red, Blue, Black, White
- Sizes: XS, S, M, L, XL
- Prices: $15-50 range
- Stock: 20-220 units

**Discounts:**
- Applied to 15 random products
- Range: 5%-25% off
- Valid dates included

---

**Configuration**

### .env File Breakdown

```env
# ===== GOOGLE AI =====
# Get from https://aistudio.google.com/
GOOGLE_API_KEY=AIzaSy_...        # Your Gemini API key
GOOGLE_MODEL=gemini-1.5-flash    # Model version

# ===== DATABASE =====
DB_USER=root                     # MySQL username
DB_PASSWORD=mypassword           # MySQL password
DB_HOST=localhost                # Database host
DB_PORT=3306                     # Database port (default)
DB_NAME=atliq_tshirts           # Database name
```

### Streamlit Configuration Extra Work**

Create `~/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true
logger.level = "info"
```

---

## Verification

### Check 1: Python Installation
```bash
python --version
# Should show 3.8+
```

### Check 2: Virtual Environment
```bash
which python  # macOS/Linux
where python  # Windows
# Should show path with venv/bin (or venv\Scripts)
```

### Check 3: Dependencies
```bash
pip show streamlit
pip show pymysql
pip show langchain-google-genai
```

### Check 4: MySQL Connection
```bash
mysql -u root -p
SHOW DATABASES;
USE atliq_tshirts;
DESCRIBE t_shirts;
```

### Check 5: Database Data
```bash
mysql -u root -p
USE atliq_tshirts;
SELECT COUNT(*) as total_shirts FROM t_shirts;
SELECT COUNT(*) as total_discounts FROM discounts;
```

Should show:
- total_shirts: 80+
- total_discounts: 15+

### Check 6: API Key
```bash
python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"
# Should print your key (without the .env it won't work)
```

### Check 7: Run App
```bash
streamlit run main_enhanced.py
```

 **open browser to http://localhost:8501**

---



#
**Terminal Setup:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_updated.txt
```















**🎉 You're all set! Enjoy using Atliq Tees Assistant!**
