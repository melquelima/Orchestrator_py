from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    userName = StringField("userName",validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])
    remember = BooleanField("remember")