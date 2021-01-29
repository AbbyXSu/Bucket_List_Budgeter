import re
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
        return redirect(url_for('home', users=new_user.first_name))
        
    return render_template('register.html', title ='Register',form =form)

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = db.session.query(Users).filter (Users.Username == form.username.data)
        if result and result.first().Username == form.username.data:
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
    posts = read_bucket_list(request_user)

    if request.method == 'GET':
        #need a different method here which makes a view. return a render template
        return get_bucket_list( posts=posts, form = form, user=request_user)

    if request.method == 'POST':
        return create_bucket_list(form, posts)

def read_bucket_list(user = None):
    #this method should get the bucketlist from db
    posts = db.session.query(TodoList).filter (TodoList.Username == user).all()
    list_todoItms = posts[0].todoitem_collection if posts else []

    return list_todoItms

def get_bucket_list( posts, form, user = None):
    if not posts:
        flash('Start your day by creating your first Bucket List here!')
        return render_template('bucketList.html', title ='My_Bucket_List', posts = posts, form = form)
    else:
        return render_template('bucketList.html', title ='My_Bucket_List', posts = posts, form = form)

def create_bucket_list(form, posts):
    try:
        if request.form:
            new_item = TodoItem(
            Todo_items_Order = form.Item_priority.data,
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
        return redirect(url_for('bucketList'), title ='My_Bucket_List', form = form, posts = posts)
        
    return render_template('bucketList.html', title ='My_Bucket_List', posts = posts, form = form)

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')