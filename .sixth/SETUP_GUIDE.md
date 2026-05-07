# 🚀 Setup Guide - Atliq Tees Assistant

Complete step-by-step setup instructions for all platforms.

---

## 📋 Table of Contents

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

## Installation Steps

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

✅ You should see `(venv)` prefix in terminal


.\.venv\Scripts\python.exe -m pip install -r requirements_updated.txt
.\.venv\Scripts\python.exe -m pip install -r requirements_updated.txt

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all packages
pip install -r requirements_updated.txt
```

⏳ This may take 2-3 minutes...

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
5. ⚠️ **Keep this secret!** Never share it.

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
5. Click ⚡ **Execute**

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

✅ Browser opens automatically at `http://localhost:8501`

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

## Configuration

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

### Streamlit Configuration (Optional)

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

✅ Should open browser to http://localhost:8501

---

## Platform-Specific Setup

### Windows 10/11

**MySQL Setup:**
1. Download MySQL Community Server
2. Run installer (.msi)
3. Choose "Server only" installation
4. Default port: 3306
5. Configure MySQL as Windows Service
6. Remember the root password!

**Command Prompt Tips:**
- Use Command Prompt (not PowerShell) for better compatibility
- Activate venv: `venv\Scripts\activate`
- Run Streamlit: `streamlit run main_enhanced.py`

### macOS

**MySQL Setup:**
```bash
# Using Homebrew
brew install mysql
brew services start mysql

# Or download DMG from mysql.com
```

**Terminal Setup:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_updated.txt
```

### Linux (Ubuntu/Debian)

**MySQL Setup:**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo systemctl start mysql
```

**Terminal Setup:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_updated.txt
```

---

## Common Setup Issues

### Issue: "python not found"
**Solution:**
- Install Python from python.org
- Add to PATH (Windows): Set in Environment Variables
- Verify: `python --version`

### Issue: "MySQL connection failed"
**Solution:**
- Check MySQL is running
  - Windows: Services → MySQL
  - macOS: `brew services list`
  - Linux: `systemctl status mysql`
- Verify credentials in .env
- Test connection: `mysql -u root -p`

### Issue: "GOOGLE_API_KEY not set"
**Solution:**
1. Create `.env` file in project root
2. Add: `GOOGLE_API_KEY=your_actual_key`
3. Save file
4. Restart Streamlit

### Issue: "ModuleNotFoundError: No module named..."
**Solution:**
```bash
# Ensure venv is activated (shows (venv) in terminal)
pip install -r requirements_updated.txt --upgrade
```

### Issue: "Port 8501 already in use"
**Solution:**
```bash
# Use different port
streamlit run main_enhanced.py --server.port 8502
```

---

## Performance Optimization

### Database Performance
```bash
# Check indexes
SHOW INDEXES FROM t_shirts;

# Analyze table
ANALYZE TABLE t_shirts;
ANALYZE TABLE discounts;
```

### Application Performance
- First query: 2-3 seconds (model initialization)
- Subsequent queries: <1 second
- Large result sets: May take longer
- Clear history if app becomes slow

---

## Next Steps

✅ Setup complete! Now:

1. **Try Example Questions**: Use built-in examples
2. **Explore Data**: Check Analytics tab
3. **Read Documentation**: See docs/ folder
4. **Ask Questions**: Type your own queries
5. **Export Results**: Download data as CSV

---

## Getting Help

### Resources
- 📖 README.md - Overview and features
- 📋 FEATURES.md - Detailed feature guide
- 🐛 TROUBLESHOOTING.md - Common issues
- 💬 GitHub Issues - Report bugs
- 📧 Support email

### Quick Checks
```bash
# Test everything in one go
python -c "
import mysql.connector
import streamlit
import langchain_google_genai
print('✅ All imports successful!')
"
```

---

## Uninstallation

If you need to remove everything:

```bash
# Remove virtual environment
rm -rf venv  # macOS/Linux
rmdir venv /s /q  # Windows

# Remove MySQL (OS-specific)
# Windows: Control Panel → Programs → Uninstall Programs
# macOS: brew uninstall mysql
# Linux: sudo apt-get remove mysql-server
```

---

**🎉 You're all set! Enjoy using Atliq Tees Assistant!**
