#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import sys

'''
数据库存入数据慢

参数				            默认值		 修改值	          备注
max_allowed_packet		    4194304(4M)	 1048576(1M)	  当前值大于建议值不修改
bulk_insert_buffer_size	    8388608(8M)	 125829120(120M)	
Net_buffer_length		    16384(16k)	 8192(8K）	      当前值大于建议值不修改
innodb_log_buffer_size		1048576(1M)	 16777216(16M)	
innodb_autoextend_increment	64	(64B)	 1287651328(128M）	
innodb_log_file_size		50331648(48M)	1287651328(128M）	
innodb_flush_log_at_trx_commit	1			0	

修改失败时，修改配置文件：
linux下的mysql服务器,修改/etc/my.cnf
windwos下的,修改my.ini文件

innodb_flush_log_at_trx_commit   设置值   0   1   2

设置为0，可能会丢失数据
set global innodb_flush_log_at_trx_commit=0;

默认值为1 数据安全
set global innodb_flush_log_at_trx_commit=1;

设置为2，介于0、1之间
set global innodb_flush_log_at_trx_commit=2;

注：
    修好后重启数据库生效

    windows 系统

    .启动mysql：输入 net start mysql;
    .停止mysql：输入 net stop mysql;
     
     win + r

     services.msc
     在服务中找到mysql 右键选择停止  启动

    Liunx

    使用 service 启动：service mysqld restart

    使用 mysqld 脚本启动：/etc/inint.d/mysqld restart
    

'''



