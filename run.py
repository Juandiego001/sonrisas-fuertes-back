from app import app, host
from app.controllers.account import bp as bp_account
from app.controllers.admin import bp as bp_admin
from app.controllers.teacher import bp as bp_teacher
from app.controllers.tutor import bp as bp_tutor
from app.controllers.student import bp as bp_student
from app.controllers.profile import bp as bp_profile
from app.controllers.resource import bp as bp_resource
from app.controllers.permission import bp as bp_permission
from app.controllers.publication import bp as bp_publication
from app.controllers.comment import bp as bp_comment
from app.controllers.folder import bp as bp_folder
from app.controllers.activity import bp as bp_activity
from app.controllers.link import bp as bp_link
from app.controllers.file import bp as bp_file


app.register_blueprint(bp_account, url_prefix='/api/account')
app.register_blueprint(bp_admin, url_prefix='/api/admin')
app.register_blueprint(bp_teacher, url_prefix='/api/teacher')
app.register_blueprint(bp_tutor, url_prefix='/api/tutor')
app.register_blueprint(bp_student, url_prefix='/api/student')
app.register_blueprint(bp_profile, url_prefix='/api/profile')
app.register_blueprint(bp_resource, url_prefix='/api/resource')
app.register_blueprint(bp_permission, url_prefix='/api/permission')
app.register_blueprint(bp_publication, url_prefix='/api/publication')
app.register_blueprint(bp_comment, url_prefix='/api/comment')
app.register_blueprint(bp_folder, url_prefix='/api/folder')
app.register_blueprint(bp_activity, url_prefix='/api/activity')
app.register_blueprint(bp_link, url_prefix='/api/link')
app.register_blueprint(bp_file, url_prefix='/api/file')


if __name__ == '__main__':
    app.run(host, 5000, True)