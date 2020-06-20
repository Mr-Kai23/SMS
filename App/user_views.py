
# ======================================================
# @Author  :   Daniel                 
# @Time    :   2020.6.20
# @Desc    :   用户视图
# ======================================================

from flask import Blueprint, request, render_template, session, redirect, url_for
from flask_login import login_required
from .models import db
from utils.check_login import is_login
from .models import User, Role, Permission


user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/home/', methods=['GET'])
@is_login
def home():
    """
    首页
    :return:
    """
    if request.method == 'GET':
        return render_template('index.html')


@user_bp.route('/head', methods=['GET'])
@is_login
def head():
    """
    页头
    :return:
    """
    if request.method == 'GET':
        user = session.get('username')

        return render_template('head.html', user=user)


@user_bp.route('/left/', methods=['GET'])
@is_login
def left():
    """
    左侧栏
    :return:
    """
    if request.method == 'GET':
        # 获取用户
        user = session.get('username')
        # 获取用户权限
        permissions = User.query.filter_by(username=user).first().role.permission

        return render_template('left.html', permissions=permissions)


@user_bp.route('/register/', methods=['GET', 'POST'])
def register():
    """
    用户注册页面
    :return:
    """
    # 注册时返回注册页面
    if request.method == "GET":
        return render_template('register.html')

    if request.method == 'POST':
        # 获取用户注册信息
        username = request.form['username']
        pwd1 = request.form['pwd1']
        pwd2 = request.form['pwd2']

        # 定义个变量来控制过滤用户填写的信息
        flag = True
        # 判断用户是否信息都填写了.(all()函数可以判断序列中数据是否用空)
        if not all([username, pwd1, pwd2]):
            msg, flag = '请填写完整用户信息！', False

        if len(username) > 20:
            msg, flag = '用户名过长！', False

        if pwd1 != pwd2:
            msg, flag = '两次密码输入不一致！', False

        # 核对用户名是否已经被注册
        u = User.query.filter_by(username=username)

        if u:
            msg, flag = '用户已被注册！', False

        if not flag:
            return render_template('register.html', msg=msg)

        # 创建新用户
        user = User(username=username, password=pwd1)
        # 用户保存
        user.save()

        # 跳转到登录页面
        return redirect(url_for('user.login'))


@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """
    登录
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        if not all([username, pwd]):
            msg = '请填写完整信息'
            return render_template('login.html', msg=msg)

        user = User.query.filter_by(username=username, password=pwd).first()

        if user:
            session['user_id'] = user.u_id
            session['username'] = username

            return render_template('index.html')
        else:
            msg = '用户或密码错误！'

            return render_template('login.html', msg=msg)


@user_bp.route('/logout/', methods=['GET'])
def logout():
    """
    退吹登录
    :return:
    """
    if request.method == 'GET':

        # 清空session
        session.clear()
        # 跳转到登录页面
        return redirect(url_for('user.login'))


@user_bp.route('/user_per_list/', methods=['GET'])
@is_login
def user_per_list():
    """
    用户权限列表
    :return:
    """
    if request.method == 'GET':
        # 角色id
        r_id = request.args.get('r_id')
        # 权限
        pers = Role.query.get(r_id=r_id).permission

        return render_template('permission/permission_list.html', pers=pers)


@user_bp.route('/user_per_add/', methods=['GET', 'POST'])
@is_login
def add_user_per():
    """
    用户权限添加
    :return:
    """
    if request.method == 'GET':
        r_id = request.form.get('r_id')
        pers = Permission.query.all()
