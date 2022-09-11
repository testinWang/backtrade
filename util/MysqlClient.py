#!/usr/bin/env python
# _*_coding:utf-8_*_
import pymysql
import traceback
from util.LoadConfig import get_conf


class MysqlClient(object):
    """
    执行sql语句类
    """
    # 单例模式
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化mysql配置
        :param platform_name:
        """
        self.sql_conf = get_conf('mysql')
        self.connect_db()

    def connect_db(self):
        """
        连接mysql
        :return:
        """
        host = str(self.sql_conf['host'])
        user = str(self.sql_conf['user'])
        pwd = str(self.sql_conf['password'])
        db = self.sql_conf['database']
        port = int(self.sql_conf['port'])
        try:
            self.conn = pymysql.connect(host=host,
                                        user=user,
                                        password=pwd,
                                        db=db,
                                        port=port,
                                        charset="utf8",
                                        autocommit=True)
        except Exception as e:
            print("连接mysql失败：{0}".format(e))
        # self.conn = pymysql.connect(host=host, user=user, password=pwd, db=db, port=port, charset="utf8")

    def get_cursor(self):
        """
        获取游标
        :return:
        """
        self.cursor=self.conn.cursor()
        return self.cursor

    def exec_sql(self, sql_type, sql, val=None):
        """
        执行sql语句
        :param sql_type:
        :param sql:
        :param val: 一次插入多条数据时使用
        :return:
        """
        result = None
        try:
            if sql_type == 'select_one':
                self.connect_db()
                cursor = self.get_cursor()
                cursor.execute(sql)
                result = cursor.fetchone()
            elif sql_type == 'select_list':
                self.connect_db()
                cursor = self.get_cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
            elif sql_type == 'update' or sql_type == 'del' or sql_type == 'insert_one':
                self.connect_db()
                result = self.get_cursor().execute(sql)
            elif sql_type == 'insert_many':
                self.connect_db()
                result = self.get_cursor().executemany(sql, tuple(val))

            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            return result
        except Exception as e:
            traceback.print_exc()



if __name__ == '__main__':
    test = MysqlClient()
    sql = 'select max(dt) from date_k where code = 1232333'
    a=test.exec_sql(sql_type='select_one', sql=sql)
    print(a)
    print(a[0])