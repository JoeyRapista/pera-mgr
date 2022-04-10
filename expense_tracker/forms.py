from tokenize import String
from wtforms import StringField, SubmitField, PasswordField, SelectField,DecimalField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired
from wtforms.widgets import TextArea 
from flask_wtf import FlaskForm

categories = ["Income","Food", "Housing", "Utilities", "Household items", "Transportion", "Medical/Health", "Insurance", "Kids", "Pets", "Subscriptions",
				"Clothing", "Personal Care", "Personal Development", "Financial/Professional Fees", "Recreation/Fun", "Travel", "Technology", "Gifts", "Charitable Giving",
				"Savings Goals/Investing", "Debt Payments"]

class LoginForm(FlaskForm): 
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()]) 
	submit = SubmitField("Login")

class RegisterForm(FlaskForm): 
	email = EmailField("Email", validators=[DataRequired()])
	username = StringField("Username", validators=[DataRequired(), Length(min=6, max=30)])
	password = PasswordField("Password", validators=[InputRequired(),Length(min=6, max=30), EqualTo('confirm', message="Password must match")] ) 
	confirm = PasswordField("Confirm password")  
	submit = SubmitField("Register")
 
class TransactionForm(FlaskForm):  
	category = SelectField("Category", 	choices = categories, validators=[DataRequired()])
	description = StringField("Description", widget=TextArea(), validators=[DataRequired()]) 
	date = StringField("Date", validators=[DataRequired()]) 
	amount = DecimalField("Amount", validators=[DataRequired()]) 
	submit = SubmitField("Add Transaction")

class AccountForm(FlaskForm): 
	username = StringField("Username", validators=[DataRequired(), Length(min=6, max=30)]) 
	email = EmailField("Email", validators=[DataRequired()]) 
	first_name = StringField("First Name") 
	last_name = StringField("Last Name")  
	submit = SubmitField("Update profile")

class ChangePasswordForm(FlaskForm): 
	password = PasswordField("Current password", validators=[DataRequired()])  
	new_password = PasswordField("New password", validators=[InputRequired(),Length(min=6, max=30), EqualTo('confirm', message="Password must match, Please try again.")] ) 
	confirm = PasswordField("Confirm password")  
	submit = SubmitField("Update")

class PieFormDaily(FlaskForm):
	date = StringField("Select date", validators=[DataRequired()])
	submit = SubmitField("Check")

class PieFormMonthly(FlaskForm):
	date = StringField("Select month", validators=[DataRequired()])
	submit = SubmitField("Check")

class BarFormMonthly(FlaskForm):
	date_start = StringField("Select start  month", validators=[DataRequired()])
	date_end = StringField("Select end month", validators=[DataRequired()])
	submit = SubmitField("Check")  