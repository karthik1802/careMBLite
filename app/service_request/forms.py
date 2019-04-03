from flask import request
from flask_wtf import  FlaskForm
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User, Department
from wtforms import StringField, PasswordField, BooleanField,\
    SubmitField, TextAreaField, SelectField, SelectMultipleField, \
    widgets


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label = False)
    option_widget = widgets.CheckboxInput()



class CreateRequestForm(FlaskForm):
    department = SelectField('Select Department', coerce = int, validators=[DataRequired()])
    summary = TextAreaField('Summary', validators = [Length(min=0, max=140)])
    description = TextAreaField('Description', validators = [Length(min=0, max=140)])
    submit = SubmitField('Submit')
    suggest_individual = MultiCheckboxField('', coerce = int)

    def __init__(self, *args, **kwargs):
        super(CreateRequestForm, self).__init__(*args, **kwargs)
        self.department.choices = [(a.id, a.name) for a in Department.query.order_by(Department.id)]
        self.suggest_individual.choices = [(a.id, a.username) for a in User.query.order_by(user.id)]
