def add_expense(expenses, name, amount, category):
    expense = {"name": name, "amount": amount, "category": category}
    expenses.append(expense)
    return expenses

def total_expenses(expenses):
    return sum(e["amount"] for e in expenses)

def filter_by_category(expenses, category):
    return [e for e in expenses if e["category"] == category]

def largest_expense(expenses):
    if not expenses:
        return None
    return max(expenses, key=lambda e: e["amount"])

def summary(expenses):
    return {
        "total": total_expenses(expenses),
        "count": len(expenses),
        "largest": largest_expense(expenses)
    }