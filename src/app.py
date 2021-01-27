from flask import Flask, redirect, render_template, request, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from .user import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY']='814b86ddf016bb20485f4ec09344cdbc'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:password@localhost/usersDB"

db = SQLAlchemy(app)

class users(db.Model):
    username= db.Column(db.String(50), nullable=False, primary_key=True)
    first_name= db.Column(db.String(50), nullable=False)  
    last_name = db.Column(db.String(50), nullable=False)  

db.create_all()
@app.route("/")
@app.route('/home')
def home():
    return render_template ('home.html')

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if request.form:
        new_user = users(
            username = form.username.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data)
        db.session.add(new_user)
        db.session.commit()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title ='Register',form =form)


@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    # if request.form:
    #     new_user = users( username =form.username,first_name = form.first_name,last_name = form.last_name)
    #     db.session.add(new_user)
    #     db.session.commit()
    if form.validate_on_submit():
        if form.username.data == 'username':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title ='Login',form =form)


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')





















# @app.route("/update", methods=["POST"])
# def update():
#     person = users.query.filter_by(name=request.form.get("oldname")).first()
#     person.name = request.form.get("newname")
#     db.session.commit()
#     return redirect("/")

# @app.route("/delete", methods=["POST"])
# def delete():
#     person = users.query.filter_by(name=request.form.get("name")).first()
#     db.session.delete(person)
#     db.session.commit()
#     return redirect("/")

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')