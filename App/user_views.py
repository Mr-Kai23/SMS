
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


user_bp = Blueprint('user', __name__)


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


@user_bp.route('/home/', methods=['GET'])
@is_login
def home():
    """
    首页
    :return:
    """
    if request.method == 'GET':
        return render_template('index.html')


@user_bp.route('/head/', methods=['GET'])
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
        user = User.query.filter_by(username=user).first()

        if user:
            permissions = user.role.permisson

        return render_template('left.html', locals())


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
        u = User.query.filter_by(username=username).first()

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

        return render_template('add_user_per.html', pers=pers, r_id=r_id)

    if request.method == 'POST':
        r_id = request.form.get('r_id')
        p_id = request.form.get('p_id')

        # 获取对象角色
        role = Role.query.get(r_id=r_id)
        # 获取权限对象
        per = Permission.query.get(p_id=p_id)

        # 添加对应关系
        per.roles.append(role)

        per.save()

        # 重定向到 roles_list 函数, user:蓝图名称
        return redirect(url_for('user.roles_list'))


@user_bp.route('/user_per_sub/', methods=['GET', 'POST'])
@is_login
def sub_user_per():
    """
    用户权限减少
    :return:
    """
    if request.method == 'GET':
        r_id = request.form.get('r_id')
        pers = Role.query.get(r_id=r_id).permission

        return render_template('user_per_list.html', pers=pers, r_id=r_id)

    if request.method == 'POST':
        r_id = request.form.get('r_id')
        p_id = request.form.get('p_id')

        # 获取对象角色
        role = Role.query.get(r_id=r_id)
        # 获取权限对象
        per = Permission.query.get(p_id=p_id)

        # 添加对应关系
        per.roles.remove(role)

        db.session.commit()

        pers = Role.query.get(r_id=r_id).permission

        # 重定向到 roles_list 函数, user:蓝图名称
        return render_template('user_per_list.html', pers=pers, r_id=r_id)


@user_bp.route('/user_list/', methods=['GET'])
@is_login
def user_list():
    """
    用户列表
    :return:
    """
    if request.method == 'GET':
        # 页码
        page = int(request.args.get('page', 1))
        # 页面数据
        page_num = int(request.args.get('page_num', 10))

        paginate = User.query.order_by('u_id').paginate(page, page_num)

        users = paginate.items

        return render_template('user/user_list.html', users=users)


@user_bp.route('/user_edit/', methods=['GET', 'POST'])
@is_login
def edit_user():
    """
    用户添加编辑
    :return:
    """
    if request.method == 'GET':
        u_id = request.args.get('u_id', None)

        if u_id:
            user = User.query.get(u_id=int(u_id))
            username = user.username

            # g_name = Grade.query.filter(Grade.g_id==g_id).first().g_name

        return render_template('user/user_edit.html', locals())

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
        u = User.query.filter_by(username=username).first()

        if u:
            msg, flag = '用户已被注册！', False

        if not flag:
            return render_template('user/user_edit.html', msg=msg)

        if 'u_id' in request.form and request.form['u_id']:
            user = User.query.get(u_id=int(request.form['u_id']))

        else:
            user = User()

        user.username = username
        user.password = pwd1

        user.save()

        return redirect(url_for('user.user_list'))


@user_bp.route('/role_assign/', methods=['GET', 'POST'])
@is_login
def assign_user_role():
    """
    分配用户权限
    """
    if request.method == 'GET':

        u_id = request.args.get('u_id')
        roles = Role.query.all()

        return render_template('assign_user_role.html', roles=roles, u_id=u_id)

    if request.method == 'POST':

        r_id = request.form.get('r_id')
        u_id = request.form.get('u_id')

        user = User.query.filter_by(u_id=u_id).first()
        user.role_id = r_id

        db.session.commit()

        return redirect(url_for('user.user_list'))


@user_bp.route('/pwd_change/', methods=['GET', 'POST'])
@is_login
def change_password():
    """
    修改用户密码
    """
    if request.method == 'GET':
        username = session.get('username')

        user = User.query.filter_by(username=username).first()

        return render_template('pwd_change.html', user=user)

    if request.method == 'POST':

        username = session.get('username')
        pwd1 = request.form.get('pwd1')
        pwd2 = request.form.get('pwd2')
        pwd3 = request.form.get('pwd3')

        pwd = User.query.filter_by(password=pwd1, username=username).first()

        if not pwd:
            msg = '请输入正确的旧密码'
            username = session.get('username')
            user = User.query.filter_by(username=username).first()

            return render_template('pwd_change.html', msg=msg, user=user)
        else:

            if not all([pwd2, pwd3]):
                msg = '密码不能为空'
                username = session.get('username')
                user = User.query.filter_by(username=username).first()

                return render_template('pwd_change.html', msg=msg, user=user)

        if pwd2 != pwd3:
            msg = '两次密码不一致,请重新输入'
            username = session.get('username')
            user = User.query.filter_by(username=username).first()

            return render_template('pwd_change.html', msg=msg, user=user)

        pwd.password = pwd2

        db.session.commit()

        return redirect(url_for('user.change_pass_sucess'))


@user_bp.route('/pwd_change_su/', methods=['GET'])
@is_login
def change_pass_sucess():
    """
    修改密码成功后
    """
    if request.method == 'GET':
        return render_template('pwd_change_su.html')
