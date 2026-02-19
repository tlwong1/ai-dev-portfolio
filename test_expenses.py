import pytest
from expenses import (
    add_expense,
    total_expenses,
    filter_by_category,
    largest_expense,
    summary,
)

# -------------------------------------------------------------------
# add_expense
# -------------------------------------------------------------------

def test_add_expense_returns_list():
    expenses = []
    result = add_expense(expenses, "Lunch", 12.50, "Food")
    assert isinstance(result, list)

def test_add_expense_single_item():
    expenses = []
    result = add_expense(expenses, "Lunch", 12.50, "Food")
    assert len(result) == 1
    assert result[0] == {"name": "Lunch", "amount": 12.50, "category": "Food"}

def test_add_expense_multiple_items():
    expenses = []
    add_expense(expenses, "Lunch", 12.50, "Food")
    add_expense(expenses, "Bus", 2.75, "Transport")
    assert len(expenses) == 2

def test_add_expense_zero_amount():
    expenses = []
    result = add_expense(expenses, "Free sample", 0, "Food")
    assert result[0]["amount"] == 0

def test_add_expense_negative_amount():
    """Negative amounts (e.g. refunds) are stored as-is."""
    expenses = []
    result = add_expense(expenses, "Refund", -5.00, "Food")
    assert result[0]["amount"] == -5.00

def test_add_expense_preserves_existing():
    expenses = [{"name": "Coffee", "amount": 3.00, "category": "Food"}]
    add_expense(expenses, "Taxi", 15.00, "Transport")
    assert len(expenses) == 2
    assert expenses[0]["name"] == "Coffee"


# -------------------------------------------------------------------
# total_expenses
# -------------------------------------------------------------------

def test_total_expenses_empty():
    assert total_expenses([]) == 0

def test_total_expenses_single():
    expenses = [{"name": "Lunch", "amount": 12.50, "category": "Food"}]
    assert total_expenses(expenses) == 12.50

def test_total_expenses_multiple():
    expenses = [
        {"name": "Lunch", "amount": 12.50, "category": "Food"},
        {"name": "Bus",   "amount":  2.50, "category": "Transport"},
        {"name": "Book",  "amount": 15.00, "category": "Education"},
    ]
    assert total_expenses(expenses) == 30.00

def test_total_expenses_with_zero():
    expenses = [
        {"name": "Free", "amount": 0,     "category": "Other"},
        {"name": "paid", "amount": 10.00, "category": "Food"},
    ]
    assert total_expenses(expenses) == 10.00

def test_total_expenses_floating_point():
    expenses = [
        {"name": "A", "amount": 0.1, "category": "Food"},
        {"name": "B", "amount": 0.2, "category": "Food"},
    ]
    assert total_expenses(expenses) == pytest.approx(0.3)


# -------------------------------------------------------------------
# filter_by_category
# -------------------------------------------------------------------

def test_filter_by_category_match():
    expenses = [
        {"name": "Lunch", "amount": 12.50, "category": "Food"},
        {"name": "Bus",   "amount":  2.50, "category": "Transport"},
        {"name": "Pizza", "amount":  9.00, "category": "Food"},
    ]
    result = filter_by_category(expenses, "Food")
    assert len(result) == 2
    assert all(e["category"] == "Food" for e in result)

def test_filter_by_category_no_match():
    expenses = [
        {"name": "Lunch", "amount": 12.50, "category": "Food"},
    ]
    result = filter_by_category(expenses, "Transport")
    assert result == []

def test_filter_by_category_empty_list():
    assert filter_by_category([], "Food") == []

def test_filter_by_category_case_sensitive():
    expenses = [{"name": "Lunch", "amount": 12.50, "category": "Food"}]
    result = filter_by_category(expenses, "food")
    assert result == []

def test_filter_by_category_all_match():
    expenses = [
        {"name": "Lunch", "amount": 12.50, "category": "Food"},
        {"name": "Pizza", "amount":  9.00, "category": "Food"},
    ]
    result = filter_by_category(expenses, "Food")
    assert len(result) == 2


# -------------------------------------------------------------------
# largest_expense
# -------------------------------------------------------------------

def test_largest_expense_empty():
    assert largest_expense([]) is None

def test_largest_expense_single():
    expenses = [{"name": "Lunch", "amount": 12.50, "category": "Food"}]
    assert largest_expense(expenses) == expenses[0]

def test_largest_expense_multiple():
    expenses = [
        {"name": "Lunch",  "amount": 12.50, "category": "Food"},
        {"name": "Laptop", "amount": 999.99, "category": "Tech"},
        {"name": "Bus",    "amount":   2.50, "category": "Transport"},
    ]
    result = largest_expense(expenses)
    assert result["name"] == "Laptop"
    assert result["amount"] == 999.99

def test_largest_expense_tie():
    """When amounts are equal, one of the tied items is returned."""
    expenses = [
        {"name": "A", "amount": 10.00, "category": "Food"},
        {"name": "B", "amount": 10.00, "category": "Food"},
    ]
    result = largest_expense(expenses)
    assert result["amount"] == 10.00

def test_largest_expense_all_zero():
    expenses = [
        {"name": "A", "amount": 0, "category": "Food"},
        {"name": "B", "amount": 0, "category": "Food"},
    ]
    result = largest_expense(expenses)
    assert result["amount"] == 0


# -------------------------------------------------------------------
# summary
# -------------------------------------------------------------------

def test_summary_empty():
    result = summary([])
    assert result["total"] == 0
    assert result["count"] == 0
    assert result["largest"] is None

def test_summary_single():
    expenses = [{"name": "Lunch", "amount": 12.50, "category": "Food"}]
    result = summary(expenses)
    assert result["total"] == 12.50
    assert result["count"] == 1
    assert result["largest"]["name"] == "Lunch"

def test_summary_multiple():
    expenses = [
        {"name": "Lunch",  "amount": 12.50, "category": "Food"},
        {"name": "Laptop", "amount": 999.99, "category": "Tech"},
        {"name": "Bus",    "amount":   2.50, "category": "Transport"},
    ]
    result = summary(expenses)
    assert result["total"] == pytest.approx(1014.99)
    assert result["count"] == 3
    assert result["largest"]["name"] == "Laptop"

def test_summary_keys_present():
    result = summary([])
    assert "total" in result
    assert "count" in result
    assert "largest" in result
