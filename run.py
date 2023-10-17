from app import app, host
from app.controllers.account import bp as bp_account
from app.controllers.admin import bp as bp_admin
from app.controllers.teacher import bp as bp_teacher
from app.controllers.student import bp as bp_student
from app.controllers.profile import bp as bp_profile
from app.controllers.subject import bp as bp_subject
from app.controllers.resource import bp as bp_resource
from app.controllers.permission import bp as bp_permission
from app.controllers.group import bp as bp_group
from app.controllers.publication import bp as bp_publication
from app.controllers.comment import bp as bp_comment

app.register_blueprint(bp_account, url_prefix='/api/account')
app.register_blueprint(bp_admin, url_prefix='/api/admin')
app.register_blueprint(bp_teacher, url_prefix='/api/teacher')
app.register_blueprint(bp_student, url_prefix='/api/student')
app.register_blueprint(bp_profile, url_prefix='/api/profile')
app.register_blueprint(bp_subject, url_prefix='/api/subject')
app.register_blueprint(bp_resource, url_prefix='/api/resource')
app.register_blueprint(bp_group, url_prefix='/api/group')
app.register_blueprint(bp_permission, url_prefix='/api/permission')
app.register_blueprint(bp_publication, url_prefix='/api/publication')
app.register_blueprint(bp_comment, url_prefix='/api/comment')

if __name__ == '__main__':
    app.run(host, 5000, True)