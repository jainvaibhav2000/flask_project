from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, EmailField, validators, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from organization.models import Employee
from datetime import date

# class TelephoneForm(Form):
#     country_code = IntegerField('Country Code')
#     area_code    = IntegerField('Area Code/Exchange')
#     number       = StringField('Number')

class RegisterForm(FlaskForm):

    def validate_email_address(self, email_address_to_check):
        email = Employee.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError('E-mail already exists! Please try a different E-mail')

    def validate_mobile_phone(self, mobile_phone_to_check):
        phone = Employee.query.filter_by(phone=mobile_phone_to_check.data).first()
        if phone:
            raise ValidationError('Phone Number already exists! Please try a different Phone Number')
        elif len(str(mobile_phone_to_check.data)) != 10:
            raise ValidationError("Phone Number should be 10 digit")

    def validate_dob(self, dob_to_check):
        if dob_to_check.data > date.today():
            raise ValidationError('Date of Birth is Invalid')


    firstname = StringField(label='First Name', validators=[Length(min=2,max=20), DataRequired()])
    lastname = StringField(label='Last Name', validators=[Length(min=1,max=10), DataRequired()])
    email_address = EmailField(label='E-mail', validators=[Email(), DataRequired()])
    #mobile_phone = FormField(TelephoneForm)
    mobile_phone = IntegerField(label='Phone Number', validators=[DataRequired()])
    dob = DateField(label="Date Of Birth", validators=[DataRequired()])
    address = StringField(label="Address", validators=[DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email_address = EmailField(label='E-mail', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class SearchForm(FlaskForm):
    choice = SelectField(label='select category', choices=[('select category','select category'),('Name','Name'),('Email','Email')],default=1, validators=[DataRequired()])
    input = StringField(label='search', validators=[DataRequired()])

class UpdateForm(FlaskForm):
    # def validate_mobile_phone(self, mobile_phone_to_check):
    #     if len(FlaskForm.mobile_phone):
    #         raise ValidationError('E-mail already exists! Please try a different E-mail')
    def validate_mobile_phone(self, mobile_phone_to_check):
        if len(str(mobile_phone_to_check.data)) != 10:
            raise ValidationError("Phone Number should be 10 digit")

    def validate_dob(self, dob_to_check):
        if dob_to_check.data > date.today():
            raise ValidationError('Date of Birth is Invalid')

    firstname = StringField(label='First Name', validators=[Length(min=2, max=20), DataRequired()])
    lastname = StringField(label='Last Name', validators=[Length(min=1, max=10), DataRequired()])
    email_address = EmailField(label='E-mail')
    mobile_phone = IntegerField(label='Phone Number', validators=[DataRequired()])
    dob = DateField(label="Date Of Birth", validators=[DataRequired()])
    address = StringField(label="Address", validators=[DataRequired()])
    submit = SubmitField(label='Create Account')