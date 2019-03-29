from app import db
from flask import url_for
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
import base64
from datetime import datetime, timedelta
import os
from operator import eq

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data



class User(PaginatedAPIMixin, UserMixin, db.Model):
    __tablename__ = 'user'
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
    #vios = db.relationship('Violation', backref='author', lazy='dynamic')
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    teamMembers = db.relationship('User',
                backref=db.backref('manager', remote_side=[id])
            )
    vio_received = db.relationship('Violation', backref = 'vio_received', \
    lazy = 'dynamic', foreign_keys = 'Violation.violation_on')
    vio_raised = db.relationship('Violation', backref = 'vio_raised', \
    lazy = 'dynamic', foreign_keys = 'Violation.violation_by')

    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return format(self.username)

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

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'about_me': self.about_me,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in = 3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if User is None or user.token_expiration < datetime.utcnow():
            return None
        return user

tags = db.Table('tags',
    db.Column('vio_id', db.Integer, db.ForeignKey('violation.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)



class Violation(db.Model):
    __tablename__ = 'violation'
    id = db.Column(db.Integer, primary_key=True)
    violation_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    violation_on = db.Column(db.Integer, db.ForeignKey('user.id'))
    violation = db.Column(db.Integer, db.ForeignKey('violation_list.id'))
    remarks = db.Column(db.String(140))
    violation_time = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledge = db.Column(db.Boolean, default=False)
    remarks_vio = db.Column(db.String(140))
    acknowledge_time = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('violations', lazy=True))

    def __repr__(self):
        return '<Raised Violations {}>'.format(self.violation_on)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(14))
    description = db.Column(db.String(50))

    def __repr__(self):
        return '<Tags {}>'.format(self.tag)


class SeverityList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20))
    vio_name = db.relationship('ViolationList', backref='severity_vio', lazy='dynamic')

    def __repr__(self):
        return '<Levels {}>'.format(self.level)


class ViolationList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    violation = db.Column(db.String(140))
    severity = db.Column(db.Integer, db.ForeignKey('severity_list.id'))
    violist = db.relationship('Violation', backref='vio', lazy='dynamic')
    def __repr__(self):
        return '<Violations {}>'.format(self.violation)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(15))
    description = db.Column(db.String(75))
    def __repr__(self):
        return 'Status {}'.format(self.violation)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(15))
    description = db.Column(db.String(75))
    def __repr__(self):
        return 'Department {}'.format(self.violation)



class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asked_at = db.Column(db.DateTime, default = datetime.utcnow)
    asked_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    department = db.Column(db.Integer, db.ForeignKey('department.id'))
    summary = db.Column(db.String(52))
    description = db.Column(db.String(100))
    status = db.Column(db.Integer, db.ForeignKey('status.id'))
    is_individual = db.Column(db.Boolean, default = False)
    solvedAt = db.Column(db.DateTime, default = datetime.utcnow)
    def __repr__(self):
        return 'Request ID {}'.format(self.violation)
