from flask import request
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Length, \
    Email, EqualTo, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User, Violation, ViolationList, Tag
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,\
    SubmitField, TextAreaField, SelectField, SelectMultipleField, \
    widgets

#Checkbox Widget
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


#Edit Profile
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

#Form To raise violatio on an Employee
class ViolationForm(FlaskForm):
    violation_on = SelectField('Select Employee',coerce = int, validators=[DataRequired()])
    violation = SelectField('Select Violation', coerce = int, validators=[DataRequired()])
    remarks = TextAreaField('Remarks', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    #To load choices from db
    def __init__(self, *args, **kwargs):
        super(ViolationForm, self).__init__(*args, **kwargs)
        self.violation_on.choices = [(a.id, a.username) for a in User.query.filter_by(is_auth = True).order_by(User.id)]
        #self.violation_on.choices = [(a.id, a.username) for a in User.query.order_by(User.id)]
        self.violation.choices = [(a.id, a.violation) for a in ViolationList.query.order_by(ViolationList.id)]

#For employee to acknowledge his violation
class ViolationAcknowledge(FlaskForm):
    remarks_vio = TextAreaField('Remarks', validators=[Length(min=0, max=140)])
    submit = SubmitField('Acknowledge')

#To tag a violation after being acknowledged
class ViolationTaggingForm(FlaskForm):
    tags = MultiCheckboxField('', coerce = int)
    submit = SubmitField('Submit')
    def __init__(self, *args, **kwargs):
        super(ViolationTaggingForm, self).__init__(*args, **kwargs)
        self.tags.choices = [(a.id, a.tag) for a in Tag.query.order_by(Tag.id)]

#To Select which violation to see
class ViewViolationManager(FlaskForm):
    user = SelectField('Select Employee',coerce = int, validators=[DataRequired()])
    submit = SubmitField('Submit')
    def __init__(self, *args, **kwargs):
        super(ViewViolationManager, self).__init__(*args, **kwargs)
        self.user.choices = [(a.id, a.username) for a in User.query.order_by(User.id)]
