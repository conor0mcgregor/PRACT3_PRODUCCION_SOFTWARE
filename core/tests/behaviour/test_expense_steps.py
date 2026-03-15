from datetime import date
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from core.expense_service import ExpenseService
from core.in_memory_expense_repository import InMemoryExpenseRepository

scenarios("./expense_management.feature")


@pytest.fixture
def context():
    repo = InMemoryExpenseRepository()
    service = ExpenseService(repo)
    return {"service": service, "db": repo}


@given(parsers.parse("un gestor de gastos vacío"))
def empty_manager(context):
    pass


@given(parsers.parse("un gestor con un gasto de {amount:d} euros"))
def manager_with_one_expense(context, amount):
    context["service"].create_expense(
        title="Gasto inicial", amount=amount, description="", expense_date=date.today()
    )


@when(parsers.parse("añado un gasto de {amount:d} euros llamado {title}"))
def add_expense(context, amount, title):
    context["service"].create_expense(
        title=title, amount=amount, description="", expense_date=date.today()
    )


@when(parsers.parse("elimino el gasto con id {expense_id:d}"))
def remove_expense(context, expense_id):
    context["service"].remove_expense(expense_id)


@then(parsers.parse("el total de dinero gastado debe ser {total:d} euros"))
def check_total(context, total):
    assert context["service"].total_amount() == total


def check_month_total(context, month_name, expected_total):
    total_actual = context["totals"].get(month_name, 0)
    assert total_actual == expected_total


@then(parsers.parse("debe haber {expenses:d} gastos registrados"))
def check_expenses_length(context, expenses):
    total = len(context["service"].list_expenses())
    assert expenses == total


@when("trato de agregar un gasto con titulo vacio")
def try_add_empty_title(context):
    try:
        context["service"].create_expense(
            title="", amount=10, description="", expense_date=date.today()
        )
    except Exception as e:
        context["last_error"] = e


@when("trato de agregar un gasto con cantidad negativa")
def try_add_negative_amount(context):
    try:
        context["service"].create_expense(
            title="Test", amount=-5, description="", expense_date=date.today()
        )
    except Exception as e:
        context["last_error"] = e


@then("el gestor debe lanzar un error")
def check_error_thrown(context):
    assert "last_error" in context
    assert context["last_error"] is not None
