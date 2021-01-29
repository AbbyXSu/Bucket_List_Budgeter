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
    return render_template ('home.html', users=current_user)

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
        return redirect(url_for('home', users=new_user.first_name))
        
    return render_template('register.html', title ='Register',form =form)

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'username':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username', 'danger')
    return render_template('login.html', title ='Login',form =form)
#---------------------------------------------------------------------------------------------------#
# @app.route('/bucketList', methods=['GET','POST'])
# def bucketList():
#     form = TodoItemForm()
#     new_item: TodoItem = None
#     #headings is used to create the table view column headers
#     headings=('Priority','Title','Description','Costs','Created_on','Last_update')
#     #posts= [dict(details = form.AllItems(i)) for i in TodoItem.query.all()]
#     #making a form to make a new bucketlist 
#     # (i.e. submit a collection of todo items & generate a list)
#     #user specific todo list

#     #on get -> return a bucketlist view 
#     # (can create lists and/or display given state)
#     # filter by 
#     #on post -> read from request form 
#     # & generate a todolist entity + insert all provided todo items
#     # if invalid, return the validation errors
#     posts= [dict(details = form.AllItems(i)) for i in db.session.query(TodoItem).all()]
#     try:
#         if request.form:
#             new_item = TodoItem(
#             Todo_items_Order = form.Itm_priority.data,
#             Title = form.Title.data,
#             Description = form.Description.data,
#             Costs = form.Costs.data)
#             db.session.add(new_item)
#             db.session.commit()

#     except dberr.IntegrityError:
#             flash(f'Item with the same priority has already been created, try again!')
#             return render_template('bucketList.html', title ='My_Bucket_List',form =form)

#     if form.validate_on_submit():
#         flash(f'Item created for {form.Title.data}! in the Bucket List', 'success')
#         return redirect(url_for('bucketList'),headings =headings, title ='My_Bucket_List',form =form, posts = posts)
        
#     return render_template('bucketList.html', headings =headings, title ='My_Bucket_List',posts = posts,form =form)


@app.route('/bucketList', methods=['GET','POST'])
def bucketList():
    """
    HTTP Request handler for /bucketlist resource.
    Returns forms for viewing & managing bucketlist & todo items
    """

    request_user = request.args.get('user') if request.args else None
    form = TodoItemForm()
    new_item: TodoItem = None
    #headings is used to create the table view column headers
    headings=('Priority','Title','Description','Costs','Created_on','Last_update')
    #posts = [dict(details = form.AllItems(i)) for i in db.session.query(TodoItem).all()]
    posts = _read_bucket_list(request_user)

    if request.method == 'GET':
        return _get_bucket_list(headings, posts, form, user=request_user)

    if request.method == 'POST':
        return _create_bucket_list(form, headings, posts)


def _read_bucket_list(user = None):
    """
    reads the bucketlist and todo items from db, matching user
    """
    posts = db.session.query(TodoList).all()
    todo_list = posts[0].todoitem_collection

    return todo_list

def _get_bucket_list(headings, posts, form, user = None):
    """
    on get -> return a bucketlist view 
    (can create lists and/or display given state)
    filter by user
    """
    #get bucketlists matching given username. If user not supplied, what to do?
    return render_template('bucketList.html', headings =headings, title ='My_Bucket_List', posts = posts, form = None)


def _create_bucket_list(form, headings, posts):
    """
    on post -> read from request form 
    & generate a todolist entity + insert all provided todo items
    if invalid, return the validation errors
    """
    try:
        if request.form:
            new_item = TodoItem(
            Todo_items_Order = form.Itm_priority.data,
            Title = form.Title.data,
            Description = form.Description.data,
            Costs = form.Costs.data)
            db.session.add(new_item)
            db.session.commit()

    except dberr.IntegrityError:
            flash(f'Item with the same priority has already been created, try again!')
            return render_template('bucketList.html', title ='My_Bucket_List',form =form)

    if form.validate_on_submit():
        flash(f'Item created for {form.Title.data}! in the Bucket List', 'success')
        return redirect(url_for('bucketList'),headings =headings, title ='My_Bucket_List', form = form, posts = posts)
        
    return render_template('bucketList.html', headings =headings, title ='My_Bucket_List', posts = posts, form = form)


@app.route('/update', methods=['GET','POST'])
def update():
    headings=('Priority','Title','Description','Costs','Created_on','Last_update')
    posts = TodoItem.query.all
    db.session.commit()
    return redirect (url_for('bucketList'),headings=headings, posts = posts)

# @app.route("/delete/<id>", methods=["POST"])
# def delete():

#     DeleteItem = TodoItem.query.filter_by(TodoList.Todo_List_ID=1).first()
#     db.session.delete(DeleteItem)
#     db.session.commit()
#     return redirect("/bucketList")

#--------------------------------------------------------------------------------------------------------------------------#




if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')