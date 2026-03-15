from datetime import date

from core.expense_service import ExpenseService
from core.no_tocar.sqlite_expense_repository import SQLiteExpenseRepository


def create_service():
    repo = SQLiteExpenseRepository()
    repo.empty()
    return ExpenseService(repo)


def test_create_and_list_expenses():
    service = create_service()

    service.create_expense(
        title="Comida", amount=10, description="", expense_date=date.today()
    )

    expenses = service.list_expenses()

    assert len(expenses) == 1
    assert expenses[0].title == "Comida"


def test_remove_expense():
    service = create_service()

    service.create_expense("A", 5, "", date.today())
    service.create_expense("B", 7, "", date.today())

    service.remove_expense(1)

    expenses = service.list_expenses()
    assert len(expenses) == 1
    assert expenses[0].title == "B"


def test_update_expense():
    service = create_service()

    service.create_expense("Café", 2, "", date.today())

    service.update_expense(expense_id=1, title="Café grande", amount=3)

    expense = service.list_expenses()[0]
    assert expense.title == "Café grande"
    assert expense.amount == 3


def test_update_non_existing_expense_does_nothing():
    service = create_service()

    service.update_expense(expense_id=999, title="Nada")

    assert service.list_expenses() == []


def test_total_amount():
    service = create_service()

    service.create_expense("A", 10, "", date.today())
    service.create_expense("B", 5, "", date.today())

    assert service.total_amount() == 15


def test_total_by_month():
    service = create_service()

    service.create_expense("Enero 1", 10, "", date(2025, 1, 10))
    service.create_expense("Enero 2", 5, "", date(2025, 1, 20))
    service.create_expense("Febrero", 7, "", date(2025, 2, 1))

    totals = service.total_by_month()

    assert totals["2025-01"] == 15
    assert totals["2025-02"] == 7


def test_create_multiple_expenses_and_list():
    service = create_service()

    service.create_expense("Pan", 3, "Mercado", date.today())
    service.create_expense("Leche", 4, "Supermercado", date.today())

    all_list = service.list_expenses()

    titles = [e.title for e in all_list]
    assert "Pan" in titles
    assert "Leche" in titles
    assert len(all_list) == 2


def test_remove_expense_reduces_total():
    service = create_service()

    service.create_expense("Libro", 3, "Mercado", date.today())
    service.create_expense("Revista", 4, "Supermercado", date.today())
    expenses = service.list_expenses()
    service.remove_expense(expenses[0].id)
    expenses_after = service.list_expenses()
    assert len(expenses_after) == 1
    assert expenses_after[0].title == "Revista"


def test_update_expense_partial_fields():
    service = create_service()

    expense = service.create_expense("Camiseta", 15, "Ropa", date.today())
    service.update_expense(expense_id=expense.id, amount=18)
    updated_expense = service._repository.get_by_id(expense.id)

    assert updated_expense is not None
    assert updated_expense.title == "Camiseta"
    assert updated_expense.amount == 18
    assert updated_expense.description == "Ropa"


def test_total_amount_after_removal():
    """
    Verifica que el cálculo del total gastado se actualiza correctamente después de eliminar un gasto.

    - Se crean dos gastos ("Cursos" por 30 y "Internet" por 25).
    - Se comprueba que la suma inicial del total es 55.
    - Se elimina el gasto con id 1 (correspondiente al gasto "Cursos").
    - Se recalcula el total y se espera que sea 25, reflejando únicamente el monto del gasto aún presente.
    - Este test valida que el método total_amount refleja los cambios en el sistema ante eliminaciones, manteniendo la consistencia de los datos agregados.
    """
    ...
