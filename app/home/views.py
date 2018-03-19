#coding=utf-8


from . import home
from flask import render_template, redirect, url_for, session, request, flash, jsonify
from functools import wraps
from app import getConn


def home_login_req(f):
    """
    访问控制装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'account' not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@home.route('/')
def index():
    # 渲染并返回 home/index.html 页面
    return render_template('home/index.html')


@home.route('/login/', methods=['GET', 'POST'])
def login():
    """
    用户登录
    """
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        db = getConn()
        cursor = db.cursor()
        sql = 'select id, account, password, username from user where account="%s"' %account
        try:
            cursor.execute(sql)
        except:
            err_msg = u'服务器内部错误，登录失败，请重新登录'
        else:
            value = cursor.fetchone()
            if not value:  # 判断用户是否存在
                err_msg = u'账号不存在'
            else:
                columns = ('id', 'account', 'password', 'username')
                user = dict(zip(columns, value))
                if user['password'] == password:  # 判断密码是否正确
                    del user['password']
                    for key in user:
                        session[key] = user[key]
                    err_msg = ''
                else:
                    err_msg = u'密码错误'
        db.close()
        return jsonify({'err_msg': err_msg})
    else:
        return render_template('home/login.html')
 

@home.route('/logout/')
@home_login_req
def logout():
    """
    退出
    """
    columns = ('id', 'account', 'password', 'username')
    for column in columns:
        session.pop(column, None)
    return redirect(url_for('home.login'))


@home.route('/user/', methods=['GET', 'POST'])
@home_login_req
def user():
    if request.method == 'POST':
        """
        对数据进行验证
        对数据进行验证
        对数据进行验证
        对数据进行验证
        对数据进行验证
        """
        user_id = request.form['user_id']
        telephone = request.form['telephone']
        qq = request.form['qq']
        db = getConn()
        cursor = db.cursor()
        sql = 'update user set telephone="%s", qq="%s" where id="%s"' %(telephone, qq, user_id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            err_msg = u'服务器内部错误，保存个人信息失败，请重试'
        else:
            err_msg = ''
        db.close()
        return jsonify({'err_msg': err_msg})
    else:
        account = session['account']
        db = getConn()
        cursor = db.cursor()
        sql = '''select id, account, username, education, grade, score, fund, telephone, qq from user
                 where account="%s"''' %account
        try:
            cursor.execute(sql)
        except:
            user = None
        else:
            user = cursor.fetchone()
            columns = ('id', 'account', 'username', 'education', 'grade', 'score', 'fund', 'telephone', 'qq')
            user = dict(zip(columns, user))
        db.close()
        return render_template('home/user.html', user=user)  


@home.route('/pwd/', methods=['GET', 'POST'])
@home_login_req
def pwd_edit():
    """
    修改密码
    """
    """
    对输入的字段进行验证
    对输入的字段进行验证
    对输入的字段进行验证
    对输入的字段进行验证
    """
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        db = getConn()
        cursor = db.cursor()
        sql = 'select password from user where id=%s'%(session['id'])
        try:
            cursor.execute(sql)
        except:
            err_msg = u'服务器内部错误，修改密码失败，请重试'
        else:
            password = cursor.fetchone()[0]
            if password != old_password:
                err_msg = u'旧密码错误'
            else:
                sql = 'update user set password="%s" where id="%s"'%(new_password, session['id'])
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                    err_msg = u'服务器内部错误，修改密码失败，请重试'
                else:
                    err_msg = ''
        db.close()
        return jsonify({'err_msg': err_msg})
    else:
        return render_template('home/pwd.html')


@home.route('/score/')
@home_login_req
def score():
    """
    得分记录页面
    """
    db = getConn()
    cursor = db.cursor()
    sql = '''select value, summary, detail, update_time from scorelog
             where user_id="%s" 
             order by update_time DESC''' %session['id']
    try:
        cursor.execute(sql)
    except:
        pass
    else:
        logs = []
        columns = ('value', 'summary', 'detail', 'update_time')
        for item in cursor.fetchall():
            logs.append(dict(zip(columns, item)))
    db.close()
    return render_template('home/score.html', logs = logs)


@home.route('/fund/')
@home_login_req
def fund():
    """
    额度记录页面
    """
    db = getConn()
    cursor = db.cursor()
    sql = '''select value, summary, detail, update_time from fundlog
             where user_id="%s" 
             order by update_time DESC''' %session['id']
    try:
        cursor.execute(sql)
    except:
        pass
    else:
        logs = []
        columns = ('value', 'summary', 'detail', 'update_time')
        for item in cursor.fetchall():
            logs.append(dict(zip(columns, item)))
    db.close()
    return render_template('home/fund.html', logs = logs)


@home.route('/score/<int:id>')
@home_login_req
def admin_score(id=None):
    """
    得分记录页面
    """
    db = getConn()
    cursor = db.cursor()
    sql = '''select value, summary, detail, update_time from scorelog
             where user_id="%s" 
             order by update_time DESC''' %id
    try:
        cursor.execute(sql)
    except:
        pass
    else:
        logs = []
        columns = ('value', 'summary', 'detail', 'update_time')
        for item in cursor.fetchall():
            logs.append(dict(zip(columns, item)))
    db.close()
    return render_template('home/score.html', logs = logs)


@home.route('/fund/<int:id>')
@home_login_req
def admin_fund(id=None):
    """
    额度记录页面
    """
    db = getConn()
    cursor = db.cursor()
    sql = '''select value, summary, detail, update_time from fundlog
             where user_id="%s" 
             order by update_time DESC''' %id
    try:
        cursor.execute(sql)
    except:
        pass
    else:
        logs = []
        columns = ('value', 'summary', 'detail', 'update_time')
        for item in cursor.fetchall():
            logs.append(dict(zip(columns, item)))
    db.close()
    return render_template('home/fund.html', logs = logs)
