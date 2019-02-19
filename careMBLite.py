from app import app, db
from flask_admin.contrib.sqla import ModelView
from app.models import User, Violation, ViolationList
from flask_admin import Admin
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
admin = Admin(app, name='careMBLite', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Violation, db.session))
admin.add_view(ModelView(ViolationList, db.session))
if __name__ == '__main__':
    app.run()

####### SET UP MAIL SERVER #########
