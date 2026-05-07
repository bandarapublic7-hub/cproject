# 🐛 Troubleshooting Guide

Solutions for common issues and error messages.

---

## 📋 Quick Navigation

- [Connection Issues](#connection-issues)
- [API & Authentication](#api--authentication)
- [Database Issues](#database-issues)
- [Performance Issues](#performance-issues)
- [Query Issues](#query-issues)
- [Installation Issues](#installation-issues)

---

## Connection Issues

### ❌ "Database connection failed"

**Error Message:**
```
Error: Database connection failed: (pymysql.err.OperationalError) 
(2003, "Can't connect to MySQL server on 'localhost' (111)")
```

**Causes & Solutions:**

1. **MySQL Not Running**
   ```bash
   # Windows
   # Services → MySQL → Start
   
   # macOS
   brew services start mysql
   
   # Linux
   sudo systemctl start mysql
   ```

2. **Wrong Credentials**
   - Edit .env file
   - Verify DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
   - Test connection: `mysql -u root -p`

3. **Wrong Host/Port**
   - Default host: `localhost` or `127.0.0.1`
   - Default port: `3306`
   - Check your MySQL config if different

4. **Database Not Created**
   ```bash
   mysql -u root -p
   SHOW DATABASES;
   # Should see 'atliq_tshirts'
   # If not, run: db_creation_enhanced.sql
   ```

**Debug Checklist:**
- [ ] MySQL service is running
- [ ] Credentials are correct
- [ ] Database exists
- [ ] .env file is in project root
- [ ] No special characters in password (or escape them)

---

### ❌ "Connection timeout"

**Error Message:**
```
timeout during connection
Max retries exceeded with url
```

**Causes:**
- MySQL server crashed
- Network connectivity issue
- Firewall blocking port 3306
- Server too busy

**Solutions:**
```bash
# 1. Restart MySQL
sudo systemctl restart mysql  # Linux
brew services restart mysql   # macOS

# 2. Check MySQL status
mysql -u root -p -e "SELECT 1"

# 3. Check firewall (Linux)
sudo ufw allow 3306

# 4. Try localhost vs 127.0.0.1
# Edit .env: DB_HOST=127.0.0.1
```

---

### ⚠️ "Access denied for user 'root'"

**Error Message:**
```
(1045, "Access denied for user 'root'@'localhost' 
(using password: YES)")
```

**Causes:**
- Wrong password
- User doesn't have permissions
- Password has special characters

**Solutions:**
```bash
# 1. Test password
mysql -u root -p
# Enter password

# 2. Reset root password (Windows)
# MySQL → Command Line Client
# Or reinstall with new password

# 3. Reset root password (macOS/Linux)
sudo mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword';
FLUSH PRIVILEGES;
```

---

## API & Authentication

### ❌ "GOOGLE_API_KEY is not set"

**Error Message:**
```
Set a real GOOGLE_API_KEY in .env.
ValueError: API key not valid. Please pass a valid API key.
```

**Solutions:**

1. **Get API Key**
   - Go to https://aistudio.google.com/
   - Click "Get API Key"
   - Create new key
   - Copy the full key

2. **Add to .env**
   ```env
   GOOGLE_API_KEY=AIzaSy_1234567890_ABCDEFGHIJK
   ```

3. **Verify Setup**
   ```bash
   python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"
   # Should print your key
   ```

4. **Restart App**
   ```bash
   # Stop Streamlit (Ctrl+C)
   # Restart: streamlit run main_enhanced.py
   ```

**Common Mistakes:**
- ❌ Key incomplete (cut off)
- ❌ Key in quotes
- ❌ Typo in variable name
- ❌ File not saved
- ❌ Using .env.example instead of .env

---

### ❌ "Invalid API key"

**Error Message:**
```
API returned an error: 403 Forbidden
Invalid API key provided
```

**Causes:**
- Key is fake/invalid
- Key not activated
- Using old/deleted key

**Solutions:**
1. Generate new key from https://aistudio.google.com/
2. Make sure key starts with `AIzaSy_`
3. Key should be 40+ characters
4. Copy exact key, no spaces

---

### ❌ "API rate limit exceeded"

**Error Message:**
```
429 Too Many Requests
Rate limit exceeded. Please try again later.
```

**Causes:**
- Too many queries in short time
- Free tier limitations
- Concurrent requests

**Solutions:**
```bash
# Wait a few minutes
# Then try again

# Use Gemini API Pro for higher limits
# Or space out queries (2-3 second gap)
```

---

## Database Issues

### ❌ "Table 'atliq_tshirts.t_shirts' doesn't exist"

**Error Message:**
```
pymysql.err.ProgrammingError: (1146, 
"Table 'atliq_tshirts.t_shirts' doesn't exist")
```

**Solutions:**
```bash
# 1. Run SQL setup
mysql -u root -p < db_creation_enhanced.sql

# 2. Verify database exists
mysql -u root -p
SHOW DATABASES;
USE atliq_tshirts;
SHOW TABLES;
```

**Using MySQL Workbench:**
1. Open MySQL Workbench
2. File → Open SQL Script
3. Select db_creation_enhanced.sql
4. Click ⚡ Execute

---

### ❌ "No data in tables"

**Error Message:**
```
Empty result set
SELECT returned no rows
```

**Solutions:**
```bash
# Check if data was loaded
mysql -u root -p
USE atliq_tshirts;
SELECT COUNT(*) FROM t_shirts;
SELECT COUNT(*) FROM discounts;
# Should show numbers > 0

# If empty, re-run setup
mysql -u root -p < db_creation_enhanced.sql
```

---

### ⚠️ "Slow queries"

**Symptoms:**
- Queries taking >5 seconds
- App feels sluggish
- Loading spinners stuck

**Solutions:**
```bash
# 1. Check table size
mysql -u root -p
USE atliq_tshirts;
SELECT COUNT(*) FROM t_shirts;

# 2. Analyze tables
ANALYZE TABLE t_shirts;
ANALYZE TABLE discounts;

# 3. Check indexes
SHOW INDEXES FROM t_shirts;
SHOW INDEXES FROM discounts;

# 4. Recreate if corrupted
# Backup then re-run setup script
```

---

### ⚠️ "Disk space error"

**Error Message:**
```
The server has run out of disk space
MySQL error 1021
```

**Solutions:**
```bash
# Check disk space
df -h  # Linux/macOS
# For Windows: Check C: drive space

# Free up space:
# 1. Delete old logs
# 2. Remove large files
# 3. Clean temporary files

# Restart MySQL
sudo systemctl restart mysql
```

---

## Performance Issues

### ⚠️ "First query is very slow"

**Expected Behavior:**
- First query: 2-3 seconds
- Subsequent queries: <1 second

**Why?**
- Model initialization (first time)
- API warmup
- Database connection establishment

**Normal timing breakdown:**
```
Generating SQL    : 1-2 seconds
Executing query   : 0.5 seconds
Writing response  : 0.5-1 seconds
Total first query : 2-4 seconds
```

**This is normal! Not a problem.**

---

### ⚠️ "App running slowly"

**Causes:**
- Too much history (>20 queries)
- Large database
- Low system RAM
- Slow internet

**Solutions:**
1. Clear query history (Sidebar button)
2. Close other applications
3. Restart Streamlit app
4. Check internet speed
5. Upgrade RAM if needed

---

### ⚠️ "Out of memory error"

**Error Message:**
```
MemoryError
malloc: unable to allocate
```

**Causes:**
- Large result sets
- Memory leak
- Too many queries cached

**Solutions:**
```bash
# 1. Clear history
# Sidebar → "Clear Query History"

# 2. Restart app
# Ctrl+C → streamlit run main_enhanced.py

# 3. Check system RAM
# Task Manager (Windows) or top (Linux/macOS)

# 4. Close other apps
```

---

## Query Issues

### ❌ "Only read-only queries are allowed"

**Error Message:**
```
ValueError: Only read-only queries are allowed.
```

**Causes:**
- Question includes INSERT, DELETE, UPDATE, DROP, ALTER, CREATE
- LLM generated unsafe query

**Solution:**
Ask a read-only question:
```
✅ "Show all Nike shirts"
✅ "What's the average price?"
❌ "Delete old records"
❌ "Update product prices"
```

---

### ❌ "The model did not return a query"

**Error Message:**
```
ValueError: The model did not return a query.
```

**Causes:**
- API timeout
- Invalid question
- Network issue

**Solutions:**
```bash
# 1. Try again (retries happen automatically)
# 2. Rephrase question more clearly
# 3. Check internet connection
# 4. Check API key validity
```

---

### ❌ "The available tables do not contain that information"

**Message:**
```
"The available tables do not contain that information."
```

**Causes:**
- Asking about non-existent columns
- Data doesn't exist in database
- Schema limitation

**Available columns:**
```sql
t_shirts:
  - brand (Van Heusen, Levi, Nike, Adidas)
  - color (Red, Blue, Black, White)
  - size (XS, S, M, L, XL)
  - price (10-50)
  - stock_quantity

discounts:
  - pct_discount
  - discount_name
  - start_date, end_date
```

**Solution:** Ask about available columns only

---

### ⚠️ "Results are incorrect"

**Solutions:**
1. Check the SQL query (SQL tab)
2. Verify it matches your question
3. Check sample data in database
4. Try different question phrasing
5. Report if SQL is wrong

---

### ⚠️ "Query results are empty"

**Causes:**
- No matching data
- Wrong filter values
- Typo in brand/color names

**Brands:** Van Heusen, Levi, Nike, Adidas (exact case)
**Colors:** Red, Blue, Black, White (exact case)
**Sizes:** XS, S, M, L, XL

**Example:**
```
❌ "nike shirts"    (lowercase - won't work)
✅ "Nike shirts"    (correct case)
```

---

## Installation Issues

### ❌ "Python not found"

**Error:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**
1. **Install Python** from python.org
2. **Add to PATH** (Windows):
   - Search: "Environment Variables"
   - Edit System Environment Variables
   - Add Python path: `C:\Python311\`
3. **Verify installation:**
   ```bash
   python --version
   ```

---

### ❌ "pip not found"

**Error:**
```
'pip' is not recognized
```

**Solutions:**
```bash
# Try python -m pip
python -m pip install --upgrade pip

# Or reinstall Python with pip option checked
```

---

### ❌ "Module not found"

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Causes:**
- Virtual environment not activated
- Dependencies not installed

**Solutions:**
```bash
# 1. Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements_updated.txt

# 3. Verify
pip list | grep streamlit
```

---

### ❌ "Permission denied"

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Causes:**
- File permissions
- Directory permissions
- Running without admin rights

**Solutions:**
```bash
# Run as administrator
# Windows: Right-click Command Prompt → Run as Administrator
# macOS/Linux: Use sudo (not ideal but works)

# Or fix permissions
chmod 755 filename
```

---

## Advanced Troubleshooting

### 📊 Enable Debug Mode

**Edit .streamlit/config.toml:**
```toml
[logger]
level = "debug"

[client]
showErrorDetails = true
logUploaderProgressDetails = true
```

### 🔍 Check Logs

**Streamlit logs:**
```bash
# Windows
%APPDATA%\.streamlit\logs

# macOS/Linux
~/.streamlit/logs
```

### 🧪 Test Components Independently

**Test MySQL:**
```bash
mysql -u root -p -e "SELECT 1"
```

**Test API Key:**
```python
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
print(f"API Key set: {bool(api_key)}")
print(f"Key starts with: {api_key[:10] if api_key else 'None'}")
```

**Test Dependencies:**
```bash
python -c "
import streamlit
import pymysql
import langchain_google_genai
print('✅ All imports OK')
"
```

---

## Getting Help

### Provide This Information

When reporting bugs, include:
1. **Error message** (full text)
2. **Steps to reproduce**
3. **OS** (Windows/macOS/Linux)
4. **Python version** (`python --version`)
5. **Streamlit version** (`streamlit --version`)
6. **MySQL version** (`mysql --version`)

### Where to Get Help

1. **Documentation:** Check SETUP_GUIDE.md, FEATURES.md
2. **GitHub Issues:** Search existing issues
3. **Stack Overflow:** Tag with [streamlit] [mysql] [python]
4. **Email Support:** (if applicable)

---

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| MySQL connection | Restart service, check credentials |
| API key error | Get from aistudio.google.com |
| Slow first query | Normal, caching makes next fast |
| Empty results | Check data exists, verify column values |
| Permission denied | Run as admin, check file perms |
| Module not found | Activate venv, pip install |
| Port in use | Use `streamlit run main.py --server.port 8502` |

---

**Still stuck? Check all three docs: README.md, SETUP_GUIDE.md, FEATURES.md**
