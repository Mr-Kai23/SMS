
# ======================================================
# @Author  :   Daniel                 
# @Time    :   2020.6.20
# @Desc    :   项目启动文件
# ======================================================

from flask_script import Manager
from utils.functions import create_app
from App.user_views import *
from App.permission_views import *
from App.grade_views import *
from App.role_views import *
from App.student_views import *

app = create_app()

manage = Manager(app=app)


if __name__ == '__main__':
    manage.run(host='0.0.0.0', port=5188)
