# '''
# auth:canhun
# '''
# from flask import Flask,make_response
#
# app = Flask(__name__)
# #载入配置文件
# app.config.from_object('config')
# print(app.config['DEBUG'])
#
# ''' 路由注册第一种方式'''
# @app.route('/hello/')
# def hello():
#     # return 'Hello,CanHun'
#     headers = {
#         'Content-type':'text/plain',
#         'charset':'utf - 8',
#         'location': 'http://www.bing.com'
#     }
#     return '<h1>Hello,CanHun</h1>',404  ,headers
#
#     # response = make_response('<h1>Hello,CanHun</h1>', 404)
#     # response.headers = headers
#     # return response
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0',port=5000,debug=app.config['DEBUG'])
#
#
# ''' 路由注册第一种方式'''
# # @app.route('/hello/')
# '''路由注册第二种方式'''
# # app.add_url_rule('/hello/',view_func= hello)
# '''
# 启动方法
# app.run(debug=True)
#     1) debug模式启动,只能通过127.0.0.1 和 localhost 访问
#     2) 可通过制定host app.run(host='0.0.0.0',debug=True)
#     3) 制定端口
# '''
#
import datetime
import time
import requests
import pandas as pd
from sqlalchemy import create_engine

#建立数据库连接  设置字符集为UTF8
engine = create_engine("mysql+mysqldb://{}:{}@{}/{}?charset=utf8".format('hexl', '123456', '192.168.0.100:3306', 'mydb'),max_overflow=5,encoding='utf-8')
conn = engine.connect()

headers = {
'Host': 'www.kuaidaili.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
}

'''爬取快代理部分'''
# url_list = ['https://www.kuaidaili.com/free/inha/%s'%i for i in range(1,2600)] + ['https://www.kuaidaili.com/free/intr/%s'%i for i in range(1,2600)]
# i = 1
# for url in url_list:
# # url = 'https://www.kuaidaili.com/free/inha/1'
#     try:
#         resp = requests.get(url,headers=headers)
#         # print(resp.text)
#         df = pd.DataFrame(pd.read_html(resp.text)[0])
#         df_ip_info = df[['IP','PORT','类型','最后验证时间']]
#         df_ip_info.rename(columns={'类型':'type','最后验证时间':'check_time'},inplace=True)
#         df_ip_info['source'] = 'kuaidaili'
#         df_ip_info['load_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         # print(df_ip_info.columns)
#         df_ip_info.to_sql('ip_info',con=conn,if_exists='append', index=False)
#         print('第%s页写入完成'%i)
#         i += 1
#         time.sleep(1)
#     except:
#         print('第%s页写入失败' % i)
'''爬取西刺代理部分'''
url_list = ['https://www.xicidaili.com/nt/%s'%i for i in range(1,700)]
i=1
for url in url_list:
# url = 'https://www.kuaidaili.com/free/inha/1'
    try:
        resp = requests.get(url, headers=headers)
        df = pd.DataFrame(pd.read_html(resp.text)[0])[1:]
        df_ip_info = df[[1, 2, 5, 9]]
        df_ip_info.rename(columns={1: 'ip', 2: 'port', 5: 'type', 9: 'check_time'}, inplace=True)
        df_ip_info['source'] = 'xici'
        df_ip_info['load_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(df_ip_info.columns)
        df_ip_info.to_sql('ip_info',con=conn,if_exists='append', index=False)
        print('第%s页写入完成'%i)
        time.sleep(2)
    except:
        print('第%s页写入失败' % i)
    finally:
        i += 1




