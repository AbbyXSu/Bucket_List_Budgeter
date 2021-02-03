from operator import add, and_, sub
import operator
import re
from types import MethodDescriptorType
from flask import Flask, redirect, render_template, request, flash
from flask.helpers import url_for
from flask_wtf import form
from sqlalchemy.orm import query, sessionmaker
from werkzeug.utils import html
from .user import RegistrationForm, LoginForm, TodoItemForm, TodoListForm, LedgerForm
import sqlalchemy.exc as dberr
from .data_access import TodoList, db, app, Base, Users, TodoItem, Ledger, BudgetSummary

#---------------------------------------------------------homepage/login/register----------------------------------------------------------------------------------------#


@app.route("/")
@app.route('/home')
def home():
    current_user = get_user(request)
    return render_template('home.html', users=current_user, first_name=request.args.get('first_name'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if not form.validate_on_submit():
        return render_template('register.html', title='Register', form=form)
    try:
        new_user = create_user(form)
    except dberr.IntegrityError:
        flash(f'Account has already been created, try again!')
        return render_template('register.html', title='Register', form=form)

    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('home', first_name=new_user.first_name, users=new_user.Username))


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    result = validate_login(form)
    if result and result.first() and result.first().Username == form.username.data:
        flash('You have been logged in!', 'success')
        return redirect(url_for('home', users=result.first().Username, first_name=result.first().first_name))
    else:
        flash('Login Unsuccessful. Please check username', 'danger')
        return render_template('login.html', title='Login', form=form)


def create_user(form):
    new_user = Users(
    Username=form.username.data,
    first_name=form.first_name.data,
    last_name=form.last_name.data)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def validate_login(form):
    if form.validate_on_submit():
        result = db.session.query(Users).filter(
        Users.Username == form.username.data)
        db.session.commit()
        return result

def get_user(request):
    current_user = request.args.get(
        'users') if request and request.args else None
    return current_user


#----------------------------------------------------------Bucket Items_CRUD---------------------------------------------------------------------------------------#


@app.route('/bucketList', methods=['GET', 'POST'])
def bucketList():
    request_user = get_user(request)
    if not request_user:
        flash('You do not have an account yet!, Create one!')
        return redirect(url_for('home'))
    form = TodoItemForm()
    new_item: TodoItem = None
    posts, todoListId = read_bucket_list(request_user)

    if request.method == 'GET':
        return get_bucket_list(posts, form, user=request_user, list_id=todoListId)

    if request.method == 'POST':
        posts, todoListId = read_bucket_list(request_user)
        list_id = create_bucket_list(request_user)
        item_id = add_todoItem_to_list(list_id, form)
        return redirect(url_for('bucketList', title='My_Bucket_List', posts=posts, form=form, bucketListId=str(list_id), users=request_user))

@app.route('/bucketList/<id>/item', methods=['GET', 'POST'])
def create_bucket_item(id):
    form = TodoItemForm(request.form)
    request_user = get_user (request)
    if not request_user:
        flash('You do not have an account yet!, Create one!')
        return redirect(url_for('home'))
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(
                f'Item created for {form.Title.data}! in the Bucket List', 'success')
            new_item_id = add_todoItem_to_list(id, form)
            posts = read_bucket_list(request_user)
            return redirect(url_for('bucketList', users=request_user))
        else:
            return render_template('createItem.html', title='My_Bucket_List', form=form, bucketList_id=str(id), users=request_user)
    if request.method == 'GET':
        return render_template('createItem.html', title='Create_My_Bucket_Item', bucketList_id=str(id), users=request_user, form=form)


@app.route('/bucketList/<id>/item/<itemId>', methods=['GET', 'POST'])
def bucket_list_item(id, itemId):
    if request.method == 'GET':
        chosenItem = chosen_item(id, itemId)
        form = TodoItemForm(request.form)
        prepopulated_item(id, itemId,form)
        return render_template('updateItem.html', title=f'update {chosenItem.Title}', form=form, id=id, itemId=itemId)
    if request.method == 'POST':
        form = TodoItemForm(request.form)
        user = get_user_with_TodoListID(id)
        update_item(id, itemId, form)
        return redirect(url_for('bucketList', users=user))


@app.route('/bucketList/<id>/item/<itemId>/delete', methods=['GET'])
def delete_bucket_list_item(id, itemId):
    deleting_item(id, itemId)
    user = get_user_with_TodoListID(id)
    return redirect(url_for('bucketList', id=id, itemId=itemId, users=user))


#---------------------------------------------------------------------------------(DB_querry_function_only)-----------------------------------------------------------------# 
def update_item(id, itemId, form):
    chosenItem = chosen_item(id, itemId,)
    chosenItem.Todo_items_Order = form.Item_priority.data
    chosenItem.Title = form.Title.data
    chosenItem.Description = form.Description.data
    chosenItem.Costs = form.Costs.data
    db.session.commit()
    return None

def prepopulated_item(id, itemId,form):   
    chosenItem = chosen_item(id, itemId)
    form.Item_priority.data = chosenItem.Todo_items_Order
    form.Title.data = chosenItem.Title
    form.Description.data = chosenItem.Description
    form.Costs.data = chosenItem.Costs
    return form.Item_priority.data, form.Title.data, form.Description.data, form.Costs.data

def chosen_item(id, itemId):
    chosenItem = db.session.query(TodoItem).filter_by(Id=itemId, Todo_List_ID=id).first()
    db.session.commit()
    return chosenItem

def deleting_item(id, itemId):
    deleteItem = db.session.query(TodoItem).filter_by(Id=itemId, Todo_List_ID=id).first()
    db.session.delete(deleteItem)
    db.session.commit()
    return deleteItem
    

def get_user_with_TodoListID(id):
    user = db.session.query(TodoList).filter_by(Todo_List_ID=id).first().Username
    db.session.commit()
    return user

#------------------------------------------------------------Bucket_List-------------------------------------------------------------------------------------#

def read_bucket_list(user=None):
    posts = db.session.query(TodoList).filter(TodoList.Username == user).all()
    db.session.commit()
    list_todoItms = list(posts[0].todoitem_collection) if posts and len(
        posts) > 0 else []
    todoListId = posts[0].Todo_List_ID if posts != [] else None
    return list_todoItms, todoListId


def get_bucket_list(posts, form, user=None, list_id=None):
    if not posts:
        flash('Start your day by creating your first Bucket List here!')
        if not list_id:
            return render_template('createItem.html', title='Create_My_Bucket_Item', users=user, form=form)
        else:
            return redirect(url_for('create_bucket_item', users=user, id=list_id))
    else:
        return render_template('bucketList.html', title='My_Bucket_List', posts=posts, form=form, bucketList_id=str(list_id), users=user)

#---------------------------------------------------------------------------------(DB_querry_function_only)-----------------------------------------------------------------# 
def create_bucket_list(user):
    newList = TodoList(Username=user)
    db.session.add(newList)
    db.session.commit()
    return newList.Todo_List_ID


def add_todoItem_to_list(listId, form=None):
    # code to add a todoItem
    if form:
        new_item = TodoItem(
            Todo_items_Order=form.Item_priority.data,
            Todo_List_ID=listId,
            Title=form.Title.data,
            Description=form.Description.data,
            Costs=form.Costs.data)
        db.session.add(new_item)
        db.session.commit()
        return new_item.Id
    return None

#-------------------------------------------------------------Budget_Summary/Ledger------------------------------------------------------------------------------------#


@app.route('/budgetSummary', methods=['GET', 'POST'])
def budgetSummary():
    request_user = get_user (request)
    if not request_user:
        flash('You do not have an account yet!, Create one!')
        return redirect(url_for('home'))
    form = LedgerForm(request.form)
    logs, budgeter_ID = read_budgetLedger(request_user)
    balance = balance_calculator(logs)
    list_todoItms, _ = read_bucket_list(request_user)
    diff, percentage, _ = performance_calculator(list_todoItms, logs)
    if request.method == 'GET':
        return get_budgetLedger(logs, form, user=request_user, budgeter_ID=budgeter_ID, balance=balance, percentage=round(percentage, 2), diff=diff)

    if request.method == 'POST':
        list_todoItms, _ = read_bucket_list(request_user)
        diff, percentage, _ = performance_calculator(list_todoItms, logs)
        budgeter_ID = create_budgetlog(request_user)
        balance = balance_calculator(logs)
        add_budgetActivity_to_Ledger(budgeter_ID, form)
        logs, _ = read_budgetLedger(request_user)
        return render_template('budgetSummary.html', title='My_Saving Journey', logs=logs, budgeter_ID=str(budgeter_ID), balance = balance, users=request_user, diff = diff, percentage=round(percentage, 2))


def read_budgetLedger(user=None):
    logs = db.session.query(BudgetSummary).filter(
        BudgetSummary.Username == user).all()
    db.session.commit()
    cashflow = list(
        logs[0].ledger_collection if logs and len(logs) > 0 else [])
    budgeter_ID = logs[0].Budgeter_Id if logs != [] else None
    return cashflow, budgeter_ID


def get_budgetLedger(logs, form, user=None, budgeter_ID=None, balance=0.00, percentage=None, diff=None):
    format_action_type(logs)
    if not logs:
        flash('Start your Saving journey here!')
        if not budgeter_ID:
            return render_template('budgetAction.html', title='Create_saving_Action', users=user, form=form)
        else:
            return redirect(url_for('budgetAction', id=budgeter_ID, users=user))
    else:
        return render_template('budgetSummary.html', title='My_Savings_journey', logs=logs, form=form, budgeter_ID=budgeter_ID, users=user, balance=balance, percentage=percentage, diff=diff)


def create_budgetlog(user):
    newlog = BudgetSummary(Username=user)
    db.session.add(newlog)
    db.session.commit()
    return newlog.Budgeter_Id


def add_budgetActivity_to_Ledger(budgeter_ID, form=None):
    if form:
        newActivity = Ledger(Value_in_GBP=form.Value_in_GBP.data,Budgeter_ID=budgeter_ID, Action_ID=form.Action_log.data)
        db.session.add(newActivity)
        db.session.commit()
        return newActivity.event_id
    return None


@app.route('/budgetSummary/<id>/item', methods=['GET', 'POST'])
def budgetAction(id):
    form = LedgerForm(request.form)
    request_user = get_user (request)
    if not request_user:
        flash('You do not have an account yet!, Create one!')
        return redirect(url_for('home'))
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('One step closer to your target' 'success')
            add_budgetActivity_to_Ledger(id, form)
            logs, _ = read_budgetLedger(request_user)
            balance = balance_calculator(logs)
            update_balance(id, balance)
            return redirect(url_for('budgetSummary', users=request_user))
        else:
            return render_template('budgetAction.html', title='Add_to_your_Savings', form=form, budgeter_ID=id, users=request_user)

    if request.method == 'GET':
        return render_template('budgetAction.html', title='Add_to_your_Savings', form=form, budgeter_ID=id, users=request_user)


def update_balance(id, balance):
    to_update = db.session.query(
        BudgetSummary).filter_by(Budgeter_Id=id).first()
    to_update.Balance = balance
    db.session.commit()


def format_action_type(logs, user=None):  # pytest done
    action_id_converter = {
        1: 'Deposit',
        2: 'Withdrawal'
    }
    for log in logs:
        action = action_id_converter.get(
            log.Action_ID, 'Action Type not found')
        log.Action_ID = action
    return logs


def balance_calculator(logs):         # pytest done
    action_operator_converter = {
        1: add,
        2: sub,
        'Deposit': add,
        'Withdrawal': sub
    }
    balance = 0.00
    for log in logs:
        amount = log.Value_in_GBP if log.Value_in_GBP else 0
        operation = action_operator_converter.get(log.Action_ID)
        if not operation:
            continue
        balance = operation(balance, amount)
    return balance


def performance_calculator(list_todoItms, logs):   # pytest done
    total_costs = 0.00
    for item in list_todoItms:
        total_costs += item.Costs
    balance = balance_calculator(logs)
    diff = balance - total_costs
    percentage = (balance/total_costs)*100 if total_costs > 0 else 0
    return diff, percentage, total_costs

#-----------------------------------------------------------My_Account--------------------------------------------------------------------------------------#


@app.route('/myAccount')
def my_account():
    request_user = get_user (request)
    list_todoItms, _ = read_bucket_list(request_user)
    logs, _ = read_budgetLedger(request_user)
    numberofBucketItems = number_of_bucketItems(request_user)
    balance = balance_calculator(logs)
    diff, percentage, total_costs = performance_calculator(list_todoItms, logs)
    return render_template('myAccount.html', users=request_user, balance=balance, diff=diff, percentage=round(percentage, 2), numberofBucketItems=numberofBucketItems, total_costs=total_costs, logs=logs)


def number_of_bucketItems(request_user):
    _, todoListId = read_bucket_list(request_user)
    numberofBucketItems = db.session.query(TodoItem).filter_by(Todo_List_ID=todoListId).count()
    return numberofBucketItems


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
