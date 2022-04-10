from email.policy import default
from operator import sub
from time import strftime
from unicodedata import category
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, LoginManager, login_required, logout_user, current_user 
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, date
from sqlalchemy import func, and_, extract

from expense_tracker.models import User, Transaction
from expense_tracker.forms import LoginForm, TransactionForm, RegisterForm, AccountForm, ChangePasswordForm, PieFormMonthly, PieFormDaily, BarFormMonthly
from expense_tracker import app, db 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id)) 
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() 
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Logged in successfully") 
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Wrong Credentials')
        else:
            flash('Wrong credentials')
    return render_template('login.html',form = form)


@app.route('/logout')
@login_required 
def logout():
	logout_user()
	flash("You logged out")
	return redirect(url_for('login'))

@app.route('/profile',methods=['GET', 'POST'])
@login_required
def profile():
    form = AccountForm()
    if form.validate_on_submit():

        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.firstname = form.first_name.data
        current_user.lastname = form.last_name.data

        db.session.add(current_user)
        db.session.commit()
        flash('Profile infos updated')
        return redirect(url_for('home'))   

    form.email.data = current_user.email 
    form.username.data = current_user.username 
    form.first_name.data = current_user.firstname 
    form.last_name.data = current_user.lastname 
    return render_template('profile.html', form=form)

@app.route('/change-password' ,methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.password.data):
            ph = generate_password_hash(form.new_password.data, 'sha256') 
            current_user.password_hash = ph
            db.session.add(current_user)
            db.session.commit()
            flash('Password updated')
            return redirect(url_for('home'))   
        else:
            flash('Invalid password, Please try again.') 
    for error in form.new_password.errors:
        flash(error)
    return render_template('change_password.html', form=form)
 
def generate_labels(transactions_objects, labels):
    for t in transactions_objects:  
            if not t.category == 'Income':
                if not t.category in labels: 
                    labels.append(t.category)
    return labels

def generate_datas(transaction_today_obj, labels, datas):
    for i in labels:
            a = 0.0 
            for j in transaction_today_obj:
                if j.category == i:
                    a = a + j.amount
            datas.append(a)
    return datas
def generate_transactions(transactions_today, transactions):
    for i in transactions_today:
            if not i.category == 'Income':
                t = {'category':i.category, 'amount': i.amount}
                transactions.append(t)  
    return transactions

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def generate_months_labels(start_date, end_date, months_labels):
    for single_date in daterange(start_date, end_date):
        mo = single_date.strftime("%b-%Y")
        if not mo in months_labels:
            months_labels.append(mo)
def generate_months_data(months_labels, transactions_between_month_income, data_income):
    for i in months_labels: 
        total_income = 0.0
        for t in transactions_between_month_income:
            fm = t.date.strftime("%b-%Y")
            if fm == i:
                total_income = total_income + t.amount
        data_income.append(total_income) 
    return data_income 

@app.route('/reports/bar/monthly', methods=['GET', 'POST'])
@login_required
def reports_line_monthly(): 
    form = BarFormMonthly() 
    time_delta = timedelta(days = 30)

    end_date = datetime.now().date() 
    start_date = end_date - time_delta 

    if form.validate_on_submit():
        start_date = datetime.strptime(form.date_start.data, '%Y-%m')  
        end_date = datetime.strptime(form.date_end.data, '%Y-%m')  

    #transactions_between_month_expenses = Transaction.query.filter(and_(func.strftime('%Y-%m', Transaction.date).between(start_date.strftime('%Y-%m'), end_date.strftime('%Y-%m')), Transaction.category != 'Income', Transaction.user_id == current_user.id) ).all()
    
    
    transactions_between_month_expenses = Transaction.query.filter(and_(Transaction.date.between(start_date, end_date), Transaction.category != 'Income', Transaction.user_id == current_user.id) ).all()
    #transactions_today = Transaction.query.filter(and_(extract('year', Transaction.date) == year, extract('month', Transaction.date) == month, Transaction.user_id == current_user.id )).all()
    
    
    #transactions_between_month_income = Transaction.query.filter(and_(func.strftime('%Y-%m', Transaction.date).between(start_date.strftime('%Y-%m'), end_date.strftime('%Y-%m')), Transaction.category == 'Income', Transaction.user_id == current_user.id) ).all()
    transactions_between_month_income = Transaction.query.filter(and_(Transaction.date.between(start_date, end_date), Transaction.category == 'Income', Transaction.user_id == current_user.id) ).all()
    
    
    
    months_labels = []
    generate_months_labels(start_date, end_date, months_labels)
    data_income = []
    generate_months_data(months_labels, transactions_between_month_income, data_income)
    data_expenses = []
    generate_months_data(months_labels, transactions_between_month_expenses, data_expenses) 

    lbl_start = months_labels[0] 
    lbl_end = months_labels[-1]  

    inc_count = len(data_income)
    data = 0.0
    for d in data_income:
        data = data + d
    avg_inc = data/inc_count

    exp_count = len(data_expenses)
    data = 0.0
    for d in data_expenses:
        data = data + d
    avg_exp = data/exp_count
 

    return render_template('reports_bar_monthly.html', avg_inc=avg_inc, avg_exp=avg_exp, lbl_start=lbl_start, lbl_end=lbl_end, form=form, months_labels=months_labels, data_income=data_income, data_expenses=data_expenses)


