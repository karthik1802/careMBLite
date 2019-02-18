from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from operator import eq

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(10))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    designation = db.Column(db.String)
    other = db.Column(db.String)
    is_auth = db.Column(db.Boolean, default=False)
    vios = db.relationship('Violation', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def vio_permision(self):
        if self.designation == "Manager" :
            return True                         
        else:
            return False

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Violation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    violation_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    violation_on = db.Column(db.String(15))
    violation = db.Column(db.String(140))
    remarks = db.Column(db.String(140))
    violation_time = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledge = db.Column(db.Boolean, default=False)
    remarks_vio = db.Column(db.String(140))
    acknowledge_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Raised Violations {}>'.format(self.violation_on)


class ViolationList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    violation = db.Column(db.String(140))

    def __repr__(self):
        return '<Violations {}>'.format(self.violation)
