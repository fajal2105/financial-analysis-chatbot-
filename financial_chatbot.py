"""
Financial chatbot prototype (BCG X GenAI Job Simulation, Task 2)

Answers a small set of predefined financial queries about Apple, Microsoft and
Tesla using the data extracted and analysed in Task 1 (financials.csv).
All amounts are in USD millions. Fiscal years 2023 to 2025.

Run:  python financial_chatbot.py
"""
import re
import pandas as pd

DATA_FILE = "financials.csv"

df = pd.read_csv(DATA_FILE)
COMPANIES = sorted(df["Company"].unique())      # Apple, Microsoft, Tesla
YEARS = sorted(int(y) for y in df["Fiscal Year"].unique())   # 2023, 2024, 2025
LATEST = YEARS[-1]

# Words a user might type  ->  column in the data (checked in this order)
METRICS = {
    "Operating Cash Flow": ["cash flow", "operating cash", "cash from operations"],
    "Total Revenue": ["revenue", "sales", "turnover"],
    "Net Income": ["net income", "profit", "earnings"],
    "Total Assets": ["asset"],
    "Total Liabilities": ["liabilit", "debt"],
}

CHANGE_WORDS = ["change", "grow", "increase", "decrease", "last year",
                "year over year", "year-over-year", "yoy", "trend",
                "went up", "went down"]
HIGH_WORDS = {"highest", "largest", "biggest", "most", "top", "best", "greatest"}
LOW_WORDS = {"lowest", "smallest", "least", "worst"}

HELP_TEXT = (
    "Example questions I can answer (Apple, Microsoft, Tesla; fiscal years "
    f"{YEARS[0]}-{LATEST}; USD millions):\n"
    "  1. What is the total revenue of Apple in 2025?\n"
    "  2. How has Tesla's net income changed over the last year?\n"
    "  3. Which company had the highest net income in 2025?\n"
    "  4. What are Microsoft's total assets and liabilities?\n"
    "  5. What is Tesla's operating cash flow in 2024?\n"
    "Tip: if you don't name a company I show all three; if you don't name a "
    f"year I use the latest ({LATEST})."
)

FALLBACK_TEXT = (
    "Sorry, I can only provide information on total revenue, net income, total "
    "assets, total liabilities and operating cash flow for Apple, Microsoft and "
    "Tesla. Type 'help' to see example questions."
)


# ---------------------------------------------------------------- helpers
def money(x):
    return f"${x:,.0f} million (${x / 1000:,.1f} billion)"


def get_value(company, year, metric):
    row = df[(df["Company"] == company) & (df["Fiscal Year"] == year)]
    return float(row[metric].iloc[0])


def find_companies(q):
    return [c for c in COMPANIES if c.lower() in q]


def find_years(q):
    return [int(y) for y in re.findall(r"\b(20\d{2})\b", q)]


def find_metric(q):
    for metric, words in METRICS.items():
        if any(w in q for w in words):
            return metric
    return None


def ranking_direction(q):
    tokens = set(re.findall(r"[a-z]+", q))
    if tokens & HIGH_WORDS:
        return "highest"
    if tokens & LOW_WORDS:
        return "lowest"
    return None


# ---------------------------------------------------------------- chatbot
def simple_chatbot(user_query):
    """Match the user's question to one of the predefined queries (if/elif)."""
    q = user_query.lower().strip()
    companies = find_companies(q)
    years = find_years(q)
    metric = find_metric(q)
    direction = ranking_direction(q)
    is_change = any(w in q for w in CHANGE_WORDS)

    note = ""
    if not companies:
        note = (f"I have data for {', '.join(COMPANIES[:-1])} and {COMPANIES[-1]} "
                "only. Showing all three:\n")
        target_companies = COMPANIES
    else:
        target_companies = companies

    if q in ("help", "menu", "?", "what can you do", "hi", "hello"):
        return HELP_TEXT

    elif any(y not in YEARS for y in years):
        return f"I only have data for fiscal years {YEARS[0]} to {LATEST}."

    # Query 3: ranking across companies
    elif direction and metric:
        year = years[0] if years else LATEST
        values = {c: get_value(c, year, metric) for c in COMPANIES}
        ordered = sorted(values.items(), key=lambda kv: kv[1],
                         reverse=(direction == "highest"))
        top, top_value = ordered[0]
        everyone = "; ".join(f"{c} {money(v)}" for c, v in ordered)
        return (f"In FY{year}, {top} had the {direction} {metric.lower()}: "
                f"{money(top_value)}.\nAll companies: {everyone}.")

    # Query 2: change versus the previous year (or between two given years)
    elif metric and is_change:
        if len(years) >= 2:
            y1, y2 = sorted(years)[:2]
        else:
            y2 = years[0] if years else LATEST
            y1 = y2 - 1
        if y1 not in YEARS:
            return (f"I don't have FY{y1} data, so I can't calculate the change "
                    f"for FY{y2}. Try a period within {YEARS[0]} to {LATEST}.")
        lines = []
        for c in target_companies:
            a, b = get_value(c, y1, metric), get_value(c, y2, metric)
            pct = (b - a) / a * 100
            verb = "increased" if b > a else "decreased"
            lines.append(f"{c}'s {metric.lower()} {verb} from {money(a)} in FY{y1} "
                         f"to {money(b)} in FY{y2} ({pct:+.1f}%).")
        return note + "\n".join(lines)

    # Query 4: assets and liabilities (balance sheet snapshot)
    elif metric in ("Total Assets", "Total Liabilities"):
        year = years[0] if years else LATEST
        lines = []
        for c in target_companies:
            assets = get_value(c, year, "Total Assets")
            liabilities = get_value(c, year, "Total Liabilities")
            lines.append(f"{c} (FY{year}): total assets {money(assets)}, total "
                         f"liabilities {money(liabilities)}. Liabilities are "
                         f"{liabilities / assets * 100:.1f}% of assets.")
        return note + "\n".join(lines)

    # Queries 1 and 5 (and net income): a single value
    elif metric:
        year = years[0] if years else LATEST
        lines = [f"{c}'s {metric.lower()} in FY{year} was "
                 f"{money(get_value(c, year, metric))}." for c in target_companies]
        return note + "\n".join(lines)

    else:
        return FALLBACK_TEXT


def main():
    print("Financial chatbot prototype. Data: Apple, Microsoft, Tesla, "
          f"FY{YEARS[0]}-FY{LATEST} (USD millions).")
    print("Type 'help' for example questions or 'exit' to quit.")
    while True:
        try:
            user_query = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_query.strip().lower() in ("exit", "quit", "bye"):
            print("Bot: Goodbye!")
            break
        if not user_query.strip():
            continue
        print("Bot:", simple_chatbot(user_query))


if __name__ == "__main__":
    main()
