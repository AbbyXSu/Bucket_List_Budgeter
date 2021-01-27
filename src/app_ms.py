from flask import Flask, redirect, render_template, request, flash
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import query,sessionmaker
from .user import RegistrationForm, LoginForm
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, engine
import sqlalchemy.exc as dberr

app = Flask(__name__)
app.config['SECRET_KEY']='88dd6a6854b7f1901b7f01d353186c6a'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://BLBAPP:abby@DESKTOP-4K1BGVB/BLB_DB?driver=SQL+Server"
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare (db.engine, reflect =True)

Users =Base.classes.Users

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

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')