@app.route('/reports/pie/monthly', methods=['GET', 'POST'])
@login_required
def reports_pie_monthly(): 
    form = PieFormMonthly()
    s_date = datetime.now()   
    year = s_date.strftime('%Y')
    month = s_date.strftime('%m') 
     
    if form.validate_on_submit():  
        s_date = datetime.strptime(form.date.data, '%Y-%m')   
        year = s_date.strftime('%Y')
        month = s_date.strftime('%m') 

    #transactions_today = Transaction.query.filter(and_(func.strftime('%Y-%m',Transaction.date) == s_date.strftime('%Y-%m'), Transaction.user_id == current_user.id )).all()
    transactions_today = Transaction.query.filter(and_(extract('year', Transaction.date) == year, extract('month', Transaction.date) == month, Transaction.user_id == current_user.id )).all()
    main_labels = []
    main_data = []
    transactions = []
    generate_labels(transactions_today, main_labels)
    generate_datas(transactions_today, main_labels, main_data) 
    generate_transactions(transactions_today,transactions ) 
    month = s_date.strftime('%B')
    return render_template('reports_pie_monthly.html', month=month, transactions=transactions,main_labels=main_labels, main_data=main_data, form=form)


@app.route('/reports/pie/daily', methods=['GET', 'POST'])
@login_required
def reports_pie_daily(): 
    form = PieFormDaily()
    s_date = datetime.now()   

    if form.validate_on_submit(): 
        s_date = datetime.strptime(form.date.data, '%Y-%m-%d')     
    transactions_today = Transaction.query.filter_by(user_id=current_user.id, date=s_date.date()).all()  
    main_labels = []
    main_data = []
    transactions = []

    generate_labels(transactions_today, main_labels)
    generate_datas(transactions_today, main_labels, main_data) 
    generate_transactions(transactions_today,transactions )

    day = s_date.strftime('%Y-%m-%d')
                    
    return render_template('reports_pie_daily.html',day=day, transactions=transactions,main_labels=main_labels, main_data=main_data, form=form)

 
 

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        if email is None:
            ph = generate_password_hash(form.password.data, 'sha256') 
            user=User(username=form.username.data, email=form.email.data, password_hash=ph )
            db.session.add(user)
            db.session.commit() 
            flash('Successfully registered, you can now login.')
            return redirect(url_for('login'))   
        else:
            flash('Email already exist, please choose another one.')
    for error in form.password.errors:
        flash(error)
    return render_template('register.html', form=form)

@app.route('/categories')
@login_required 
def categories(): 
    return render_template('categories.html')


@app.route('/', methods=['GET', 'POST'])
@login_required 
def home():   
    form = TransactionForm()
    if form.validate_on_submit(): 
        date = datetime.strptime(form.date.data, '%Y-%m-%d')
        transaction = Transaction(category=form.category.data, description=form.description.data, date=date, user_id=current_user.id, amount=form.amount.data)
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added')
        return redirect(url_for('home'))
    page = request.args.get('page', 1, type=int)
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date_added.desc()).paginate(page=page, per_page=20)
    return render_template('home.html', form=form, transactions=transactions) 


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    transaction = Transaction.query.get_or_404(id)
    try:
        db.session.delete(transaction)
        db.session.commit()
        flash("Transaction deleted")
        return redirect(url_for('home'))
    except:
        flash("Something wrong happned deleting the record, please try again")
        return redirect(url_for('home'))



