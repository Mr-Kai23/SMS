
# ======================================================
# @Author  :   Daniel                 
# @Time    :   2020.6.20
# @Desc    :   用户视图
# ======================================================

from flask import request, render_template, redirect, url_for
from utils.check_login import is_login
from .models import Grade, Student, Permission
from .user_views import user_bp


@user_bp.route('/permission/', methods=['GET'])
@is_login
def permission_list():
    """
    权限列表
    :return:
    """
    if request.method == 'GET':
        permissions = Permission.query.all()

        return render_template('permission/permission.html', permissions=permissions)


@user_bp.route('/permission_edit/', methods=['GET', 'POST'])
@is_login
def edit_permission():
    """
    添加编辑权限
    :return:
    """
    if request.method == 'GET':
        pers = Permission.query.all()

        # 如果是编辑，就会获取到p_id
        p_id = request.form.get('p_id', None)

        if p_id:
            p_name = Permission.query.get('p_id').p_name

        return render_template('permission/permission_edit.html', locals())

    if request.method == 'POST':
        p_name = request.form.get('p_name')
        p_er = request.form.get('p_er')

        if 'p_id' in request.form and request.form['p_id']:
            permission = Permission.query.get(p_id=int(request.form['p_id']))

        else:
            # 权限名称
            p_name_test_repeat = Permission.query.filter_by(p_name=p_name).first()

            if p_name_test_repeat:
                msg = '权限名称重复!'

                return render_template('permission/permission_edit.html', msg=msg)

            # 权限简称
            p_er_test_repeat = Permission.query.filter_by(p_er=p_er).first()

            if p_er_test_repeat:
                msg1 = '权限简写名重复!'

                return render_template('permission/permission_edit.html', msg=msg1)

            permission = Permission()

        permission.p_name = p_name
        permission.p_er = p_er

        permission.save()

        return redirect(url_for('user.permission_list'))
