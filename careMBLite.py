from app import create_app, db
from flask import flash,redirect,url_for
from flask_admin.contrib.sqla import ModelView
from app.models import User, Violation, ViolationList, SeverityList, Tag
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password

#Flask Shell
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
#Admin view + Flask Security

class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.username == 'Karthi':
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                flash("You are not admin")
                return redirect(url_for('index'))
            else:
                # login
                return redirect(url_for('login'))


admin = Admin(app, name='careMBLite', template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Violation, db.session))
admin.add_view(MyModelView(ViolationList, db.session))
admin.add_view(MyModelView(SeverityList, db.session))
admin.add_view(MyModelView(Tag, db.session))

#to run using careMBLite.py
if __name__ == '__main__':
    app.run()