class SaveToSql(object):
    def __init__(self, host='localhost', user=None, password=None, db_name=None,table_name=None,charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.table_name = table_name
        self.charset = charset
        self._connect()

    def _connect(self):
        try:
            self.conn = pymysql.connect(
                host = self.host,
                user = self.user,                #数据库   用户名  root
                password = self.password,          #数据库   密码 123456
                # charset = 'utf8',
                charset = self.charset
            )

            # 获取数据库名 并判断数据是否存在
            db_names = self._get_db_names()
            if not self.db_name in db_names:
                print('没有数据库:%s' % self.db_name)
                sys.exit()
            else:
                self.conn.select_db(self.db_name)

            # 获取数据库下的表单名 并判表单是否存在
            table_names = self._get_table_names()
            if not self.table_name in table_names:
                print('没有表单:%s' % self.table_name)
                sys.exit()
            else:
                print('成功连接数据库')

        except pymysql.err.OperationalError as err:
            if err.args[0] == 1045:
                print('用户名、密码输入错误')
                sys.exit()

    def _get_db_names(self):
        with self.conn.cursor() as cur:
            sql = 'show databases;'
            cur.execute(sql)
            result = cur.fetchall()
            databases = [x[0] for x in result]
        return databases

    def _get_table_names(self):
        with self.conn.cursor() as cur:
            sql = 'show tables;'
            cur.execute(sql)
            result = cur.fetchall()
            table_name = [x[0] for x in result]
        return table_name

    def switch_db(self,db_name):
        db_names = self._get_db_names()
        if not self.db_name in db_names:
            print('没有数据库:%s' % self.db_name)
            sys.exit()
        else:
            self.conn.select_db(db_name)
            self.db_name = db_name

    def is_exist_tableName(self, db_name=None, table_name=None):
        befor_db = self.db_name
        if db_name:
            db_names = self._get_db_names()
            if not self.db_name in db_names:
                print('没有数据库:%s' % self.db_name)
                return False
            else:
                self.conn.select_db(self.db_name)

        if table_name:
            table_names = self._get_table_names()
            if not self.table_name in table_names:
                print('没有表单:%s' % self.table_name)
                sys.exit()
            else:
                self.db_name = befor_db
                return True
        if not table_name:
            return None

    def get_field_desc(self):
        with self.conn.cursor() as cur:
            sql = 'desc %s;' % self.table_name
            cur.execute(sql)
            result = cur.fetchall()
        return result

    def exec_sql(self, sql_sentence):
        return_list = ['show','desc','select']
        keyword = sql_sentence.split(' ')[0]
        with self.conn.cursor() as cur:
            cur.execute(sql_sentence)
            if not keyword in return_list:
                self.conn.commit()
            elif keyword in return_list:
                cur.execute(sql_sentence)
                result = cur.fetchall()
                return result

    def insert_one_data(self, *args):
        '''
        传参说明： 1、args数与表单中的字段一致

                  2、args传入tuple 或 list 对象
                     [(字段名，1),(字段名，2),(3,字段名3)... ...]

                  3、args可接受 一个字典对象 键值对要求
                     key为字段名
                     value为传入的字段数据
        '''
        sql = ''
        field = [x[0] for x in self.get_field_desc()]
        fieldName = []
        values = []
        if not args: raise '传参为空'

        if len(args) == len(field) or len(args[0]) == len(field):
            values = tuple(args[0])
            sql = 'insert into %s.%s values %s;' % \
                  (self.db_name, self.table_name, repr(values))

        elif isinstance(args, (list, tuple)) and isinstance(args[0], (list, tuple)) and len(args[0]) == 2:
            for x,y in args:
                if x in field:
                    fieldName.append(x)
                    values.append(y)
                elif y in field:
                    fieldName.append(y)
                    values.append(x)
                else:
                    raise '数据库:%s,表单名:%s\n不存在字段名：%s,%s' % (self.db_name,self.table_name,x,y)

            sql = 'insert into %s.%s %s values %s;' % \
                    (self.db_name, self.table_name, repr(tuple(fieldName)), repr(tuple(values)))

        elif isinstance(args, (dict)):
            fieldName, values = args.items()
            sql = 'insert into %s.%s %s values %s;' % \
                  (self.db_name, self.table_name, repr(tuple(fieldName)), repr(tuple(values)))
        if sql:
            self.exec_sql(sql)
        else:
            raise '传参异常！！！'

    def insert_emany_data(self,table_name=None ,args=[]):
        if not table_name:
            table_name = self.table_name
        field = repr(tuple([i[0] for i in self.get_field_desc()])).replace("'",'')
        batch_count = 10000
        for i in range(0,len(args)+1,batch_count):
            values = ','.join([repr(tuple(i)) for i in args[i:i+batch_count]])
            sql_sentence = 'insert into %s.%s %s values %s' % (self.db_name,table_name,field, values)
            with self.conn.cursor() as cur:
                cur.execute(sql_sentence)
                self.conn.commit()

    def clear_table_data(self, table_name):
        sql_sentence = 'DELETE FROM %s.%s;' % (self.db_name,table_name)
        self.exec_sql(sql_sentence)

import pymongo
class SaveToMongodB(object):
    def __init__(self,host='localhost', port=27017,user=None, password=None, db_name=None,collection_name=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.collection_name = collection_name
        self._connect()

    def _connect(self):
        self.client = client = pymongo.MongoClient(self.host, self.port)
        if self.password:
            client.authenticate(self.db_name, self.password)
        self.db = db = eval('client.%s' % str(self.db_name))
        collection = eval('db.%s' % str(self.collection_name))
        self.collection = collection
        print('连接Mongodb成功')

    def get_collection_names(self):
        return self.db.collection_names()

    def get_db_names(self):
        return self.client.database_names()

    def insert_data(self, data):
        if self.collection:
            self.collection.insert(data)
        else:
            print('没有集合对象')

if __name__ == '__main__':
    # sql = SaveToSql(user='root', password='123456', db_name='tongcheng58', table_name='recruitinfo')
    # sql.insert_one_data()
    # student1 = {
    #     'id': '20170101',
    #     'name': 'Jordan',
    #     'age': 20,
    #     'gender': 'male'
    # }

    # db = SaveToMongodB(db_name='stext',collection_name='kkk')
    # # db.insert_data(student1)
    # db.get_collection_names()
    # print(db.get_db_names())
    pass
