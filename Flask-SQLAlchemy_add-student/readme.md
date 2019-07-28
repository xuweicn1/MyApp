[toc]

## 简介

[翻译：Flask – SQLAlchemy](https://www.tutorialspoint.com/flask/flask_sqlalchemy.htm)

### 结构
```
$ tree -I "__pycache*|*.pyc" -FCL 3
.
|-- database.db
|-- readme.md
|-- templates/
|   |-- addnew.html
|   |-- home.html
|   `-- show_all.html
`-- views.py

```
### 展示

#### 1. 主页


![](https://img2018.cnblogs.com/blog/720033/201907/720033-20190719214954510-95842715.png)
#### 2. 学生信息查看

![](https://img2018.cnblogs.com/blog/720033/201907/720033-20190719215106361-986697090.png)

#### 3. 添加学生信息

![](https://img2018.cnblogs.com/blog/720033/201907/720033-20190719215214766-1723489616.png)


### 技术

- Flask – SQLAlchemy的使用
- flask中表单数据的传递

### 运行

```
python .\views.py
```


## 代码

### 创建数据库表单

```
# crdb.py

import sqlite3

conn = sqlite3.connect('database.db')
print "Opened database successfully";

conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print "Table created successfully";
conn.close()
```


### views视图

```
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
    # __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin


@app.route('/')
def home():
    """主页"""

    return render_template('home.html')


@app.route('/show_all')
def show_all():
    """展示所有"""
    data = Student.query.all()
    return render_template('show_all.html', students=data)


@app.route('/addnew', methods=['GET', 'POST'])
def addnew():
    """添加新成员"""
    if request.method == 'POST':

        f_name = request.form['name']
        f_city = request.form['city']
        f_addr = request.form['addr']
        f_pin = request.form['pin']

        if not f_name or not f_city or not f_addr:
            flash('请填入必要项')
        else:
            stuinfo = Student(f_name, f_city, f_addr, f_pin)
            db.session.add(stuinfo)
            db.session.commit()
            flash('添加成功')
            return redirect(url_for('show_all'))
    return render_template('addnew.html')


if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    app.run(debug=True)

```

### home主页

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>主页</title>
</head>
<body>
    <h1><a href = "/show_all">查看学生信息</a></h1>
    
    <br>
    <h1><a href = "/addnew">添加学生信息</a></h1>
</body>
</html>
```

### 添加成员addnew.html
```
<!DOCTYPE html>
<html>
   <body>
      <h3>学生信息表</h3>
      <hr/>
      
      {%- for category, message in get_flashed_messages(with_categories = true) %}
         <div class = "alert alert-danger">
            {{ message }}
         </div>
      {%- endfor %}
      
      <form action = "{{ request.path }}" method = "post">
         <label for = "name">姓名</label><br>
         <input type = "text" name = "name" placeholder = "张三" /><br><br>

         <label for = "city">城市</label><br>
         <input type = "text" name = "city" placeholder = "北京" /><br><br>

         <label for = "addr">地址</label><br>
         <textarea name = "addr" placeholder = "朝阳区大望路"></textarea><br><br>

         <label for = "PIN">邮编</label><br>
         <input type = "text" name = "pin" placeholder = "100000" /><br><br>

         <input type = "submit" value = "输入" />
      </form>
      <h3><a href="{{ url_for('home') }}">返回主页</a></h3>
   </body>
</html>
```

### 展示页show_all

```
<!DOCTYPE html>
<html lang="en">

<head></head>

<body>


   <h2> 学生表</h2>
   <hr>
   <h3><a href="{{ url_for('addnew') }}">添加新成员</a></h3>
   <table border="1">
      <thead>
         <tr>
            <th>姓名</th>
            <th>城市</th>
            <th>地址</th>
            <th>邮编</th>
         </tr>
      </thead>

      <tbody>
         {% for student in students %}
         <tr>
            <td>{{ student.name }}</td>
            <td>{{ student.city }}</td>
            <td>{{ student.addr }}</td>
            <td>{{ student.pin }}</td>
         </tr>
         {% endfor %}
      </tbody>
   </table>
   <br>

   

   <h3>消息提示</h3>
   <div class="widget-content" style="height: 100px;width:50%;border:1px solid #ccc;">
      消息通知：
      {%- for message in get_flashed_messages() %}
      {{ message }}
      {%- endfor %}

   </div>
   <br>

   <h3><a href="{{ url_for('home') }}">返回主页</a></h3>

</body>

</html>
```
