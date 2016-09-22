# -*- coding: utf-8 -*-
from flask import Blueprint  # 导入蓝图


main = Blueprint('main', __name__)  # 实例化Blueprint类对象,'main'蓝本的名字, 蓝本所在的包和模块,使用__name__就行


from . import views, errors  # 避免循环导入依赖,因为在views.py和errors.py还要导入蓝本main
from ..models import Permission


@main.app_context_processor
def inject_permissions():  # 为了避免每次调用render_template()时多添加一个模板参数，可以使用上下文处理器，上下文处理器能让变量在所有模板中全局可访问
    return dict(Permission=Permission)


