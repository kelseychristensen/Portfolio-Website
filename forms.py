from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, URL

class CreateItemForm(FlaskForm):
    title = StringField("Portfolio Item Title", validators=[DataRequired()])
    img_url = StringField("Portfolio Item Image URL", validators=[DataRequired(), URL()])
    description = StringField("Portfolio Item Description", validators=[DataRequired()])
    github = StringField("Github URL", validators=[DataRequired(), URL()])
    dribbble = StringField("Dribbble URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit New Item")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

class RegistrationForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up")