# 👔 Atliq Tees - Natural Language to SQL Assistant

A modern web application that converts natural language questions into SQL queries for inventory management. Perfect for non-technical users to query their t-shirt store database.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

### 🔍 Core Features
- **Natural Language to SQL**: Ask questions in plain English, get SQL queries automatically
- **Safe Execution**: Read-only queries only - no data modification risks
- **Real-time Results**: Instant query execution with beautiful formatting
- **AI-Powered Responses**: Google Gemini AI generates human-friendly answers

### 📊 Advanced Features
- **Query History**: Track last 20 queries with timestamps
- **Quick Filters**: One-click queries for common questions
- **Analytics Dashboard**: View inventory statistics and insights
- **Export Functionality**: Download results as CSV files
- **Smart Caching**: Optimized database and model initialization

### 🎨 User Experience
- **Modern UI**: Clean, professional interface with Streamlit
- **Responsive Design**: Works on desktop and mobile
- **Tabbed Interface**: Organized sections for different functions
- **Example Questions**: Pre-built question templates
- **Error Handling**: Clear, helpful error messages

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL Server (local or remote)
- Google Gemini API key (free)
- 2GB RAM minimum

### 1️⃣ Clone Repository
```bash
git clone <repository-url>
cd atliq-tees-assistant
```

### 2️⃣ Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements_updated.txt
```

### 4️⃣ Set Up Database

**Option A: Using MySQL CLI**
```bash
mysql -u root -p < db_creation_enhanced.sql
```

**Option B: Using GUI (MySQL Workbench)**
1. Open MySQL Workbench
2. Connect to your MySQL server
3. File → Open SQL Script → Select `db_creation_enhanced.sql`
4. Execute the script (Ctrl+Shift+Enter)

### 5️⃣ Configure Environment

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# Get from https://aistudio.google.com/
GOOGLE_API_KEY=your_actual_api_key_here
GOOGLE_MODEL=gemini-1.5-flash

# Your MySQL credentials
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=atliq_tshirts
```

### 6️⃣ Run the Application
```bash
streamlit run main_enhanced.py
```

The app will open at `http://localhost:8501`

---

## 📋 Example Questions

Try asking:

- "How many White Nike shirts are in stock?"
- "What is the average price of Adidas shirts?"
- "Show all discounts currently available"
- "Which brand has the highest total stock?"
- "List all Red shirts under $30"
- "What's the total inventory value?"
- "How many different sizes of Levi shirts do we have?"
- "Show me shirts with discounts greater than 20%"

---

## 🏗️ Project Structure

```
atliq-tees-assistant/
├── main_enhanced.py              # Main application (improved version)
├── db_creation_enhanced.sql      # Database setup with sample data
├── requirements_updated.txt      # Python dependencies
├── .env.example                  # Configuration template
├── README.md                     # This file
└── docs/
    ├── SETUP_GUIDE.md           # Detailed setup instructions
    ├── FEATURES.md              # Feature documentation
    └── TROUBLESHOOTING.md       # Common issues & solutions
```

---

## 🔧 Configuration Details

### Database Schema

**t_shirts Table**
```sql
- t_shirt_id: Unique identifier
- brand: Van Heusen, Levi, Nike, Adidas
- color: Red, Blue, Black, White
- size: XS, S, M, L, XL
- price: 10-50 (currency units)
- stock_quantity: Available units
- created_at: Record creation timestamp
- updated_at: Last modification timestamp
```

**discounts Table**
```sql
- discount_id: Unique identifier
- t_shirt_id: Foreign key to t_shirts
- pct_discount: 0-100%
- discount_name: Description
- start_date: Discount start date
- end_date: Discount end date
```

