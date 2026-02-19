import csv
import os
import pytest
from expenses import (
    add_expense,
    total_expenses,
    filter_by_category,
    largest_expense,
    summary,
    monthly_summary,
    save_expenses_to_csv,
    load_expenses_from_csv,
)

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def make_expense(name, amount, category, date="2025-01-01"):
    return {"name": name, "amount": float(amount), "category": category, "date": date}


# -------------------------------------------------------------------
# add_expense
# -------------------------------------------------------------------

def test_add_expense_returns_list():
    result = add_expense([], "Lunch", 12.50, "Food")
    assert isinstance(result, list)

def test_add_expense_single_item():
    result = add_expense([], "Lunch", 12.50, "Food", date="2025-01-01")
    assert len(result) == 1
    assert result[0] == {"name": "Lunch", "amount": 12.50, "category": "Food", "date": "2025-01-01"}

def test_add_expense_default_date_is_set():
    result = add_expense([], "Lunch", 12.50, "Food")
    assert "date" in result[0]
    assert len(result[0]["date"]) == 10  # YYYY-MM-DD

def test_add_expense_multiple_items():
    expenses = []
    add_expense(expenses, "Lunch", 12.50, "Food", date="2025-01-01")
    add_expense(expenses, "Bus", 2.75, "Transport", date="2025-01-02")
    assert len(expenses) == 2

def test_add_expense_zero_amount():
    result = add_expense([], "Free sample", 0, "Food", date="2025-01-01")
    assert result[0]["amount"] == 0

def test_add_expense_negative_amount():
    result = add_expense([], "Refund", -5.00, "Food", date="2025-01-01")
    assert result[0]["amount"] == -5.00

def test_add_expense_preserves_existing():
    expenses = [make_expense("Coffee", 3.00, "Food")]
    add_expense(expenses, "Taxi", 15.00, "Transport", date="2025-01-02")
    assert len(expenses) == 2
    assert expenses[0]["name"] == "Coffee"

def test_add_expense_amount_stored_as_float():
    result = add_expense([], "Lunch", "12", "Food", date="2025-01-01")
    assert isinstance(result[0]["amount"], float)


# -------------------------------------------------------------------
# total_expenses
# -------------------------------------------------------------------

def test_total_expenses_empty():
    assert total_expenses([]) == 0

def test_total_expenses_single():
    assert total_expenses([make_expense("Lunch", 12.50, "Food")]) == 12.50

def test_total_expenses_multiple():
    expenses = [
        make_expense("Lunch", 12.50, "Food"),
        make_expense("Bus", 2.50, "Transport"),
        make_expense("Book", 15.00, "Education"),
    ]
    assert total_expenses(expenses) == 30.00

def test_total_expenses_with_zero():
    expenses = [make_expense("Free", 0, "Other"), make_expense("Paid", 10.00, "Food")]
    assert total_expenses(expenses) == 10.00

def test_total_expenses_floating_point():
    expenses = [make_expense("A", 0.1, "Food"), make_expense("B", 0.2, "Food")]
    assert total_expenses(expenses) == pytest.approx(0.3)


# -------------------------------------------------------------------
# filter_by_category
# -------------------------------------------------------------------

def test_filter_by_category_match():
    expenses = [
        make_expense("Lunch", 12.50, "Food"),
        make_expense("Bus", 2.50, "Transport"),
        make_expense("Pizza", 9.00, "Food"),
    ]
    result = filter_by_category(expenses, "Food")
    assert len(result) == 2
    assert all(e["category"] == "Food" for e in result)

def test_filter_by_category_no_match():
    result = filter_by_category([make_expense("Lunch", 12.50, "Food")], "Transport")
    assert result == []

def test_filter_by_category_empty_list():
    assert filter_by_category([], "Food") == []

def test_filter_by_category_case_sensitive():
    result = filter_by_category([make_expense("Lunch", 12.50, "Food")], "food")
    assert result == []

def test_filter_by_category_all_match():
    expenses = [make_expense("Lunch", 12.50, "Food"), make_expense("Pizza", 9.00, "Food")]
    assert len(filter_by_category(expenses, "Food")) == 2


# -------------------------------------------------------------------
# largest_expense
# -------------------------------------------------------------------

def test_largest_expense_empty():
    assert largest_expense([]) is None

def test_largest_expense_single():
    e = make_expense("Lunch", 12.50, "Food")
    assert largest_expense([e]) == e

def test_largest_expense_multiple():
    expenses = [
        make_expense("Lunch", 12.50, "Food"),
        make_expense("Laptop", 999.99, "Tech"),
        make_expense("Bus", 2.50, "Transport"),
    ]
    assert largest_expense(expenses)["name"] == "Laptop"

