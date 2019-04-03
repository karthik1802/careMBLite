from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, \
    current_app
from flask_login import current_user, login_required
from app import db
from app.service_request.forms import CreateRequestForm
from app.service_request import bp
from app.models import Request
@bp.route('/create_request', methods = ['GET', 'POST'])
@login_required
def create_request():
    form = CreateRequestForm()
    if form.validate_on_submit():
        requestCreated = Request(asked_at = , asked_by = , department = , summary = ,\
        description = , status = , is_individual = True )
    return render_template('service_request/create_request.html', title = 'Create Request', form = form)
