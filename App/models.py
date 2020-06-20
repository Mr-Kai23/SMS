
# ======================================================
# @Author  :   Daniel                 
# @Time    :   2020.6.20
# @Desc    :   数据库文件
# ======================================================

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .user_views import user_bp

# 初始化db
db = SQLAlchemy()


class Grade(db.Model):
    """
    班级模型
    """
    g_id = db.Column('grade_id', db.Integer, autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(20), unique=True)
    g_create_time = db.Column(db.DateTime, default=datetime.now)

    # 设置与班级一对多的关联关系
    students = db.relationship('Student', backref='grade')

    # 自定义表名
    __tablename__ = 'grade'

    def __init__(self, name):
        self.g_name = name

    def save(self):
        db.session.add(self)
        db.session.commit()


class Student(db.Model):
    """
    学生模型
    """
    s_id = db.Column('student_id', db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(20))
    s_sex = db.Column(db.Integer)
    # 设置与班级 一对多的关联关系
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)

    def __init__(self, name, sex, grade_id):
        self.s_name = name
        self.s_sex = sex
        self.grade_id = grade_id

        # 自定义表名
        __tablename__ = 'student'

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    """
    用户模型
    """
    u_id = db.Column('user_id', db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    u_create_time = db.Column(db.DateTime, default=datetime.now)

    # 用户和角色的一对多的关联关系
    role_id = db.Column(db.Integer, db.ForeignKey('role.r_id'))

    # 表名
    __tablename__ = 'user'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()


# 角色和权限的(多对多的)关联表
# r_p为关联表的表名
r_p = db.Table('r_p',
               db.Column('role_id', db.Integer, db.ForeignKey('role.r_id'), primary_key=True),
               db.Column('permission_id', db.Integer, db.ForeignKey('permission.p_id'), primary_key=True)
               )


class Role(db.Model):
    """
    角色模型
    """
    r_id = db.Column('role_id', db.Integer, autoincrement=True, primary_key=True)
    r_name = db.Column(db.String(20))
    # 用户和角色一对多的关联关系, backref:user取角色时的引用名
    users = db.relationship('User', backref='role')

    # 表名
    __tablename__ = 'role'

    def __init__(self, name):
        self.r_name = name

    def save(self):
        db.session.add(self)
        db.session.commit()


class Permission(db.Model):
    """
    权限模型
    """
    p_id = db.Column('permission_id', db.Integer, autoincrement=True, primary_key=True)
    p_name = db.Column(db.String(20), unique=True)
    p_er = db.Column(db.String(16), unique=True)

    # 角色和权限的多对多的关系，backref:role取权限时的引用名
    roles = db.relationship('Role', secondery=r_p, backref=db.backref('permission', lazy=True))

    # 表名
    __tablename__ = 'permission'

    def __init__(self, name, er):
        self.p_name = name
        self.p_er = er

    def save(self):
        db.session.add(self)
        db.session.commit()


@user_bp.route('/create_db/')
def create_db():
    """
    创建数据库
    :return:
    """

    db.create_all()


@user_bp.route('/drop_db/')
def drop_db():
    """
    删除数据库
    :return:
    """

    db.drop_all()

    return '删除成功！'