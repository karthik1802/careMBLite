from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ViolationForm
from app.models import User, Violation
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()


    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        { 'body': 'Test post #1'},
        { 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/raise_violation', methods=['GET', 'POST'])
@login_required
def raise_violation():
    form = ViolationForm()
    if form.validate_on_submit():
        vioRaised = Violation(violation_by=current_user.username,
        violation_on=dict(form.violation_on.choices).get(form.violation_on.data),
        violation=dict(form.violation.choices).get(form.violation.data) ,
        remarks= form.remarks.data , violation_time= datetime.utcnow() )
        db.session.add(vioRaised)
        db.session.commit()
        flash('Violation Raised!!')
        return redirect(url_for('index'))
    return render_template('violation.html', title='Violation', form=form)

@app.route('/view_violations')
@login_required
def view_violations():
    vios = [(a.id, a.violation) for a in Violation.query.filter_by(violation_on = current_user.username)]
    list = []
    return render_template('view_violations.html',user=user, vios=vios)
