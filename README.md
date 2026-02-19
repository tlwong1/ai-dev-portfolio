# AI-Assisted Expense Tracker

A Python expense tracking module built to demonstrate AI-assisted software development practices, including AI-generated test suites and documented human-AI workflows.

## What It Does

A set of Python functions for tracking personal expenses — adding expenses, filtering by category, calculating totals, and generating summaries.

## Project Structure

```
ai-dev-portfolio/
├── expenses.py        # Core expense tracking logic
├── test_expenses.py   # AI-generated pytest test suite
└── README.md
```

## How to Run

**Run the tests:**
```
python -m pytest test_expenses.py -v
```

**Expected output:** 25 passed in ~0.05s

## AI-Assisted Development

This project demonstrates real-world AI-assisted development practices:

**AI-Generated Test Suite**
`test_expenses.py` was generated using Claude AI (claude.ai). The prompt asked for full pytest coverage including normal cases, edge cases, and error handling across all five functions. The generated tests were reviewed manually, validated for correctness, and run against the codebase before being committed.

**Results:**
- 25 tests generated covering all functions
- 100% pass rate on first run
- Coverage includes empty inputs, floating point precision, negative values, and edge cases like tied amounts

**Tools Used:**
- Claude AI (Anthropic) — test generation
- GitHub Copilot — in-editor autocomplete assistance
- pytest — test framework

**My Role:**
I wrote the core logic in `expenses.py`, reviewed and validated all AI-generated tests for correctness, and manually verified that each test was testing the right behavior before pushing to GitHub.

## Skills Demonstrated

- Python functions and data structures
- AI-assisted test generation and validation
- Git version control and GitHub workflow
- pytest testing framework
