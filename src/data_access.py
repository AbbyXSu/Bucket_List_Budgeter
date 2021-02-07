from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.base import Connection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, engine


app = Flask(__name__)
#read these from environment variables
app.config['SECRET_KEY'] = '88dd6a6854b7f1901b7f01d353186c6a'
#app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://BLBAPP:abby@DESKTOP-4K1BGVB/BLB_DB?driver=SQL+Server"
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://BLBAPP:abby@192.168.1.18,1434/BLB_DB?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

Users = Base.classes.Users
TodoItem = Base.classes.TodoItem
Ledger = Base.classes.Ledger
TodoList = Base.classes.TodoList
BudgetSummary = Base.classes.BudgetSummary


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


def update_item(id, itemId, form):
    chosenItem = chosen_item(id, itemId,)
    chosenItem.Todo_items_Order = form.Item_priority.data
    chosenItem.Title = form.Title.data
    chosenItem.Description = form.Description.data
    chosenItem.Costs = form.Costs.data
    db.session.commit()
    return None


def prepopulated_item(id, itemId, form):
    chosenItem = chosen_item(id, itemId)
    form.Item_priority.data = chosenItem.Todo_items_Order
    form.Title.data = chosenItem.Title
    form.Description.data = chosenItem.Description
    form.Costs.data = chosenItem.Costs
    return form.Item_priority.data, form.Title.data, form.Description.data, form.Costs.data


def chosen_item(id, itemId):
    chosenItem = db.session.query(TodoItem).filter_by(
        Id=itemId, Todo_List_ID=id).first()
    db.session.commit()
    return chosenItem


def deleting_item(id, itemId):
    deleteItem = db.session.query(TodoItem).filter_by(
        Id=itemId, Todo_List_ID=id).first()
    db.session.delete(deleteItem)
    db.session.commit()
    return deleteItem


def get_user_with_TodoListID(id):
    user = db.session.query(TodoList).filter_by(
        Todo_List_ID=id).first().Username
    db.session.commit()
    return user


def read_bucket_list(user=None):
    posts = db.session.query(TodoList).filter(TodoList.Username == user).all()
    db.session.commit()
    list_todoItms = list(posts[0].todoitem_collection) if posts and len(
        posts) > 0 else []
    todoListId = posts[0].Todo_List_ID if posts != [] else None
    return list_todoItms, todoListId


def create_bucket_list(user):
    newList = TodoList(Username=user)
    db.session.add(newList)
    db.session.commit()
    return newList.Todo_List_ID


def add_todoItem_to_list(listId, form=None):
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


def create_budgetlog(user):
    newlog = BudgetSummary(Username=user)
    db.session.add(newlog)
    db.session.commit()
    return newlog.Budgeter_Id


def add_budgetActivity_to_Ledger(budgeter_ID, form=None):
    if form:
        newActivity = Ledger(Value_in_GBP=form.Value_in_GBP.data,
                             Budgeter_ID=budgeter_ID, Action_ID=form.Action_log.data)
        db.session.add(newActivity)
        db.session.commit()
        return newActivity.event_id
    return None


def read_budgetLedger(user=None):
    logs = db.session.query(BudgetSummary).filter(
        BudgetSummary.Username == user).all()
    db.session.commit()
    cashflow = list(
        logs[0].ledger_collection if logs and len(logs) > 0 else [])
    budgeter_ID = logs[0].Budgeter_Id if logs != [] else None
    return cashflow, budgeter_ID


def update_balance(id, balance):
    to_update = db.session.query(
        BudgetSummary).filter_by(Budgeter_Id=id).first()
    to_update.Balance = balance
    db.session.commit()


def number_of_bucketItems(request_user):
    _, todoListId = read_bucket_list(request_user)
    numberofBucketItems = db.session.query(
        TodoItem).filter_by(Todo_List_ID=todoListId).count()
    return numberofBucketItems

def update_numberOfItem(id,numberofBucketItems):
    to_update = db.session.query(
        TodoList).filter_by(Todo_List_ID=id).first()
    to_update.Number_of_items = numberofBucketItems
    db.session.commit()



if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
