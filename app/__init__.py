#coding=utf-8


from flask import Flask, render_template
from .common import getConn, create_db


# 定义 Flask 应用
app = Flask(__name__)


# 加载配置项
app.config['SECRET_KEY'] = 'd7361dff5b8e4df5b06d37cc296d4a6e'

# 开启调试模式
# app.debug = True

# 导入蓝图
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

# 注册蓝图
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")

# 404 处理
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
