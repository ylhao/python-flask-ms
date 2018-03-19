#coding=utf8


import pymysql
from models import Models


# 数据库配置
DB = {
    'user': 'xxx',
    'passwd': 'xxx',
    'db': 'score',
    'host': '127.0.0.1',
    'port': 3306,
    'charset':'utf8'
}


def getConn():
    """
    获取数据库连接
    """
    conn = pymysql.connect(host=DB['host'], port=DB['port'], user=DB['user'],
                            passwd=DB['passwd'], db=DB['db'], charset=DB['charset'])
    return conn


def create_db():
    """
    创建数据表
    """
    db = getConn()
    cursor = db.cursor()
    for item in Models:
        cursor.execute(item)
    print('create tables success!')
