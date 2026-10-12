# Financial Chatbot Prototype (Task 2)

A simple rule-based chatbot that answers predefined financial questions about **Apple, Microsoft and Tesla** using the data extracted and analysed in Task 1 (`financials.csv`).

- Data: fiscal years 2023 to 2025, all amounts in **USD millions** (Total Revenue, Net Income, Total Assets, Total Liabilities, Operating Cash Flow).
- Each company uses its own fiscal year (Microsoft ends June, Apple ends September, Tesla ends December).
- Tesla net income is "net income attributable to common stockholders".

## How it works
1. `pandas` loads `financials.csv` once at start-up.
2. The user's question is lower-cased, then the script detects three things with simple keyword and regex matching: the **company** (Apple, Microsoft, Tesla), the **fiscal year** (a four-digit number, default = latest year, 2025) and the **metric** (e.g. "revenue", "profit", "cash flow", "assets").
3. An `if / elif / else` chain in `simple_chatbot()` matches the question to one of the predefined query types below, looks the numbers up in the data and builds the answer (including percentage change where relevant).
4. Anything that matches nothing gets a polite fallback message listing what the bot can do.

## Predefined queries
| # | Query type | Example question |
|---|---|---|
| 1 | Total revenue | "What is the total revenue of Apple in 2025?" |
| 2 | Change over the last year (or between two years), for any metric | "How has Tesla's net income changed over the last year?" |
| 3 | Highest / lowest company for a metric | "Which company had the highest net income in 2025?" |
| 4 | Total assets and liabilities (with liabilities-to-assets ratio) | "What are Microsoft's total assets and liabilities?" |
| 5 | Operating cash flow | "What is Tesla's operating cash flow in 2024?" |

Also supported: `help` shows examples, `exit` quits. If no company is named, the bot shows all three. Input is not case-sensitive.

## How to run
```
pip install pandas
python financial_chatbot.py      # interactive chat in the terminal
python test_chatbot.py           # runs the tests and writes test_results.txt
```

## Testing
`test_chatbot.py` runs 18 test questions (all five query types, two companies at once, upper-case input, no company named, unknown company, year outside the data, no earlier year available, off-topic question, help). Result: **18/18 passed**. Full questions and answers are in `test_results.txt`.

## Limitations
- **Rule-based, not AI:** it understands only keywords. Unusual phrasing, typos (e.g. "revnue") or questions with several metrics at once may fail or give only the first metric found.
- **Very small dataset:** 3 companies, 3 fiscal years, 5 metrics. It cannot answer about other companies, ratios beyond liabilities-to-assets, segments, or forecasts.
- **Fiscal years are not aligned:** "2025" means a different 12-month period for each company, so cross-company comparisons are approximate.
- **No context memory:** each question is handled on its own, so follow-ups like "and for Tesla?" do not work.
- **Unknown company names are not detected:** if the question names a company it does not know (e.g. Google), it says it only covers three companies and shows all three.
- **Data accuracy depends on manual extraction** from the 10-K filings.

## Possible improvements
Use an LLM or an NLP library for intent detection (so free-form questions work), add conversation memory, connect to live filing data (e.g. SEC EDGAR), and build a simple Flask or chat web interface.