### Environment Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `GOOGLE_API_KEY` | `AIzaSy...` | Gemini API key from Google AI Studio |
| `GOOGLE_MODEL` | `gemini-1.5-flash` | LLM model to use |
| `DB_USER` | `root` | MySQL username |
| `DB_PASSWORD` | `password123` | MySQL password |
| `DB_HOST` | `localhost` | Database hostname/IP |
| `DB_PORT` | `3306` | Database port |
| `DB_NAME` | `atliq_tshirts` | Database name |

---

## 📖 Usage Guide

### 🔍 Querying Data

1. **Type Your Question**: Enter any business question about inventory
2. **Click Ask**: Hit the 🚀 Ask button or press Enter
3. **View Results**: See AI-generated answer in the Answer tab
4. **Explore Details**: Check SQL, raw data, or export results

### 📊 Using Analytics

1. Go to the **Analytics** tab
2. View inventory statistics by brand
3. Check price ranges and averages
4. Monitor stock levels

### 📜 Query History

1. Open the **History** tab
2. See all your recent queries
3. Click "View" to see full details
4. Clear history when needed

### 📥 Exporting Results

1. Ask a question and get results
2. Go to **Export** tab
3. Click "Download as CSV"
4. Results saved to your downloads folder

---

## 🔒 Security Features

✅ **Read-Only Queries**: Only SELECT, DESCRIBE, SHOW, WITH allowed
✅ **Keyword Blocking**: INSERT, DELETE, DROP, ALTER, CREATE blocked
✅ **Input Validation**: All queries validated before execution
✅ **Error Safety**: Graceful error handling with helpful messages
✅ **API Security**: API keys not logged or exposed

---

## ⚠️ Troubleshooting

### "Database connection failed"
- Check MySQL is running: `mysql -u root -p`
- Verify credentials in `.env`
- Ensure database exists: `SHOW DATABASES;`

### "GOOGLE_API_KEY not set"
- Get free key from https://aistudio.google.com/
- Add to `.env` file
- Restart the application

### "PyMySQL not installed"
```bash
pip install PyMySQL==1.1.0
```

### "Connection refused" error
- MySQL might not be running
- **Windows**: `Start → Services → MySQL80` (or your version)
- **macOS**: `brew services start mysql`
- **Linux**: `sudo systemctl start mysql`

### "Slow response times"
- First query might be slow (model initialization)
- Subsequent queries are cached for speed
- Check your internet connection for API calls

---

## 🎓 Learning Resources

### MySQL Basics
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQL Tutorial](https://www.w3schools.com/sql/)

### Google Gemini
- [Gemini API Docs](https://ai.google.dev/docs)
- [Prompt Engineering Guide](https://ai.google.dev/docs/guides/prompt_engineering)

### Streamlit
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)

---

## 🐛 Bug Reports & Feature Requests

Found an issue? Have a great idea?

1. Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
2. Search existing issues
3. Create detailed bug report with:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Error messages
   - System info

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👥 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

### Get Help
- 📖 Check documentation in `/docs` folder
- 🐛 Search existing GitHub issues
- 💬 Open a discussion for questions
- 📧 Email support (if applicable)

### Version History

**v2.0** (Current)
- ✨ Redesigned UI with tabs and sections
- 🎨 Modern styling and colors
- 📊 Analytics dashboard
- 📜 Query history with persistence
- 📥 CSV export functionality
- 🚀 Performance improvements

**v1.0**
- Initial release
- Basic natural language to SQL
- Simple query execution

---

## 🙏 Acknowledgments

- Google Gemini AI for powerful language processing
- Streamlit for beautiful web framework
- LangChain for LLM orchestration
- MySQL for robust database

---

## 📊 Performance Tips

1. **First Load**: Be patient on first query (model initialization)
2. **Caching**: Subsequent queries are faster (cached)
3. **Complex Queries**: Simple questions perform better
4. **History**: Keep query history under 50 for best performance
5. **Database**: Ensure MySQL has adequate resources

---

**Happy Querying! 🎉**

For more detailed information, check out the documentation in the `/docs` folder.
