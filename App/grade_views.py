
# ======================================================
# @Author  :   Daniel                 
# @Time    :   2020.6.20
# @Desc    :   用户视图
# ======================================================

from flask import request, render_template
from utils.check_login import is_login
from .models import Grade, Student
from .user_views import user_bp


@user_bp.route('/grade/', methods=['GET'])
@is_login
def grades_list():
    """
    显示班级列表
    :return:
    """
    if request.method == 'GET':
        # 查询第几页数据
        page = int(request.args.get('page', 1))
        # 查询每页的数据是多少，默认为10条
        page_num = int(request.args.get('page_num', 10))
        # 查询当前第几页的多少条数据
        paginate = Grade.query.order_by('g_id').paginate(page, page_num)
        # 获取某页的具体数据
        grades = paginate.items

        # 返回获取到的数据到前端页面
        return render_template('grade/grade_list.html', grades=grades, paginate=paginate)


@user_bp.route('/grade_edit/', methods=['GET', 'POST'])
@is_login
def edit_grade():
    """
    班级添加
    :return:
    """
    if request.method == 'GET':
        g_id = request.args.get('g_id', None)

        if g_id:
            g_name = Grade.query.get(g_id=int(g_id)).g_name
            # g_name = Grade.query.filter(Grade.g_id==g_id).first().g_name

        return render_template('grade/grade_edit.html', locals())

    if request.method == 'POST':
        g_name = request.form['g_name']

        # 判断是否为编辑修改
        if 'g_id' in request.form and request.form['g_id']:
            grade = Grade.query.get(g_id=int(request.form['g_id']))

        else:

            o_grade = Grade.query.filter_by(g_name=g_name).first()

            # 判断要添加的信息数据库中是否存在(因为班级名称不能重复)
            if o_grade:
                msg = '班级名称不能重复！！'
                return render_template('grade/grade_edit.html', msg=msg)

            # 创建班级
            grade = Grade()

        grade.g_name = g_name
        grade.save()


@user_bp.route('/grade_student/', methods=['GET', 'POST'])
@is_login
def grade_students_list():
    """
    班级学生列表
    :return:
    """
    if request.method == 'GET':
        g_id = request.args.get('g_id')

        students = Student.query.filter_by(grade_id=g_id).all()

        return render_template('student/student_list.html', students=students)

