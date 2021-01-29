from enum import unique
from flask_wtf import FlaskForm
from flask_wtf import validators
from wtforms import StringField
from wtforms.fields.simple import SubmitField, BooleanField
from wtforms.fields import IntegerField,SelectField,FieldList,FormField
from wtforms.validators import DataRequired, length, EqualTo



#create username field, put in validator
class RegistrationForm(FlaskForm):
    username = StringField('username', 
                            validators=[DataRequired(), length(min=2, max=20)])
    first_name =StringField('first_name',
                            validators=[DataRequired(), length(min=2,max=20)])
    last_name = StringField('last_name',
                            validators =[DataRequired(), length(min=2,max =20)])
    submit =SubmitField ('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('username', 
                            validators=[DataRequired(), length(min=2, max=20)])
    remember = BooleanField ('Remember Me')
    Submit =SubmitField ('Login')

class TodoItemForm(FlaskForm):
    Itm_priority = IntegerField('', 
                            validators=[DataRequired(), length(max=1), unique])
    Title =StringField('title', 
                            validators=[DataRequired(), length(min=2, max=50)])
    Description = StringField('title', 
                            validators=[DataRequired(), length(min=2, max=50)])
    Costs = IntegerField('', 
                            validators=[DataRequired()])
    Submit =SubmitField ('Submit')

class TodoListForm(FlaskForm):
    AllItems = FieldList (FormField(TodoItemForm),min_entries=0)
    Delete = BooleanField('Delete')
    Update = BooleanField('Update')

class LedgerForm(FlaskForm):
    action_options= [('1', 'Deposit'), ('2', 'Withdrawal')]
    Action_log = SelectField('Action', 
                            validators=[DataRequired()], choices=action_options)
    Value_in_GBP =IntegerField('', 
                            validators=[DataRequired()])
    Submit =SubmitField ('Submit')

