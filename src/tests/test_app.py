from operator import add
from typing import AsyncContextManager
import json
from flask.testing import FlaskClient
from flask.wrappers import Response
from src.app import *
from flask import url_for
from ..data_access import TodoList, db, app, Base, Users, TodoItem, Ledger, BudgetSummary
from _pytest import monkeypatch
import pytest
from unittest.mock import patch, MagicMock
from .configure_test_app import *
from ..user import *


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


def test_home_with_username(test_client: FlaskClient):
    response = test_client.get("/home?users=TestUsername&first_name='Luke'")
    assert response.status_code == 200
    assert 'Luke' in response.data.decode("utf-8")
    assert 'users=TestUsername' in response.data.decode("utf-8")


def test_home_with_none_user(test_client: FlaskClient):
    response = test_client.get("/home?users=''")
    assert response.status_code == 200
    assert 'there' in response.data.decode("utf-8")
    assert 'users=' in response.data.decode("utf-8")


def test_home_with_no_query(test_client: FlaskClient):
    response = test_client.get("/home")
    assert response.status_code == 200
    assert 'there' in response.data.decode("utf-8")
    assert 'users=' not in response.data.decode("utf-8")


def test_register_get(test_client: FlaskClient):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert 'Join Today' in response.data.decode('utf-8')


def test_register_get_submit(test_client: FlaskClient):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert 'submit' in response.data.decode('utf-8')


def test_register_get_register(test_client: FlaskClient):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert 'register' in response.data.decode('utf-8')


def test_login_get(test_client: FlaskClient):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert 'username' in response.data.decode("utf-8")
    assert 'there' not in response.data.decode("utf-8")


def test_login_get_remeberme(test_client: FlaskClient):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert 'remember' in response.data.decode("utf-8")
    assert 'Login' in response.data.decode("utf-8")


def test_login_get_sign_up(test_client: FlaskClient):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert 'form-check' in response.data.decode("utf-8")
    assert 'Sign Up Here' in response.data.decode("utf-8")


def test_login_get_methods(test_client: FlaskClient):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert 'POST' in response.data.decode("utf-8")
    assert 'next' in response.data.decode("utf-8")


def test_login_get_methods(test_client: FlaskClient):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert 'POST' in response.data.decode("utf-8")
    assert 'next' in response.data.decode("utf-8")


@pytest.fixture()
def db_data_setup():
    student = Users(Username='sniffy13145',
                    first_name='slavoj', last_name='zizek')
    db.session.add(student)
    db.session.commit()

    test_todo_list = TodoList(Username=student.Username, Number_of_items=3)
    db.session.add(test_todo_list)
    db.session.commit()
    test_todo_item_1 = TodoItem(Todo_List_ID=test_todo_list.Todo_List_ID,
                                Todo_items_Order=1, Description='fun', Costs=3, Title='pancake')
    test_todo_item_2 = TodoItem(Todo_List_ID=test_todo_list.Todo_List_ID,
                                Todo_items_Order=2, Description='debate', Costs=4, Title='china')
    test_todo_item_3 = TodoItem(Todo_List_ID=test_todo_list.Todo_List_ID,
                                Todo_items_Order=3, Description='endtime', Costs=5, Title='living')
    db.session.add(test_todo_item_1)
    db.session.add(test_todo_item_2)
    db.session.add(test_todo_item_3)
    db.session.commit()

    test_budgetSummary = BudgetSummary(Username=student.Username, Balance=9)
    db.session.add(test_budgetSummary)
    db.session.commit()

    test_ledger = Ledger(
        Budgeter_ID=test_budgetSummary.Budgeter_Id, Action_ID=1, Value_in_GBP=9)
    db.session.add(test_ledger)
    db.session.commit()
    db.session.flush()

    yield student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger
    # remove / reset the data
    db.session.delete(test_ledger)
    db.session.commit()
    db.session.delete(test_budgetSummary)
    db.session.commit()
    db.session.delete(test_todo_item_3)
    db.session.commit()
    db.session.delete(test_todo_item_2)
    db.session.commit()
    db.session.delete(test_todo_item_1)
    db.session.commit()
    db.session.delete(test_todo_list)
    db.session.commit()
    db.session.delete(student)
    db.session.commit()
    db.session.flush()


