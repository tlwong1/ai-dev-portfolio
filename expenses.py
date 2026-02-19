import csv
from datetime import datetime


def add_expense(expenses, name, amount, category, date=None):
    """Add a new expense to the list. Date defaults to today if not provided."""
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")
    expense = {"name": name, "amount": float(amount), "category": category, "date": date}
    expenses.append(expense)
    return expenses


def total_expenses(expenses):
    """Return the total sum of all expense amounts."""
    return sum(e["amount"] for e in expenses)


def filter_by_category(expenses, category):
    """Return a list of expenses matching the given category."""
    return [e for e in expenses if e["category"] == category]


def largest_expense(expenses):
    """Return the single largest expense, or None if the list is empty."""
    if not expenses:
        return None
    return max(expenses, key=lambda e: e["amount"])


def summary(expenses):
    """Return a summary dict with total, count, and largest expense."""
    return {
        "total": total_expenses(expenses),
        "count": len(expenses),
        "largest": largest_expense(expenses),
    }


def monthly_summary(expenses):
    """Return a dict of {YYYY-MM: total} grouping expenses by month."""
    totals = {}
    for e in expenses:
        month = e["date"][:7]  # "YYYY-MM"
        totals[month] = totals.get(month, 0) + e["amount"]
    return totals


def save_expenses_to_csv(expenses, filepath):
    """Save the expenses list to a CSV file."""
    fieldnames = ["name", "amount", "category", "date"]
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)


def load_expenses_from_csv(filepath):
    """Load expenses from a CSV file and return as a list of dicts."""
    expenses = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["amount"] = float(row["amount"])
            expenses.append(row)
    return expenses