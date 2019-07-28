[toc]

## 介绍 Flaskr


### 功能

博客应用称为 flaskr，有如下功能：

1. 允许用户用配置文件里指定的凭证登入登出。只支持一个用户。
2. 当用户登入后，可以向页面添加条目。条目标题是纯文本，正文可以是一些 HTML 。因信任这里的用户，这部分 HTML 不做审查。
3. 页面倒序显示所有条目（后来居上），并且用户登入后可以在此添加新条目。


### 技术

- Flask – SQLite的使用
- flask中表单数据的传递

### 运行效果

```
python .\views.py
```
![](https://img2018.cnblogs.com/blog/720033/201907/720033-20190728104542351-1764145869.png)
![](https://img2018.cnblogs.com/blog/720033/201907/720033-20190728104616733-1712815923.png)
![](https://img2018.cnblogs.com/blog/720033/201907/720033-20190728104633589-1213995461.png)



## 文件结构


```
$ tree -I "__pycache*|*.pyc" -FCL 3
.
|-- app.py
|-- crdb.py
|-- database.db
|-- readme.md
|-- static/
|   `-- style.css
`-- templates/
    |-- layout.html
    |-- login.html
    `-- show_entries.html
```



## 数据库

1. cmd命令窗口运行：
```
> sqlite3 database.db
sqlite> drop table if exists entries;
sqlite> drop table if exists entries;
sqlite> create table entries (id integer primary key autoincrement,title string, text string);
sqlite> insert into entries(title,text) values('第1条','起床锻炼');
sqlite> insert into entries(title,text) values('第2条','回来洗澡');
sqlite> insert into entries(title,text) values('第3条','去吃早餐');
sqlite> .quit
```
2. 或者脚本`crdb.py`


```
# crdb.py

import sqlite3

conn = sqlite3.connect('database.db')
print ('成功连接数据库')

conn.execute('drop table if exists entries')
conn.execute('create table entries (id integer primary key autoincrement,title string, text string)')
conn.execute("insert into entries(title,text) values('第1条','起床锻炼')")
conn.commit()

print ('创建成功');

conn.close()
```

## 代码`app.py`

`app.py`
```
# -*- coding: utf-8 -*-


from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import sqlite3


app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = 'This is a secret'   #会话必用
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'pass'

DATABASE = 'data.db'

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
```

## 基础页`layout.html`


```
<!doctype html>
<title>Flaskr</title>
<link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
<div class=page>
  <h1>Flask小项目</h1>
  <div class=metanav>
  {% if not session.logged_in %}
    <a href="{{ url_for('login') }}">登陆</a>
  {% else %}
    <a href="{{ url_for('logout') }}">退出</a>
  {% endif %}
  </div>
  {% for message in get_flashed_messages() %}
    <div class=flash>{{ message }}</div>
  {% endfor %}
  {% block body %}{% endblock %}
</div>
```



## 登陆页`login.html`


```
{% extends "layout.html" %}
{% block body %}
  <h2>登陆</h2>
  {% if error %}<p class=error><strong>Error:</strong> {{ error }}{% endif %}
  <form action="{{ url_for('login') }}" method=post>
    <dl>
      <dt>用户名:
      <dd><input type=text name=username>
      <dt>密码:
      <dd><input type=password name=password>
      <dt><br>
      <dd><input type=submit value=输入>
    </dl>
  </form>
{% endblock %}
```



## 展示页`show_entries.html`


```
{% extends "layout.html" %}
{% block body %}
  {% if session.logged_in %}
    <form action="{{ url_for('add_entry') }}" method=post class=add-entry>
      <dl>
        <dt>标题:
        <dd><input type=text size=30 name=title>
        <dt>文本:
        <dd><textarea name=text rows=5 cols=40></textarea>
        <dd><input type=submit value=发布>
      </dl>
    </form>
  {% endif %}
  <ul class=entries>
  {% for entry in entries %}
    <li><h2>{{ entry.title }}</h2>{{ entry.text|safe }}
  {% else %}
    <li><em>Unbelievable.  No entries here so far</em>
  {% endfor %}
  </ul>
{% endblock %}
```

## 样式`style.css`

```
body            { font-family: sans-serif; background: #eee; }
a, h1, h2       { color: #377BA8; }
h1, h2          { font-family: 'Georgia', serif; margin: 0; }
h1              { border-bottom: 2px solid #eee; }
h2              { font-size: 1.2em; }

.page           { margin: 2em auto; width: 35em; border: 5px solid #ccc;
                  padding: 0.8em; background: white; }
.entries        { list-style: none; margin: 0; padding: 0; }
.entries li     { margin: 0.8em 1.2em; }
.entries li h2  { margin-left: -1em; }
.add-entry      { font-size: 0.9em; border-bottom: 1px solid #ccc; }
.add-entry dl   { font-weight: bold; }
.metanav        { text-align: right; font-size: 0.8em; padding: 0.3em;
                  margin-bottom: 1em; background: #fafafa; }
.flash          { background: #CEE5F5; padding: 0.5em;
                  border: 1px solid #AACBE2; }
.error          { background: #F0D6D6; padding: 0.5em; }
```

## 参考

[flask教程](http://docs.jinkan.org/docs/flask/tutorial/index.html)