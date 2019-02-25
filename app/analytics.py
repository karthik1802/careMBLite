from app.models import *

class UserAnalytics(object):

    def myViolations(username, **kwargs):
        if(kwargs):
            return Violation.query.filter_by(violation_on = username).order_by(Violation.violation_time.desc())

        else:
            return Violation.query.filter_by(violation_received = username).order_by(Violation.violation_time.desc())

    #def myTeamsViolations(username, **kwargs):
    #    if(kwargs):
