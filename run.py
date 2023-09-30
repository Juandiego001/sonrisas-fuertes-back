from app import app
from app.controllers.account import bp as bp_account
from app.controllers.admin import bp as bp_admin
from app.controllers.teacher import bp as bp_teacher
from app.controllers.student import bp as bp_student
from app.controllers.group import bp as bp_group
from app.controllers.subject import bp as bp_subject
from app.controllers.resource import bp as bp_resource

app.register_blueprint(bp_account, url_prefix='/api/account')
app.register_blueprint(bp_admin, url_prefix='/api/admin')
app.register_blueprint(bp_teacher, url_prefix='/api/teacher')
app.register_blueprint(bp_student, url_prefix='/api/student')
app.register_blueprint(bp_group, url_prefix='/api/group')
app.register_blueprint(bp_subject, url_prefix='/api/subject')
app.register_blueprint(bp_resource, url_prefix='/api/resource')

if __name__ == '__main__':
    app.run('localhost', 5000, True)