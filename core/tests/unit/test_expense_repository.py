from datetime import date

from core.expense import Expense
from core.in_memory_expense_repository import InMemoryExpenseRepository


def create_expense(id=1, title="Test", amount=10):
    return Expense(
        id=id, title=title, amount=amount, description="", expense_date=date.today()
    )


def test_save_new_expense():
    repo = InMemoryExpenseRepository()
    expense = create_expense()
    repo.save(expense)
    expenses = repo.list_all()
    assert len(expenses) == 1
    assert expenses[0].id == 1


def test_save_updates_existing_expense():
    repo = InMemoryExpenseRepository()
    expense = create_expense()

    repo.save(expense)

    updated = create_expense(id=1, title="Updated", amount=20)
    repo.save(updated)

    expenses = repo.list_all()
    assert len(expenses) == 1
    assert expenses[0].title == "Updated"
    assert expenses[0].amount == 20


def test_remove_expense():
    repo = InMemoryExpenseRepository()
    expense = create_expense()
    repo.save(expense)
    repo.remove(expense_id=1)
    assert repo.list_all() == []


def test_list_all_returns_copy():
    repo = InMemoryExpenseRepository()
    repo.save(create_expense())
    expenses = repo.list_all()
    expenses.clear()
    assert len(repo.list_all()) == 1


def test_get_by_id_returns_expense():
    repo = InMemoryExpenseRepository()
    expense = create_expense()
    repo.save(expense)
    get_expense = repo.get_by_id(expense_id=1)
    # assert get_expense == expense
    assert get_expense is not None
    assert get_expense.id == expense.id
    assert get_expense.title == expense.title
    assert get_expense.amount == expense.amount
    assert get_expense.description == expense.description
    assert get_expense.expense_date == expense.expense_date


def test_get_by_id_returns_none_if_not_found():
    repo = InMemoryExpenseRepository()
    expense = create_expense()
    repo.save(expense)
    get_expense = repo.get_by_id(expense_id=2)
    assert get_expense is None
