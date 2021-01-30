import re
from types import MethodDescriptorType
from flask import Flask, redirect, render_template, request, flash
from flask.helpers import url_for
from sqlalchemy.orm import query,sessionmaker
from .user import RegistrationForm, LoginForm, TodoItemForm,TodoListForm,LedgerForm
import sqlalchemy.exc as dberr
from .conn import TodoList, db, app, Base, Users, TodoItem,Ledger,BudgetSummary,ActionLogType


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
    posts, todoListId = read_bucket_list(request_user)

    if request.method == 'GET':
        #need a different method here which makes a view. return a render template
        return get_bucket_list( posts, form, user=request_user, list_id = todoListId)

    if request.method == 'POST':
        #return create_bucket_item(form, posts,request_user)
        list_id = create_bucket_list(request_user)
        item_id = add_todoItem_to_list(list_id, form)
        return render_template('bucketList.html',  title ='My_Bucket_List', posts = posts, form = form, bucketListId = str(list_id))


@app.route('/bucketList/<id>/item', methods = ['GET','POST'])
def create_bucket_item(form, id):
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
            return render_template('bucketList.html', title ='My_Bucket_List', posts = posts, bucketList_id = str(id), users =request_user)
        else:
            #return the view for invalid
            return render_template('createItem.html', title ='My_Bucket_List', form = form, bucketList_id = str(id), users =request_user)
    if request.method == 'GET':
        #return create item view which links to the given bucketlistId
        return render_template('createItem.html', title ='Create_My_Bucket_Item',bucketList_id = str(id), users =request_user)


@app.route('/bucketList/<id>/item/<itemId>', methods = ['GET','POST'])
def bucket_list_item(id, itemId):
    pass


@app.route('/bucketList/<id>/item/<itemId>/delete', methods = ['GET'])
def delete_bucket_list_item(id, itemId):
    #delete from db
    #redirect to the bucketlist endpoint    
    
    pass


def read_bucket_list(user = None):
    #this method should get the bucketlist from db
    posts = db.session.query(TodoList).filter (TodoList.Username == user).all()
    list_todoItms = posts[0].todoitem_collection if posts and len(posts) > 0 else []
    todoListId = posts[0].Todo_List_ID if posts != [] else None
    return list_todoItms, todoListId

def get_bucket_list( posts, form, user = None, list_id = None):
    if not posts:
        flash('Start your day by creating your first Bucket List here!')
        if not list_id:
            return render_template('createItem.html', title ='Create_My_Bucket_Item', users = user, form = form)
        else:
            return render_template('createItem.html', title ='My_Bucket_List', posts = posts, bucketList_id = str(list_id), users = user, form = form)

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

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')