def test_largest_expense_tie():
    expenses = [make_expense("A", 10.00, "Food"), make_expense("B", 10.00, "Food")]
    assert largest_expense(expenses)["amount"] == 10.00

def test_largest_expense_all_zero():
    expenses = [make_expense("A", 0, "Food"), make_expense("B", 0, "Food")]
    assert largest_expense(expenses)["amount"] == 0


# -------------------------------------------------------------------
# summary
# -------------------------------------------------------------------

def test_summary_empty():
    result = summary([])
    assert result == {"total": 0, "count": 0, "largest": None}

def test_summary_single():
    result = summary([make_expense("Lunch", 12.50, "Food")])
    assert result["total"] == 12.50
    assert result["count"] == 1
    assert result["largest"]["name"] == "Lunch"

def test_summary_multiple():
    expenses = [
        make_expense("Lunch", 12.50, "Food"),
        make_expense("Laptop", 999.99, "Tech"),
        make_expense("Bus", 2.50, "Transport"),
    ]
    result = summary(expenses)
    assert result["total"] == pytest.approx(1014.99)
    assert result["count"] == 3
    assert result["largest"]["name"] == "Laptop"

def test_summary_keys_present():
    assert set(summary([]).keys()) == {"total", "count", "largest"}


# -------------------------------------------------------------------
# monthly_summary
# -------------------------------------------------------------------

def test_monthly_summary_empty():
    assert monthly_summary([]) == {}

def test_monthly_summary_single_month():
    expenses = [
        make_expense("Lunch", 12.50, "Food", date="2025-01-10"),
        make_expense("Bus", 2.50, "Transport", date="2025-01-15"),
    ]
    result = monthly_summary(expenses)
    assert result == {"2025-01": pytest.approx(15.00)}

def test_monthly_summary_multiple_months():
    expenses = [
        make_expense("Lunch", 12.50, "Food", date="2025-01-10"),
        make_expense("Rent", 900.00, "Housing", date="2025-02-01"),
    ]
    result = monthly_summary(expenses)
    assert "2025-01" in result
    assert "2025-02" in result
    assert result["2025-01"] == pytest.approx(12.50)
    assert result["2025-02"] == pytest.approx(900.00)

def test_monthly_summary_groups_correctly():
    expenses = [
        make_expense("A", 10.00, "Food", date="2025-03-01"),
        make_expense("B", 20.00, "Food", date="2025-03-15"),
        make_expense("C", 5.00, "Food", date="2025-04-01"),
    ]
    result = monthly_summary(expenses)
    assert result["2025-03"] == pytest.approx(30.00)
    assert result["2025-04"] == pytest.approx(5.00)


# -------------------------------------------------------------------
# save_expenses_to_csv / load_expenses_from_csv
# -------------------------------------------------------------------

@pytest.fixture
def tmp_csv(tmp_path):
    return str(tmp_path / "test_expenses.csv")

def test_save_creates_file(tmp_csv):
    save_expenses_to_csv([make_expense("Lunch", 12.50, "Food")], tmp_csv)
    assert os.path.exists(tmp_csv)

def test_save_and_load_roundtrip(tmp_csv):
    expenses = [
        make_expense("Lunch", 12.50, "Food", date="2025-01-01"),
        make_expense("Bus", 2.50, "Transport", date="2025-01-02"),
    ]
    save_expenses_to_csv(expenses, tmp_csv)
    loaded = load_expenses_from_csv(tmp_csv)
    assert len(loaded) == 2
    assert loaded[0]["name"] == "Lunch"
    assert loaded[0]["amount"] == pytest.approx(12.50)
    assert loaded[1]["category"] == "Transport"

def test_load_converts_amount_to_float(tmp_csv):
    save_expenses_to_csv([make_expense("Lunch", 12.50, "Food")], tmp_csv)
    loaded = load_expenses_from_csv(tmp_csv)
    assert isinstance(loaded[0]["amount"], float)

def test_save_empty_list(tmp_csv):
    save_expenses_to_csv([], tmp_csv)
    loaded = load_expenses_from_csv(tmp_csv)
    assert loaded == []

def test_load_sample_csv():
    """Load the real sample_expenses.csv included in the project."""
    loaded = load_expenses_from_csv("sample_expenses.csv")
    assert len(loaded) == 10
    assert all("amount" in e for e in loaded)
    assert all(isinstance(e["amount"], float) for e in loaded)

def test_save_csv_has_correct_headers(tmp_csv):
    save_expenses_to_csv([make_expense("Lunch", 12.50, "Food")], tmp_csv)
    with open(tmp_csv, newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)
    assert headers == ["name", "amount", "category", "date"]