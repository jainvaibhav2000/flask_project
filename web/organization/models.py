from organization import db, login_manager
from organization import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)

class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=20), nullable=False)
    last_name = db.Column(db.String(length=10), nullable=False)
    email_address = db.Column(db.String(length=40), nullable=False, unique=True)
    phone = db.Column(db.Integer(), nullable=False, unique=True)
    dob = db.Column(db.Date(), nullable=False)
    address = db.Column(db.String(length=20), nullable=False)
    admin = db.Column(db.Boolean,default=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_login_password(self, attempted_password):
        if bcrypt.check_password_hash(self.password_hash, attempted_password):
            return  True
        else:
            return False


    def __repr__(self):
        return f'Employee{self.first_name}'

# class EmployeeToken(db.Model, UserMixin):
#     id = db.Column(db.Integer(), primary_key=True)
#     token = db.Column(db.String(), nullable=False, unique=True)


