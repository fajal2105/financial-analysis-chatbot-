"""Runs test queries against the chatbot and writes test_results.txt"""
from financial_chatbot import simple_chatbot

# (description, query, substrings that must appear in the answer)
TESTS = [
    ("Q1 total revenue, named year", "What is Apple's total revenue in 2025?", ["416,161"]),
    ("Q1 default year = latest", "What is the total revenue of Microsoft?", ["FY2025", "281,724"]),
    ("Q2 change vs last year", "How has Tesla's net income changed over the last year?", ["7,091", "3,794", "-46.5%", "decreased"]),
    ("Q2 change between two years", "How did Microsoft's revenue change from 2023 to 2025?", ["211,915", "281,724", "+32.9%", "increased"]),
    ("Q2 change, single year given", "How did Apple's net income change in 2024?", ["96,995", "93,736", "-3.4%"]),
    ("Q3 highest across companies", "Which company had the highest net income in 2025?", ["Apple had the highest", "112,010"]),
    ("Q3 lowest across companies", "Which company had the lowest total liabilities in 2024?", ["Tesla had the lowest", "48,390"]),
    ("Q4 assets and liabilities", "What are Apple's total assets and liabilities?", ["359,241", "285,508", "79.5%"]),
    ("Q4 liabilities, named year", "Microsoft total liabilities 2023", ["205,753"]),
    ("Q5 operating cash flow", "What is Tesla's operating cash flow in 2024?", ["14,923"]),
    ("Two companies at once", "Compare Apple and Tesla revenue in 2025", ["416,161", "94,827"]),
    ("Case-insensitive input", "WHAT IS TESLA'S TOTAL REVENUE IN 2023", ["96,773"]),
    ("No company named -> all three", "What is the total revenue?", ["Showing all three", "Apple", "Microsoft", "Tesla"]),
    ("Unknown company handled", "What is Google's revenue?", ["only", "Showing all three"]),
    ("Year outside data", "What was Apple's revenue in 2030?", ["2023 to 2025"]),
    ("No earlier year available", "How did Apple's revenue change in 2023?", ["FY2022"]),
    ("Unsupported topic", "What is the weather today?", ["Sorry, I can only provide"]),
    ("Help command", "help", ["Example questions"]),
]

lines, passed = [], 0
for i, (desc, query, expected) in enumerate(TESTS, 1):
    answer = simple_chatbot(query)
    ok = all(e in answer for e in expected)
    passed += ok
    lines.append(f"Test {i:02d} [{'PASS' if ok else 'FAIL'}] {desc}")
    lines.append(f"  Query : {query}")
    lines.append("  Answer: " + answer.replace("\n", "\n          "))
    if not ok:
        lines.append(f"  Missing: {[e for e in expected if e not in answer]}")
    lines.append("")
summary = f"RESULT: {passed}/{len(TESTS)} tests passed"
lines.append(summary)
open("test_results.txt", "w").write("\n".join(lines))
print(summary)