def test_bucketList_get_table(test_client: FlaskClient, db_data_setup):
    response = test_client.get("bucketList?users=sniffy13145")
    assert response.status_code == 200
    assert 'Preference' in response.data.decode("utf-8")
    assert 'Title' in response.data.decode("utf-8")


def test_bucketList_get_Description(test_client: FlaskClient, db_data_setup):
    response = test_client.get("bucketList?users=sniffy13145")
    assert response.status_code == 200
    assert 'Description' in response.data.decode("utf-8")
    assert 'Cost' in response.data.decode("utf-8")


def test_bucketList_get_todo_items(test_client: FlaskClient, db_data_setup):
    response = test_client.get("bucketList?users=sniffy13145")
    assert response.status_code == 200
    assert 'china' in response.data.decode("utf-8")
    assert 'fun' in response.data.decode("utf-8")


def test_bucketList_get_action(test_client: FlaskClient, db_data_setup):
    response = test_client.get("bucketList?users=sniffy13145")
    assert response.status_code == 200
    assert 'Delete' in response.data.decode("utf-8")
    assert 'Update' in response.data.decode("utf-8")


def test_get_bucket_list_item(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get(
        f"bucketList/{test_todo_list.Todo_List_ID}/item/{test_todo_item_1.Id}?users=sniffy13145")
    assert response.status_code == 200
    assert 'fun' in response.data.decode("utf-8")
    assert 'pancake' in response.data.decode("utf-8")


def test_get_bucket_list_item_data(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get(
        f"bucketList/{test_todo_list.Todo_List_ID}/item/{test_todo_item_1.Id}?users=sniffy13145")
    assert response.status_code == 200
    assert '1' in response.data.decode("utf-8")
    assert '3' in response.data.decode("utf-8")


def test_delete_bucket_list_item_items(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get(
        f"bucketList/{test_todo_list.Todo_List_ID}/item/{test_todo_item_3.Id}/delete?users=sniffy13145", follow_redirects=True)
    assert response.status_code == 200
    assert 'endtime' not in response.data.decode("utf-8")
    assert 'living' not in response.data.decode("utf-8")


def test_delete_bucket_list_item_numberpfbucketitems(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get(
        f"bucketList/{test_todo_list.Todo_List_ID}/item/{test_todo_item_3.Id}/delete?users=sniffy13145", follow_redirects=True)
    assert response.status_code == 200
    assert '2' in response.data.decode("utf-8")
    assert '1' in response.data.decode("utf-8")


def test_get_bucket_list(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get(
        f"bucketList/{test_todo_list.Todo_List_ID}/item/{test_todo_item_3.Id}/delete?users=sniffy13145", follow_redirects=True)
    assert response.status_code == 200
    assert 'create' not in response.data.decode("utf-8")
    assert 'Bucket_List' in response.data.decode("utf-8")


def test_budgetSummary_balance(test_client: FlaskClient, db_data_setup):
    response = test_client.get("/budgetSummary?users=sniffy13145")
    assert response.status_code == 200
    assert '9' in response.data.decode("utf-8")
    assert 'balance' in response.data.decode("utf-8")


def test_budgetSummary_Action_ID(test_client: FlaskClient, db_data_setup):
    response = test_client.get("/budgetSummary?users=sniffy13145")
    assert response.status_code == 200
    assert 'Deposit' in response.data.decode("utf-8")
    assert '1' in response.data.decode("utf-8")


def test_budgetSummary_Budgeter_Id(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get("/budgetSummary?users=sniffy13145")
    assert response.status_code == 200
    assert str(test_budgetSummary.Budgeter_Id) in response.data.decode("utf-8")


def test_get_budgetLedger(test_client: FlaskClient, db_data_setup):
    response = test_client.get("/budgetSummary?users=sniffy13145")
    assert response.status_code == 200
    assert 'budgetSummary' in response.data.decode("utf-8")
    assert 'budgetAction' not in response.data.decode("utf-8")


def test_get_budgetLedger_title(test_client: FlaskClient, db_data_setup):
    response = test_client.get("/budgetSummary?users=sniffy13145")
    assert response.status_code == 200
    assert 'My_Savings_journey' in response.data.decode("utf-8")
    assert 'Create_saving_Action' not in response.data.decode("utf-8")


def test_budgetSummary_Budgeter_Id(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get(
        f"budgetSummary/{test_budgetSummary.Budgeter_Id}/item", follow_redirects=True)
    assert response.status_code == 200
    assert 'budgetSummary' in response.data.decode("utf-8")
    assert 'Add_to_your_Savings' not in response.data.decode("utf-8")


def test_budgetSummary_Budgeter_Id(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get(
        f"budgetSummary/{test_budgetSummary.Budgeter_Id}/item", follow_redirects=True)
    assert response.status_code == 200
    assert '9' in response.data.decode("utf-8")
    assert str(test_budgetSummary.Budgeter_Id) not in response.data.decode(
        "utf-8")


def test_my_account_diff(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get('/myAccount?users=sniffy13145')
    assert response.status_code == 200
    assert 'myAccount' in response.data.decode("utf-8")
    assert '9' in response.data.decode("utf-8")


def test_get_budgetLedger_none(test_client: FlaskClient, db_data_setup):
    response = get_budgetLedger(logs=None, form=LedgerForm())
    assert 'Action' in response
    assert 'Value/GBP' in response


def test_get_budgetLedger_none_with_not_budget_ID(test_client: FlaskClient, db_data_setup):
    response = get_budgetLedger(
        logs=None, form=LedgerForm(),  budgeter_ID=None)
    assert 'Action' in response
    assert 'id' in response


def test_bucketList_None(test_client: FlaskClient, db_data_setup):
    response = test_client.get("bucketList", follow_redirects=True)
    assert response.status_code == 200
    assert 'there' in response.data.decode("utf-8")
    assert 'Hello' in response.data.decode("utf-8")


def test_create_bucke_item_None(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get(
        f"bucketList/{test_todo_list.Todo_List_ID}/item", follow_redirects=True)
    assert response.status_code == 200
    assert 'there' in response.data.decode("utf-8")
    assert 'Hello' in response.data.decode("utf-8")


def test_budgetsummary_None(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get("budgetSummary", follow_redirects=True)
    assert response.status_code == 200
    assert 'there' in response.data.decode("utf-8")
    assert 'Hello' in response.data.decode("utf-8")


def test_get_bucket_list_noneposts_noid(test_client: FlaskClient, db_data_setup):
    response = get_bucket_list(posts=None, list_id=None, form=TodoItemForm())
    assert 'Create_My_Bucket_Item' in response
    assert 'Preference' in response


def test_get_bucket_list_noneposts(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = get_bucket_list(
        posts=None, form=TodoItemForm(), list_id=test_todo_list.Todo_List_ID)
    assert 'Redirecting' in response.data.decode("utf-8")


def test_budgetAction_get_withuser(test_client: FlaskClient, db_data_setup):
    student, test_todo_list, test_todo_item_1, test_todo_item_2, test_todo_item_3, test_budgetSummary, test_ledger = db_data_setup
    response = test_client.get(
        f"budgetSummary/{test_budgetSummary.Budgeter_Id}/item?users=sniffy13145")
    assert response.status_code == 200
    assert 'Add_to_your_Savings' in response.data.decode("utf-8")
    assert 'Action' in response.data.decode("utf-8")


@pytest.fixture()
def prepare_test_register_post_register():
    user='ThebigOther1314'
    name='slavoj'
    last_name='zizek'
    input_form=dict(username=user, 
                    first_name=name,
                    last_name=last_name,
                    Submit='Sign Up')

    yield input_form, name

    to_delete=db.session.query(Users).filter_by(Username=user).first()
    if to_delete:
        db.session.delete(to_delete)
    db.session.commit()

def test_register_post_register(test_client: FlaskClient, prepare_test_register_post_register):        
    my_form, name = prepare_test_register_post_register
    
    response = test_client.post(url_for('register'), 
                            data=my_form,
                            content_type='application/x-www-form-urlencoded',
                            follow_redirects=True)

    assert response.status_code == 200
    assert name in response.data.decode('utf-8')


