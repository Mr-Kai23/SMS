
# ======================================================
# @Author  :   Daniel                 
# @Time    :   2020.6.20
# @Desc    :   用户视图
# ======================================================

from flask import request, render_template, redirect, url_for
from utils.check_login import is_login
from .models import Role
from .user_views import user_bp


@user_bp.route('/role/', methods=['GET'])
@is_login
def roles_list():
    """
    角色信息列表
    :return:
    """
    if request.method == 'GET':
        # 第几页
        page = int(request.args.get('page', 1))
        # 每页的数据
        page_num = int(request.args.get('page_num', 10))
        # 查询当前第几页的多少条数据
        paginate = Role.query.order_by('r_id').paginate(page, page_num)

        # 获取某页的具体数据
        roles = paginate.items

        return render_template('role/role_list.html', roles=roles)


@user_bp.route('/role_edit/', methods=['GET', 'POST'])
@is_login
def edit_role():
    """
    添加编辑角色
    :return:
    """
    if request.method == 'GET':
        r_id = request.args.get('r_id', None)

        if r_id:
            r_name = Role.query.get(r_id=int(r_id)).r_name

        return render_template('role/role_edit.html', locals())

    if request.method == 'POST':
        r_name = request.form['r_name']

        if 'r_id' in request.form and request.form['r_id']:
            role = Role.query.get(r_id=int(request.form['r_id']))

        else:
            r = Role.query.filter_by(r_name=r_name).first()

            if r:
                msg = '角色名称不能重复！！'

                return render_template('role/role_edit.html', msg=msg)

            role = Role()

        role.r_name = r_name

        role.save()

        # 重定向到 roles_list 方法
        return redirect(url_for('user.roles_list'))