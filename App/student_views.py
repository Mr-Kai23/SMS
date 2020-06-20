
# ======================================================
# @Author  :   Daniel                 
# @Time    :   2020.6.20
# @Desc    :   用户视图
# ======================================================

from flask import request, render_template
from utils.check_login import is_login
from .models import Student, Grade
from .user_views import user_bp


@user_bp.route('/student/', methods=['GET'])
@is_login
def students_list():
    """
    学生列表
    :return:
    """
    if request.method == 'GET':

        # 第几页
        page = int(request.args.get('page', 1))
        # 每页的数据
        page_num = int(request.args.get('page_num', 10))
        # 查询当前第几页的多少条数据
        paginate = Student.query.order_by('s_id').paginate(page, page_num)

        # 获取某页的具体数据
        students = paginate.items

        return render_template('student/student_list.html', students=students)


@user_bp.route('/student_edit/', methods=['GET', 'POST'])
@is_login
def edit_student():
    """
    添加编辑学生
    :return:
    """
    if request.method == 'GET':
        grades = Grade.query.all()
        s_id = request.args.get('s_id', None)

        if s_id:
            student = Student.query.get(s_id=s_id)
            s_name = student.s_name
            s_sex = student.s_sex

        return render_template('student/student_edit.html', locals())

    if request.method == 'POST':
        s_name = request.form.get('s_name')
        s_sex = request.form.get('s_sex')
        grade_id = request.form.get('g_name')

        if 's_id' in request.form and request.form['s_id']:
            student = Student.query.get(s_id=int(request.form['s_id']))

        else:
            stu = Student.query.filter_by(s_name=s_name, grade_id=grade_id)

            if stu:
                msg = '班级中学生名字不能重复！！'

                return render_template('student/student_edit.html', msg=msg)

            student = Student()

        student.s_name = s_name
        student.s_sex = s_sex
        student.grade_id = grade_id

        student.save()