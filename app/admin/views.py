# coding=utf8
from . import admin
from flask import render_template, redirect, url_for, request, jsonify, session, flash
from app import getConn
from functools import wraps
import re


def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_super' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    """
    登录
    """
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        # =================================
        # 服务器端 account password 格式验证
        # 
        # 
        # =================================
        db = getConn()
        cursor = db.cursor()
        sql = 'select id, account, password, username, is_super, create_time from admin where account="%s"' %account
        try:
            cursor.execute(sql)
        except:
            err_msg = u'服务器内部错误'
        else:
            value = cursor.fetchone()
            if not value:
                err_msg = u'用户名不存在'  
            else:
                columns = ('id', 'account', 'password', 'username', 'is_super', 'create_time')
                user = dict(zip(columns, value))
                if user['password'] == password:
                    err_msg = ''
                    for key in user:
                        session[key] = user[key]
                else:
                    err_msg = u'密码错误'
        return jsonify({'err_msg': err_msg})
        db.close()
    else:
        return render_template('admin/login.html')


@admin.route('/logout/')
@admin_login_req
def logout():
    """
    退出
    """
    keys = ('id', 'account', 'password', 'username', 'is_super', 'create_time')
    for key in keys:
        # Flask 中的 session 基于字典类型实现，调用 session.pop() 方法时会返回调用时传入的键对应的值，如果键并不存在，那么返回第二个参数 
        session.pop(key, None)
    return redirect(url_for('admin.login'))


@admin.route('/')
@admin_login_req
def index():
    """
    主页
    """
    db = getConn()
    cursor = db.cursor()
    sql = 'select id, account, username, score, fund from user'
    try:
        cursor.execute(sql)
    except:
        pass
    else:
        users = []
        columns = ('id', 'account', 'username', 'score', 'fund')
        for item in cursor.fetchall():
            users.append(dict(zip(columns, item)))
    db.close()
    return render_template('admin/index.html', users = users)


@admin.route('/user/add/', methods=['GET', 'POST'])
@admin_login_req
def user_add():
    """
    添加成员
    """
    if request.method == 'POST':
        """
        对各个字段的验证
        对各个字段的验证
        对各个字段的验证
        对各个字段的验证
        """
        print(request.form)
        account = request.form['account']
        username = request.form['username']
        password = request.form['password']
        init_score = int(request.form['init_score'])
        init_fund = int(request.form['init_fund'])
        education = request.form['education']
        grade = request.form['grade']
        db = getConn()
        cursor = db.cursor()
        sql = 'select * from user where account="%s"' %account
        try:
            cursor.execute(sql)
        except:
            err_msg = u'服务器内部错误，添加成员失败，请重试'
        else:
            value = cursor.fetchone()
            if value:
                err_msg = u'账号已存在'
            else:
                sql = '''insert into user(account, username, password, education, score, fund, grade)
                         values ('%s', '%s', '%s', '%s', '%s', '%s', '%s');''' %(account, username, password, education, init_score, init_fund, grade)
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    err_msg = u'服务器内部错误，添加成员失败，请重试'
                    db.rollback()
                else:
                    err_msg = ''
        db.close()
        return jsonify({'err_msg': err_msg})
    else:
        return render_template('admin/user_add.html')


@admin.route('/user/list/')
@admin_login_req
def user_list():
    """
    成员列表
    """
    db = getConn()
    cursor = db.cursor()
    sql = 'select id, account, username, education, grade, telephone, qq from user'
    try:
        cursor.execute(sql)
    except:
        pass
    else:
        users = []
        columns = ('id', 'account', 'username', 'education', 'grade', 'telephone', 'qq')
        for item in cursor.fetchall():
            users.append(dict(zip(columns, item)))
    db.close()
    return render_template('admin/user_list.html', users=users)


@admin.route('/score/edit/<int:user_id>', methods=['GET'])
@admin.route('/score/edit/', methods=['POST'])
@admin_login_req
def score_edit(user_id=None):
    """
    修改分数
    """
    if request.method == 'POST':
        """
        验证 edit_score 字段的格式
        验证 edit_score 字段的格式
        验证 edit_score 字段的格式
        """
        db = getConn()
        cursor = db.cursor()
        edit_score = int(request.form['edit_score'])
        user_id = request.form['userid']
        tag = request.form['tag']
        reason = request.form['reason']
        if request.form['option'] == '1':  # 减分
            edit_score = -edit_score
        user_sql = 'update user set score=score+%s where id="%s"' %(edit_score, user_id)
        scorelog_sql = 'insert into scorelog(user_id, value, summary, detail) values ("%s", "%s", "%s", "%s")' %(user_id, edit_score, tag, reason)
        try:
            cursor.execute(user_sql)
            cursor.execute(scorelog_sql)
            db.commit()
        except:
            db.rollback()
            err_msg = u'服务器内部错误，修改分数失败，请重试'
        else:
            err_msg = ''
        db.close()
        return jsonify({'err_msg': err_msg})
    else:
        db = getConn()
        cursor = db.cursor()
        sql = 'select id, account, username, score from user where id="%s"' %user_id
        try:
            cursor.execute(sql)
        except:
            pass
        else:
            user = cursor.fetchone()
            columns = ('id', 'account', 'username', 'score')
            user = dict(zip(columns, user))
        db.close()
        return render_template('admin/score_edit.html', user=user)


@admin.route('/fund/edit/<int:user_id>', methods=['GET'])
@admin.route('/fund/edit/', methods=['POST'])
@admin_login_req
def fund_edit(user_id=None):
    """
    修改额度
    """
    if request.method == 'POST':
        """
        验证 edit_fund 字段的格式
        验证 edit_fund 字段的格式
        验证 edit_fund 字段的格式
        """
        db = getConn()
        cursor = db.cursor()
        edit_fund = int(request.form['edit_fund'])
        user_id = request.form['userid']
        tag = request.form['tag']
        reason = request.form['reason']
        if request.form['option'] == '1':  # 扣除额度
            edit_fund = -edit_fund
        user_sql = 'update user set fund=fund+%s where id="%s"' %(edit_fund, user_id)
        fundlog_sql = 'insert into fundlog(user_id, value, summary, detail) values ("%s", "%s", "%s", "%s")' %(user_id, edit_fund, tag, reason)
        try:
            cursor.execute(user_sql)
            cursor.execute(fundlog_sql)
            db.commit()
        except:
            db.rollback()
            err_msg = u'服务器内部错误，修改额度失败，请重试'
        else:
            err_msg = ''
        db.close()
        return jsonify({'err_msg': err_msg})
    else:
        db = getConn()
        cursor = db.cursor()
        sql = 'select id, account, username, fund from user where id="%s"' %user_id
        try:
            cursor.execute(sql)
        except:
            pass
        else:
            user = cursor.fetchone()
            columns = ('id', 'account', 'username', 'fund')
            user = dict(zip(columns, user))
        db.close()
        return render_template('admin/fund_edit.html', user=user)


@admin.route('/user/delete/', methods=['POST'])
@admin_login_req
def user_delete():
    """
    删除用户
    """
    db = getConn()
    cursor = db.cursor()
    user_id = request.form['user_id']
    sql = 'delete from user where id="%s"' %user_id
    try:
        cursor.execute(sql)
        db.commit()
    except:
        err_msg = u'服务器内部错误，删除用户失败，请重试'
        db.rollback()
    else:
        err_msg = ''
    db.close()
    return jsonify({'err_msg': err_msg})



@admin.route('/pwd/', methods=['GET', 'POST'])
@admin_login_req
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
        sql = 'select password from admin where id=%s'%(session['id'])
        try:
            cursor.execute(sql)
        except:
            err_msg = u'服务器内部错误，修改密码失败，请重试'
        else:
            password = cursor.fetchone()[0]
            if password != old_password:
                err_msg = u'旧密码错误'
            else:
                sql = 'update admin set password="%s" where id="%s"'%(new_password, session['id'])
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
        return render_template('admin/pwd.html')
