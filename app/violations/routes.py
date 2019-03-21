from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.violations.forms import ViolationForm, ViewViolationManager, ViolationAcknowledge,\
    ViolationTaggingForm
from app.models import User, Violation, ViolationList, Tag
from app.analytics import UserAnalytics
from app.violations import bp




@bp.route('/raise_violation', methods=['GET', 'POST'])
@login_required
def raise_violation():
    if current_user.vio_permision():
        form = ViolationForm()
        if form.validate_on_submit():
            vioRaised = Violation(violation_on=dict(form.violation_on.choices).get(form.violation_on.data),
            remarks= form.remarks.data , violation_time= datetime.utcnow() )
            current_user.vio_raised.append(vioRaised)
            violation_on = User.query.filter_by(id=form.violation_on.data).first()
            violation_on.vio_received.append(vioRaised)
            vio = ViolationList.query.filter_by(id=form.violation.data).first()
            vio.violist.append(vioRaised)
            db.session.add(vioRaised)
            db.session.commit()
            flash('Violation Raised!!')
            return redirect(url_for('main.index'))
    else:
        flash('You do not have permission to raise Violation, Sorry!!'+str(current_user.designation))
        return redirect(url_for('main.index'))
    return render_template('violations/violation.html', title='Violation', form=form)

@bp.route('/view_violations/<username>')
@login_required
def view_violations(username):
    return render_template('violations/view_violations.html',username=username, vios=UserAnalytics.userTagViolations(username, acknowledge=False),
    vios_res=UserAnalytics.userTagViolations(username, acknowledge = True) )


@bp.route('/acknowledge_violation/<violation_id>', methods=['GET', 'POST'])
@login_required
def acknowledge_violation(violation_id):
    #check username of violation
    violation = Violation.query.filter_by(id = violation_id).first()
    form_0 = ViolationAcknowledge(prefix="form_0")
    form_1 = ViolationTaggingForm(prefix="form_1")
    if True:
    #if current_user.username == violation.violation_on or current_user.vio_permision():   ##CHANGE IT!!
        if form_1.validate_on_submit():
            for a in form_1.tags.data:
                tagg = Tag.query.filter_by(id=a).first_or_404()
                violation.tags.append(tagg)
                db.session.commit()
            flash('Violation has been tagged')
            return redirect(url_for('violations.view_violations', username = violation.vio_received.username))
        if form_0.validate_on_submit():
            violation.acknowledge = True
            violation.acknowledge_time = datetime.utcnow()
            violation.remarks_vio = form_0.remarks_vio.data
            db.session.commit()
            flash('Acknowledged, Your response has been marked')
            return redirect(url_for('violations.view_violations', username = current_user.username))

        return render_template('violations/acknowledge_violation.html', violation=violation, form_0=form_0, form_1=form_1)
    else:
        flash("Don't try to act smart")
        return redirect(url_for('violations.view_violations', username = current_user.username))


@bp.route('/emp_violation', methods=['GET', 'POST'])
@login_required
def emp_violation():
    form = ViewViolationManager()
    if form.validate_on_submit():
        return redirect(url_for('violations.view_violations', username = dict(form.user.choices).get(form.user.data)))
    return render_template('violations/emp_select.html',form = form)
