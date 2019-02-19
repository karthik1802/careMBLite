from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Violation, ViolationList


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    designation = StringField('Designation', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class ViolationForm(FlaskForm):
    violation_on = SelectField('Select Employee',coerce = int, validators=[DataRequired()])
    violation = SelectField('Select Violation', coerce = int, validators=[DataRequired()])
    remarks = TextAreaField('Remarks', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ViolationForm, self).__init__(*args, **kwargs)
        self.violation_on.choices = [(a.id, a.username) for a in User.query.filter_by(is_auth = True).order_by(User.id)]
        self.violation.choices = [(a.id, a.violation) for a in ViolationList.query.order_by(ViolationList.id)]

class ViolationAcknowledge(FlaskForm):
    remarks_vio = TextAreaField('Remarks', validators=[Length(min=0, max=140)])
    submit = SubmitField('Acknowledge')

class ViewViolationManager(FlaskForm):
    user = SelectField('Select Employee',coerce = int, validators=[DataRequired()])
    submit = SubmitField('Submit')
    def __init__(self, *args, **kwargs):
        super(ViewViolationManager, self).__init__(*args, **kwargs)
        self.user.choices = [(a.id, a.username) for a in User.query.order_by(User.id)]
