
# ======================================================
# @Author  :   Daniel                 
# @Time    :   2020.6.20
# @Desc    :   项目启动文件
# ======================================================

from flask_script import Manager
from utils.functions import create_app
from App.models import db
from App.user_views import *
from App.permission_views import *
from App.grade_views import *
from App.role_views import *
from App.student_views import *
from flask_migrate import MigrateCommand, Migrate

app = create_app()


@app.route('/')
def redirect_login():
    """
    初始的路由转发
    :return:
    """
    return redirect(url_for('user.login'))


manage = Manager(app)

# 数据库迁移
Migrate(app, db)
manage.add_command("db", MigrateCommand)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5188)
    # manage.run()
