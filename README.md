# AI-Assisted Expense Tracker

A Python expense tracking module built to demonstrate AI-assisted software development practices, including AI-generated test suites and documented human-AI workflows.

## What It Does

A set of Python functions for tracking personal expenses — adding expenses, filtering by category, calculating totals, generating summaries, grouping by month, and reading/writing CSV files.

## Project Structure

```
ai-dev-portfolio/
├── expenses.py           # Core expense tracking logic
├── test_expenses.py      # AI-generated pytest test suite
├── sample_expenses.csv   # Sample data to try out the module
└── README.md
```

## Features

- Add expenses with name, amount, category, and date
- Filter expenses by category
- Calculate totals and find the largest expense
- Generate summaries and monthly breakdowns
- Load expenses from a CSV file
- Save expenses to a CSV file

## How to Run

**Run the tests:**
```
python -m pytest test_expenses.py -v
```

**Expected output:** 37 passed in ~0.09s

**Try it with sample data:**
```python
from expenses import load_expenses_from_csv, summary, monthly_summary

expenses = load_expenses_from_csv("sample_expenses.csv")
print(summary(expenses))
print(monthly_summary(expenses))
```

## AI-Assisted Development

This project demonstrates real-world AI-assisted development practices:

**AI-Generated Test Suite**
`test_expenses.py` was generated using Claude AI (claude.ai). The prompt asked for full pytest coverage including normal cases, edge cases, and error handling across all functions. The generated tests were reviewed manually, validated for correctness, and run against the codebase before being committed.

**Results:**
- 37 tests generated covering all 8 functions
- 100% pass rate on first run
- Coverage includes empty inputs, floating point precision, negative values, CSV roundtrip, edge cases like tied amounts, and real file I/O

**Tools Used:**
- Claude AI (Anthropic) — test generation and code review
- GitHub Copilot — in-editor autocomplete assistance
- pytest — test framework

**My Role:**
I wrote the core logic in `expenses.py`, reviewed and validated all AI-generated tests for correctness, and manually verified that each test was testing the right behavior before pushing to GitHub.

## Skills Demonstrated

- Python functions, data structures, and the csv module
- AI-assisted test generation and validation
- Git version control and GitHub workflow
- pytest testing framework including fixtures and file I/O testing
