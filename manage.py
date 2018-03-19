#coding=utf-8


from app import app, create_db
from flask_script import Manager


manager = Manager(app)


@manager.command
def run():
    """
    启动服务
    """
    app.run()


@manager.command
def deploy():
    """
    部署项目
    """
    create_db()


if __name__ == "__main__":
    manager.run()
