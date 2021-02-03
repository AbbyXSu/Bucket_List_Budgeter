from operator import add
from typing import AsyncContextManager
from src.app import add_budgetActivity_to_Ledger, balance_calculator, format_action_type, performance_calculator
from flask import url_for
from ..data_access import TodoList, db, app, Base, Users, TodoItem, Ledger, BudgetSummary, get_user
from _pytest import monkeypatch
import pytest
from unittest.mock import patch, MagicMock


def test_format_action_type_Deposit():
    logs = [Ledger(Action_ID=1)]
    expected_result = Ledger(Action_ID='Deposit')

    actual_result = format_action_type(logs)[0]
    assert actual_result.Action_ID == expected_result.Action_ID


def test_format_action_type_withdrawal():
    logs = [Ledger(Action_ID=2)]
    expected_result = Ledger(Action_ID='Withdrawal')
    actual_result = format_action_type(logs)[0]
    assert actual_result.Action_ID == expected_result.Action_ID


def test_format_action_type_invalid_action_type():
    logs = [Ledger(Action_ID=7)]
    expected_result = Ledger(Action_ID='Action Type not found')
    actual_result = format_action_type(logs)[0]
    assert actual_result.Action_ID == expected_result.Action_ID


def test_format_action_type_no_action_type():
    logs = [Ledger(Action_ID=None)]
    expected_result = Ledger(Action_ID='Action Type not found')
    actual_result = format_action_type(logs)[0]
    assert actual_result.Action_ID == expected_result.Action_ID


def test_balance_calculator_1_add():
    logs = [Ledger(Action_ID=1, Value_in_GBP=1)]
    expected_result = 1.00
    actual_result = balance_calculator(logs)
    assert actual_result == expected_result


def test_balance_calculator_2_sub():
    logs = [Ledger(Action_ID=2, Value_in_GBP=1)]
    expected_result = -1.00
    actual_result = balance_calculator(logs)
    assert actual_result == expected_result


def test_balance_calculator_1_add2items():
    logs = [
        Ledger(Action_ID=1, Value_in_GBP=1),
        Ledger(Action_ID=1, Value_in_GBP=1)
    ]
    expected_result = 2.00
    actual_result = balance_calculator(logs)
    assert actual_result == expected_result


def test_balance_calculator_add_sub_add2items():
    logs = [
        Ledger(Action_ID=1, Value_in_GBP=3),
        Ledger(Action_ID=2, Value_in_GBP=1)
    ]
    expected_result = 2.00
    actual_result = balance_calculator(logs)
    assert actual_result == expected_result


def test_balance_calculator_None():
    logs = [Ledger(Action_ID=None, Value_in_GBP=None)]
    expected_result = 0
    actual_result = balance_calculator(logs)
    assert actual_result == expected_result


def test_balance_calculator_empty_list():
    logs = []
    expected_result = 0
    actual_result = balance_calculator(logs)
    assert actual_result == expected_result


def test_performance_calculator_empty():
    logs = []
    todo_items = []
    expected_diff = 0
    excepted_percenatge = 0
    expected_total_costs = 0
    actual_diff, actual_percentage, actal_total_costs = performance_calculator(
        todo_items, logs)
    assert actual_diff == expected_diff
    assert actual_percentage == excepted_percenatge
    assert actal_total_costs == expected_total_costs


def test_performance_calculator_single_todoitem():
    logs = [Ledger(Action_ID=1, Value_in_GBP=2)]
    todo_items = [TodoItem(Costs=4)]
    expected_diff = -2
    excepted_percenatge = 50
    expected_total_costs = 4
    actual_diff, actual_percentage, actal_total_costs = performance_calculator(
        todo_items, logs)
    assert actual_diff == expected_diff
    assert actual_percentage == excepted_percenatge
    assert actal_total_costs == expected_total_costs


def test_performance_calculator_single_todoitem_minus():
    logs = [Ledger(Action_ID=2, Value_in_GBP=4)]
    todo_items = [TodoItem(Costs=4)]
    expected_diff = -8
    excepted_percenatge = -100
    expected_total_costs = 4
    actual_diff, actual_percentage, actal_total_costs = performance_calculator(
        todo_items, logs)
    assert actual_diff == expected_diff
    assert actual_percentage == excepted_percenatge
    assert actal_total_costs == expected_total_costs

# 3 Steps of testing via pytest
# Arrange ( via monkey patch)
# Act (call the method under test)
# Assert - assert the result is what we expected


def test_home_with_username():
    
    pass

def test_home_with_none_username():
    pass
