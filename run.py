'''
auth:canhun
'''
from flask import Flask,make_response

app = Flask(__name__)
#载入配置文件
app.config.from_object('config')
print(app.config['DEBUG'])

''' 路由注册第一种方式'''
@app.route('/hello/')
def hello():
    # return 'Hello,CanHun'
    headers = {
        'Content-type':'text/plain',
        'charset':'utf - 8',
        'location': 'http://www.bing.com'
    }
    return '<h1>Hello,CanHun</h1>',404  ,headers

    # response = make_response('<h1>Hello,CanHun</h1>', 404)
    # response.headers = headers
    # return response


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=app.config['DEBUG'])


''' 路由注册第一种方式'''
# @app.route('/hello/')
'''路由注册第二种方式'''
# app.add_url_rule('/hello/',view_func= hello)
'''
启动方法
app.run(debug=True)
    1) debug模式启动,只能通过127.0.0.1 和 localhost 访问
    2) 可通过制定host app.run(host='0.0.0.0',debug=True)
    3) 制定端口
'''