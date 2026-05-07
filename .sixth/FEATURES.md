# ✨ Features Guide - Atliq Tees Assistant

Comprehensive guide to all features and how to use them.

---

## 📋 Table of Contents

1. [Core Features](#core-features)
2. [Query Assistant](#query-assistant)
3. [Analytics Dashboard](#analytics-dashboard)
4. [Query History](#query-history)
5. [Advanced Features](#advanced-features)
6. [Tips & Tricks](#tips--tricks)

---

## Core Features

### 🔍 Natural Language to SQL

**What it does:** Converts English questions to SQL queries automatically.

**How to use:**
1. Type your question in plain English
2. Click "🚀 Ask" button
3. App generates SQL query
4. Results displayed in tabs

**Example:**
```
Question: "How many Red Nike shirts are in stock?"
↓
SQL: SELECT SUM(stock_quantity) FROM t_shirts 
     WHERE brand='Nike' AND color='Red'
↓
Answer: "Nike has 45 red shirts currently in stock."
```

### 🔒 Read-Only Safety

**Security features:**
- ✅ Only SELECT/SHOW/DESCRIBE queries allowed
- ❌ Blocks INSERT, DELETE, UPDATE, DROP, ALTER
- ✅ Input validation on all queries
- ❌ No SQL injection risk

**Example blocked queries:**
```sql
-- ❌ BLOCKED
DELETE FROM t_shirts WHERE id=1;  -- Contains DELETE
INSERT INTO discounts VALUES (...);  -- Contains INSERT
DROP TABLE t_shirts;  -- Contains DROP
```

### ⚡ Real-Time Execution

**Features:**
- Instant query processing
- Live results display
- Error handling with clear messages
- Retry logic for reliability

**Performance:**
- Cold start: 2-3 seconds (first query)
- Cached queries: <1 second
- Large results: 1-2 seconds

---

## Query Assistant

### 💬 Question Input

**Input Methods:**

1. **Type Directly:**
   - Click text input field
   - Type your question
   - Press Enter or click "Ask"

2. **Use Example Questions:**
   - Click any example button
   - Question auto-filled
   - Click "Ask" to execute

3. **Use Quick Filters:**
   - Click filter buttons (📊 Stock Overview, 💰 Price Range, etc.)
   - Pre-built queries execute

**Best Practices:**
- ✅ Be specific: "Red Nike shirts" not "red stuff"
- ✅ Mention brand/color/size when relevant
- ✅ Ask about available columns only
- ❌ Don't ask about non-existent fields

### 📜 Example Questions

**Pre-built examples included:**

```
📊 Stock Overview
💰 Price Range
🏷️ Discounts
📈 Top Sellers
🔍 Inventory Details
```

**Add your own:**
Edit EXAMPLE_QUESTIONS in main_enhanced.py

### 🎯 Quick Filters

**Stock Overview**
- Shows total inventory by brand
- Helps identify overstocked/understocked items

**Price Range**
- Average price by size
- Helps with pricing strategy

**Discounts**
- Current discount information
- Identify which products are on sale

**Top Seller**
- Brand with most inventory
- Useful for reordering

---

## Analytics Dashboard

### 📊 Inventory Analytics

**What's shown:**

1. **Inventory by Brand**
   - Stock count per brand
   - Total units available
   - Visual overview

2. **Price Statistics**
   - Minimum price
   - Maximum price
   - Average price

3. **Stock Distribution**
   - By color
   - By size
   - By price range

**How to access:**
1. Click **Analytics** tab
2. View automatic calculations
3. Use for business insights

**Example Insights:**
```
Nike has 450 units in stock
Adidas average price: $32.50
Red color is most common
L size has highest stock
```

---

## Query History

### 📜 View Past Queries

**Features:**
- Stores last 20 queries
- Shows timestamp
- Displays full query details
- Quick review capability

**Access:**
1. Click **History** tab
2. See all past queries
3. Click "View" to see details
4. Click "Clear" to remove history

**What's stored:**
- Question asked
- SQL query generated
- Raw database result
- AI-generated answer
- Execution timestamp

### 🗑️ Clear History

**Purpose:** Remove all stored queries

**When to use:**
- Privacy concerns
- Reduce app memory usage
- Fresh start

**How:**
1. Sidebar → "Clear Query History" button
2. Confirm deletion
3. History removed

---

## Advanced Features

### 📥 Export Results

**Formats supported:**
- 📄 CSV (Comma-separated values)
- 📋 View raw data
- 💾 Copy SQL query

**How to export:**
1. Ask question and get results
2. Click **Export** tab
3. Click relevant button
4. File downloaded automatically

**Example workflow:**
```
Question → Results → Export Tab → Download CSV
          ↓
     Use in Excel/Sheets
```

### 💾 Download CSV

**What's exported:**
- Query results
- Formatted properly
- Can open in Excel/Google Sheets
- Retains column names

**File naming:**
```
query_20240115_143022.csv
       ↑       ↑
     Date    Time
```

### 📋 Copy SQL

**Use cases:**
- Modify query manually
- Run in MySQL directly
- Learn SQL syntax
- Share with team

**How:**
1. Click "Copy SQL" in Export tab
2. Query code block appears
3. Use your database tool to execute

### 🔍 View Raw Data

**Shows:**
- Exact database response
- Unformatted results
- Useful for debugging
- Technical reference

**Example output:**
```
[('Nike', 450), ('Adidas', 380), ('Levi', 220), ('Van Heusen', 190)]
```

---

## Advanced Features

### 🎨 Visualization

**Available charts:**
- 📊 Data tables (tabular results)
- 📈 Statistics display
- 🏷️ Price analysis
- 📦 Stock quantities

**Auto-formatted results:**
```
Question: "What's the stock by brand?"
↓
Answer: "Van Heusen: 320, Levi: 285, Nike: 450, Adidas: 380"
```

### 🔄 Retry Logic

**Automatic retries:**
- SQL Generation: 3 attempts
- Response Generation: 3 attempts
- Exponential backoff: 2-8 seconds

**Helps with:**
- Network issues
- API timeouts
- Temporary service disruptions

### 💾 Query Caching

**What's cached:**
- Database connection
- LLM model instance
- Query results (in session)

**Benefits:**
- Faster subsequent queries
- Reduced API calls
- Lower latency

---

## Tips & Tricks

### 🎯 Effective Questions

**Good questions:**
```
✅ "How many XL Black Adidas shirts do we have?"
✅ "What's the average price of Nike shirts?"
✅ "Show me all items with more than 30% discount"
✅ "Which size has the most inventory?"
```

**Poor questions:**
```
❌ "How much stuff?" (too vague)
❌ "Gimme red ones" (incomplete)
❌ "Modify the database" (not allowed)
❌ "Chart my data" (not specific)
```

### 📊 Smart Querying

**Performance tips:**
1. Use specific values when filtering
2. Ask one question at a time
3. Use existing filter buttons when possible
4. Check history before re-asking

**Data tips:**
1. Check analytics before detailed queries
2. Use quick filters for common questions
3. Review example questions for inspiration
4. Combine results from multiple queries

### 🔗 Combining Features

**Workflow example:**
```
1. Check Analytics → See which brand has low stock
2. Ask Question → "How many XL Nike shirts?"
3. View Result → Get specific count
4. Check History → Review answer again
5. Export → Save for reporting
```

### ⚡ Speed Optimization

**Fastest approach:**
1. Use Quick Filters for common queries
2. Use Example Questions for preset questions
3. Click "View History" to reuse past queries
4. Cache means second query is fastest

**Slowest approach:**
1. Type complex question
2. System generates SQL from scratch
3. First query is always slowest
4. Model initialization takes time

---

## Common Workflows

### 📦 Stock Management Workflow

```
1. Click "Analytics" tab
2. View "Total Inventory by Brand"
3. Identify low-stock brands
4. Ask: "How many Red Nike XL shirts?"
5. Check discount status
6. Export results for ordering
```

### 💰 Pricing Analysis Workflow

```
1. Click "Analytics" tab
2. Check "Price Statistics"
3. Review price ranges
4. Ask: "Average price by brand?"
5. Compare with competitor prices
6. Export for pricing strategy
```

### 🏷️ Discount Management Workflow

```
1. Use "🏷️ Discounts" quick filter
2. View current discounts
3. Check discount dates
4. Ask: "Items with >20% discount?"
5. Review discount impact
6. Export for promotion tracking
```

### 📈 Inventory Reporting Workflow

```
1. Click "Analytics" tab
2. Gather key metrics
3. Ask multiple questions
4. Build report from answers
5. Use Query History
6. Export all results as CSVs
7. Compile in spreadsheet
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Submit question |
| Ctrl+A | Select all text |
| Ctrl+C | Copy selected |
| Ctrl+V | Paste |

---

## Accessibility Features

**Built-in support for:**
- 🔍 High contrast text
- 📱 Mobile responsive
- ♿ Screen reader friendly
- 🎨 Color-blind friendly design

---

## FAQ - Features

**Q: Can I modify data?**
A: No, only read-only queries are allowed for safety.

**Q: How far back is history?**
A: Last 20 queries are stored in current session.

**Q: Can I export to other formats?**
A: Currently CSV only. More formats coming soon!

**Q: Is my data secure?**
A: Yes! No modification possible, input validated, API key protected.

**Q: Can I share results?**
A: Export CSV and share, or use History to recreate.

**Q: Do questions have character limits?**
A: No practical limit, but more specific = better results.

---

**Ready to explore? Start with a Quick Filter or Example Question! 🚀**
