# -*- coding: utf-8 -*-
"""延迟创建程序实例"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):  # 程序的工厂函数,接收一个参数,程序使用的配置名
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # 保存的配置可以使用Flask app.config配置对象提供的from_object()方法导入程序
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint  # main蓝图
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint  # auth蓝图
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app




