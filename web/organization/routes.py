from organization import app
from flask import render_template, redirect, url_for, flash, request
from organization.models import Employee
from organization.forms import RegisterForm, LoginForm, SearchForm, UpdateForm
from organization import db
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
import jwt

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s %(message)s')
file_handler = logging.FileHandler('organization/logs/flask_app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

tt = ""
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = tt
        if token=="":
            flash('You are not authorized user:', category='danger')
            return redirect(url_for('login_page'))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms="HS256")
        except jwt.ExpiredSignatureError:
            logger.info(f'employee_id for current user:{current_user.id} and name {current_user.first_name} {current_user.last_name} is logout due to token expired')
            # logout_user()
            flash('Token is Expired Please Login again:',category='danger')
            return redirect(url_for('logout_page'))
        return func(*args, **kwargs)
    return decorated

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route('/detail')
@login_required
@token_required
def detail_page():
    logger.info(f'employee_id for current user:{current_user.id} and name {current_user.first_name} {current_user.last_name} access the Details Page')
    return render_template('details.html')

@app.route("/employee")
@login_required
@token_required
def employee_page():
    logger.info(f'employee_id for current user:{current_user.id} and name {current_user.first_name} {current_user.last_name} access the Employees Page')
    employees = Employee.query.all()
    form = SearchForm()
    # view=0
    # for i in employees:
    #     view=i
    #     break
    #print(view)
    return render_template('employees.html',employees=employees, view=None, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        create_employee = Employee(first_name=form.firstname.data,
                                  last_name=form.lastname.data,
                                  email_address=form.email_address.data,
                                  phone=form.mobile_phone.data,
                                  dob=form.dob.data,
                                  address=form.address.data,
                                  password=form.password1.data)
        db.session.add(create_employee)
        db.session.commit()
        login_user(create_employee)

        global tt
        valid_for = datetime.now() + timedelta(minutes=15)
        epoc_time = int(valid_for.timestamp())
        token = jwt.encode({
            'payload': form.firstname.data,
            'exp': epoc_time
        },
            app.config['SECRET_KEY'], algorithm="HS256")
        tt = token

        logger.info(f'New user-- employee_id for current user:{current_user.id} and name {current_user.first_name} {current_user.last_name} is login')
        flash(f"Account created successfully! You are now logged in as {create_employee.first_name} {create_employee.last_name}", category='success')
        return redirect(url_for('employee_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error to creating a user: {err_msg}',category='danger')
    return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    # app.config['WTF_CSRF_ENABLED']=False
    form = LoginForm(request.form)
    if form.validate_on_submit():
        attempted_employee_login = Employee.query.filter_by(email_address=form.email_address.data).first()
        if attempted_employee_login and attempted_employee_login.check_login_password(attempted_password=form.password.data):
            login_user(attempted_employee_login)

            global tt
            valid_for = datetime.now() + timedelta(minutes=15)
            epoc_time = int(valid_for.timestamp())
            token = jwt.encode({
                'payload': attempted_employee_login.first_name,
                'exp': epoc_time
            },
                app.config['SECRET_KEY'], algorithm="HS256")
            tt = token

            logger.info(f'employee_id for current user:{current_user.id} and name {current_user.first_name} {current_user.last_name} is login')
            flash(f"You Successfully logged in as: {attempted_employee_login.first_name} {attempted_employee_login.last_name}", category='success')

            return redirect(url_for('detail_page'))
        else:
            logger.error(f'unauthorized user-- {form.email_address.data} is try to login')
            flash('E-mail and Password are not match! Please try again',category='danger')
            #return "by"

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    global tt
    tt = ""
    logger.info(f'employee_id for current user:{current_user.id} and name {current_user.first_name} {current_user.last_name} is logout')
    logout_user()
    flash("You have been logged out Successfully!", category="info")
    return redirect(url_for("home_page"))

@app.route("/employee/edit/<id>",methods=['GET','POST'])
@login_required
@token_required
def update_page(id):
    form = UpdateForm()
    if current_user.admin:
        employee = Employee.query.filter_by(id=id).first()
        if form.validate_on_submit():
            employee.first_name = form.firstname.data
            employee.last_name = form.lastname.data
            employee.phone = form.mobile_phone.data
            employee.dob = form.dob.data
            employee.address = form.address.data
            db.session.commit()
            flash(f"Account Update successfully!", category='success')

            logger.info(f'employee_id of admin:{current_user.id} and name {current_user.first_name} {current_user.last_name} update the employee information of employee_id-{id}')
            return redirect(url_for('employee_page'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error to updating a user details: {err_msg}', category='danger')

        return render_template('update.html', employee=employee, form=form)
    else:
        logger.warning(f'employee_id for current user:{current_user.id} and name {current_user.first_name} {current_user.last_name} try to update the employee information of employee_id-{id}')
        return redirect(url_for('employee_page'))


@app.route("/employee/<id>",methods=['GET','POST'])
@login_required
@token_required
def view_page(id):

    if current_user.admin:
        form=SearchForm()
        employees = Employee.query.all()
        view = Employee.query.filter_by(id=id).first()

        logger.info(f'employee_id of admin:{current_user.id} and name {current_user.first_name} {current_user.last_name} view the employee information of employee_id-{id}')
        return render_template('employees.html', employees=employees, view=view, form=form)
    else:
        logger.warning(f'employee_id for current user:{current_user.id} and name {current_user.first_name} {current_user.last_name} try to view the employee information of employee_id-{id}')
    return redirect(url_for('employee_page'))


@app.route("/delete/<id>",methods=['GET','POST'])
@login_required
@token_required
def delete_page(id):
    if current_user.admin:
        employee = Employee.query.filter_by(id=id).first()
        db.session.delete(employee)
        db.session.commit()

        logger.info(f'employee_id of admin:{current_user.id} and name {current_user.first_name} {current_user.last_name} delete the employee information of employee_id-{id}')
    else:
        logger.warning(f'employee_id for current user:{current_user.id} and name {current_user.first_name} {current_user.last_name} try to delete the employee information of employee_id-{id}')
    return redirect(url_for('employee_page'))

@app.route("/search", methods=['GET', 'POST'])
@login_required
@token_required
def search_page():
    form = SearchForm()
    search_value = form.input.data
    if form.choice.data == "Email":
        if len(search_value) != 0:
            employees = Employee.query.filter(Employee.email_address.contains(search_value))
            return render_template('employees.html', employees=employees, view=None, form=form)
        else:
            flash('Enter Value for search', category='danger')
    elif form.choice.data == "Name":
        lst = search_value.split()
        if len(lst)==1:
            employees = Employee.query.filter(Employee.first_name.contains(lst[0]))
            return render_template('employees.html', employees=employees, view=None, form=form)
        elif len(lst)==2:
            employees = Employee.query.filter(Employee.first_name.contains(lst[0]), Employee.last_name.contains(lst[1]))
            return render_template('employees.html', employees=employees, view=None, form=form)
        else:
            flash('Enter Value for search', category='danger')
    return redirect(url_for('employee_page'))