from flask_wtf import FlaskForm
from flask_wtf import validators
from wtforms import StringField
from wtforms.fields.simple import SubmitField, BooleanField
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


