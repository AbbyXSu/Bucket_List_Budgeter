from operator import and_
import re
from types import MethodDescriptorType
from flask import Flask, redirect, render_template, request, flash
from flask.helpers import url_for
from flask_wtf import form
from sqlalchemy.orm import query,sessionmaker
from werkzeug.utils import html
from .user import RegistrationForm, LoginForm, TodoItemForm,TodoListForm,LedgerForm
import sqlalchemy.exc as dberr
from .conn import TodoList, db, app, Base, Users, TodoItem,Ledger,BudgetSummary


@app.route("/")
@app.route('/home')
def home():
    current_user = request.args.get('users') if request and request.args else None
    return render_template ('home.html', users=current_user,first_name =request.args.get('first_name'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    new_user: Users = None
    try:
        if request.form:
            new_user = Users(
            Username = form.username.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data)
            db.session.add(new_user)
            db.session.commit()

    except dberr.IntegrityError:
            flash(f'Account has already been created, try again!')
            return render_template('register.html', title ='Register',form =form)

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home', first_name=new_user.first_name, users=new_user.Username))
        
    return render_template('register.html', title ='Register',form =form)

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = db.session.query(Users).filter (Users.Username == form.username.data)
        if result and result.first() and result.first().Username == form.username.data:
            flash('You have been logged in!', 'success')
            return redirect(url_for('home',users =result.first().Username, first_name =result.first().first_name))
        else:
            flash('Login Unsuccessful. Please check username', 'danger')
            return render_template('login.html', title ='Login',form =form)
    return render_template('login.html', title ='Login',form =form)
#---------------------------------------------------------------------------------------------------#

@app.route('/bucketList', methods=['GET','POST'])
def bucketList():
    request_user = request.args.get('users') if request.args else None
    if not request_user:
        flash('You do not have an account yet!, Create one!')
        return redirect(url_for('home'))
    form = TodoItemForm()
    new_item: TodoItem = None
    posts,todoListId = read_bucket_list(request_user)

    if request.method == 'GET':
        #need a different method here which makes a view. return a render template
        return get_bucket_list( posts, form, user=request_user, list_id = todoListId)

    if request.method == 'POST':
        #return create_bucket_item(form, posts,request_user)
        list_id = create_bucket_list(request_user)
        item_id = add_todoItem_to_list(list_id, form)
        return render_template('bucketList.html',  title ='My_Bucket_List', posts = posts, form = form, bucketListId = str(list_id),users =request_user)


@app.route('/bucketList/<id>/item', methods = ['GET','POST'])
def create_bucket_item(id):
    form = TodoItemForm(request.form)
    request_user = request.args.get('users') if request.args else None
    if not request_user:
        flash('You do not have an account yet!, Create one!')
        return redirect(url_for('home'))
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(f'Item created for {form.Title.data}! in the Bucket List', 'success')
            #add the new item
            new_item_id = add_todoItem_to_list(id, form)
            #read the list
            posts = read_bucket_list(request_user)
            #return the bucketlist table view
            #return render_template('bucketList.html', title ='My_Bucket_List', posts = posts, bucketList_id = str(id), users = request_user)
            return redirect(url_for('bucketList', users=request_user))
        else:
            #return the view for invalid
            return render_template('createItem.html', title ='My_Bucket_List', form = form, bucketList_id = str(id), users = request_user)
    if request.method == 'GET':
        #return create item view which links to the given bucketlistId
        return render_template('createItem.html', title ='Create_My_Bucket_Item',bucketList_id = str(id), users = request_user, form = form)


@app.route('/bucketList/<id>/item/<itemId>', methods = ['GET','POST'])
def bucket_list_item(id, itemId):
    #if get, return the edit form populated with this item
    if request.method == 'GET':
        chosenItem = db.session.query(TodoItem).filter_by(Id = itemId, Todo_List_ID =id).first()
        form = TodoItemForm()
        form.Item_priority.data = chosenItem.Todo_items_Order
        form.Title.data = chosenItem.Title
        form.Description.data = chosenItem.Description
        form.Costs.data = chosenItem.Costs
        return render_template('updateItem.html', title =f'update {chosenItem.Title}',form =form,id = id, itemId =itemId)
    if request.method == 'POST':
        form = TodoItemForm(request.form)
        chosenItem = db.session.query(TodoItem).filter_by(Id = itemId, Todo_List_ID =id).first()
        chosenItem.Todo_items_Order = form.Item_priority.data
        chosenItem.Title = form.Title.data
        chosenItem.Description = form.Description.data
        chosenItem.Costs = form.Costs.data
        db.session.commit()
        user = db.session.query(TodoList).filter_by(Todo_List_ID = id).first().Username
        return redirect(url_for('bucketList', users=user))
    #if post, apply update to the todo item and then redirect to bucketlist page


@app.route('/bucketList/<id>/item/<itemId>/delete', methods = ['GET'])
def delete_bucket_list_item(id, itemId):
    #delete from db
    #redirect to the bucketlist endpoint  
    deleteItem = db.session.query(TodoItem).filter_by(Id = itemId, Todo_List_ID =id).first() 
    db.session.delete(deleteItem)
    db.session.commit()
    user = db.session.query(TodoList).filter_by(Todo_List_ID = id).first().Username
    return redirect(url_for('bucketList', id = id, itemId =itemId, users=user))


def read_bucket_list(user = None):
    #this method should get the bucketlist from db
    posts = db.session.query(TodoList).filter (TodoList.Username == user).all()
    list_todoItms = list(posts[0].todoitem_collection) if posts and len(posts) > 0 else []
    todoListId = posts[0].Todo_List_ID if posts != [] else None
    return list_todoItms, todoListId

def get_bucket_list( posts, form, user = None, list_id = None):
    if not posts:
        flash('Start your day by creating your first Bucket List here!')
        if not list_id:
            return render_template('createItem.html', title ='Create_My_Bucket_Item', users = user, form = form)
        else:
            #return render_template('createItem.html', title ='My_Bucket_List', posts = posts, bucketList_id = str(list_id), users = user, form = form)
            return redirect(url_for('create_bucket_item', users = user, id = list_id))

        #in the CreateItem.html, for bucketListId = NONE, make the form submission url hook back to POST /bucketList
        #if the bucketlistid is given, make the view link to the /bucketList/{id}/item
    else:
        return render_template('bucketList.html', title ='My_Bucket_List', posts = posts, form = form, bucketList_id = str(list_id), users=user)

#-------------------------------------------------------------------------------------------------------------------------------------#
def create_bucket_list (user):
    """ 
    returns newly created bucket list ID 
    """
    #Equivalent SQL Statement: insert into todoList (Username) VALUES (user) returning created.todoListId
    newList = TodoList(Username=user)
    db.session.add(newList) #look up how to get sqlalchemy to return the id of created item
    db.session.commit()
    #>> CODE HERE WHICH CREATES BUCKETLIST AND RETURNS THE CREATED ID     #>> CODE HERE TO return the created list id as a number
    return newList.Todo_List_ID

def add_todoItem_to_list(listId, form = None):
    #code to add a todoItem
    if form:
        new_item = TodoItem(
        Todo_items_Order = form.Item_priority.data,
        Todo_List_ID = listId,
        Title = form.Title.data,
        Description = form.Description.data,
        Costs = form.Costs.data)
        db.session.add(new_item)
        db.session.commit()
        return new_item.Id
    return None

#------------------------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/budgetSummary', methods = ['GET','POST'])
def budgetSummary():
    request_user = request.args.get('users') if request.args else None
    if not request_user:
        flash('You do not have an account yet!, Create one!')
        return redirect(url_for('home'))
    form = LedgerForm(request.form)
    logs,budgeter_ID = read_budgetLedger (request_user)

    if request.method == 'GET':
        return get_budgetLedger(logs, form, user = request_user, budgeter_ID = budgeter_ID)

    if request.method =='POST':
        budgeter_ID = create_budgetlog(request_user)
        event_id = add_budgetActivity_to_Ledger (budgeter_ID,form)
        return render_template ('budgetSummary.html', title ='My_Saving Journey', logs=logs, budgeter_ID =str( budgeter_ID), users = request_user)


def read_budgetLedger(user=None):
    logs = db.session.query(BudgetSummary).filter(BudgetSummary.Username == user).all()
    cashflow= list(logs[0].ledger_collection if logs and len(logs)>0 else [])
    budgeter_ID = logs[0].Budgeter_Id if logs !=[] else None
    return cashflow, budgeter_ID
    
def get_budgetLedger(logs,form,user = None, budgeter_ID = None):
    if not logs:
        flash('Start your Saving journey here!')
        if not budgeter_ID:
            return render_template ('budgetAction.html', title ='Create_saving_Action', users = user, form = form)
        else:
            #this needs to redirect to an action, not an html file
            return redirect(url_for('budgetAction', id =  budgeter_ID, users = user))
    else:
        return render_template ('budgetSummary.html',title ='My_Savings_journey', logs = logs ,form = form,budgeter_ID=budgeter_ID, users =user)

def create_budgetlog (user):
    #newlog = Ledger(Username = user)
    newlog = BudgetSummary(Username = user)
    db.session.add(newlog)
    db.session.commit()
    return newlog.Budgeter_Id

def add_budgetActivity_to_Ledger(budgeter_ID,form = None):
    if form:
        newActivity= Ledger(Value_in_GBP = form.Value_in_GBP.data, Budgeter_ID = budgeter_ID, Action_ID = form.Action_log.data)
        db.session.add(newActivity)
        db.session.commit()
        return newActivity.event_id
    return None



@app.route ('/budgetSummary/<id>/item', methods =['GET','POST'])
def budgetAction(id):
    form = LedgerForm(request.form)
    request_user = request.args.get('users') if request.args else None
    if not request_user:
        flash('You do not have an account yet!, Create one!')
        return redirect(url_for('home'))
    if  request.method == 'POST':
        if form.validate_on_submit():
            flash('One step closer to your target' 'success')
            new_event_id = add_budgetActivity_to_Ledger(id,form)
            logs = read_budgetLedger(request_user)
            return redirect(url_for('budgetSummary', users=request_user))
        else:
            return render_template ('budgetAction.html', title = 'Add_to_your_Savings', form = form, budgeter_ID = id, users = request_user)
        
    if request.method == 'GET':
            return render_template ('budgetAction.html', title = 'Add_to_your_Savings', form = form, budgeter_ID = id, users = request_user)




if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')