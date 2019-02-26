from app.models import User, Violation
from flask_login import current_user
class UserAnalytics(object):

    def myViolations(username, **kwargs):
        user = User.query.filter_by(username=username).first_or_404()
        if(kwargs):
            return Violation.query.filter_by(vio_received = user, acknowledge=kwargs.get('acknowledge')).order_by(Violation.violation_time.desc())


        else:
            return Violation.query.filter_by(vio_received = user).order_by(Violation.violation_time.desc())
