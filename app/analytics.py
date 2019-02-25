from app.models import *

class UserAnalytics(object):

    def myViolations(username, **kwargs):
        if(kwargs):
            return Violation.query.filter(Violation.violation_on.in_(['Karthi','test-user'])).filter_by(acknowledge=kwargs.get('acknowledge')).order_by(Violation.violation_time.desc())

        else:
            return Violation.query.filter_by(violation_on = username).order_by(Violation.violation_time.desc())

    #def myTeamsViolations(username, **kwargs):
    #    a = User.query.join(teams, (teams.c.manager_id == User.id)).filter(teams.c.employee_id == 1)
    #    print(a)
    #    return Violation.query.filter(Violation.violation_on.in_(a))
