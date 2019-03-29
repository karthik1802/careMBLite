from app.models import User, Violation, Tag, tags
from app import db
from flask_login import current_user


class UserAnalytics(object):

    def userViolations(username, **kwargs):
        user = db.session.query(User).filter_by(username=username).first_or_404()
        if(kwargs):
            return db.session.query(Violation).filter_by(vio_received = user, acknowledge=kwargs.get('acknowledge')).order_by(Violation.violation_time.desc())


        else:
            return db.session.query(Violation).filter_by(vio_received == user).order_by(Violation.violation_time.desc())

    def userTagViolations(username, **kwargs):
        user = User.query.filter_by(username=username).first_or_404()
        if(kwargs):
            return db.session.query(Violation, Tag, tags).filter(tags.c.tag_id == 1).filter(Violation.id == tags.c.vio_id).order_by(Violation.violation_time.desc())
