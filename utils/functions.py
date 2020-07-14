
# ======================================================
# @Author  :   Daniel                 
# @Time    :   2020.6.20
# @Desc    :   App创建、初始化
# ======================================================

import os

import redis
from flask import Flask

from App.user_views import user_bp
from App.models import db


def create_app():
    # 定义系统路径,当前文件目录
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    # 定义静态文件路径
    static_dir = os.path.join(BASE_DIR, 'static')
    # 定义模板目录
    templates_dir = os.path.join(BASE_DIR, 'templates')

    # 初始化app
    app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)

    # 注册蓝图
    app.register_blueprint(blueprint=user_bp, url_prefix='/user')

    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123456@127.0.0.1:3306/sms'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 设置session秘钥，用于和session内容生成hash值，防止内容被串改
    app.config['SECRET_KEY'] = 'secret_key'
    # 设置session存储库， 使用redis
    app.config['SESSION_TYPE'] = 'redis'
    # 连接redis
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379, db=1)

    # 初始化db
    db.init_app(app=app)

    return app



