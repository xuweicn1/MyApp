# -*- coding: utf-8 -*-


from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import sqlite3


app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = 'This is a secret'   #会话必用
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'pass'

DATABASE = 'database.db'

def connect_db():
    """新建连接"""
    return sqlite3.connect(DATABASE)


@app.before_request
def before_request():
    """每次请求前获取连接"""
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """每次请求后关闭连接"""
    g.db.close()


@app.route('/')
def show_entries():
    """字典形式返回查询结果"""
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    """添加新内容"""
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('成功发布说说')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """登陆判定"""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = '用户名错误'
        elif request.form['password'] != app.config['PASSWORD']:
            error = '密码错误'
        else:
            session['logged_in'] = True
            flash('登陆成功')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """退出"""
    session.pop('logged_in', None)
    flash('你已经退出')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':

    app.run(debug=True)
