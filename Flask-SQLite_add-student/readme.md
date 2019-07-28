[TOC]

## 简介


### 结构
```
$ tree -I "__pycache*|*.pyc" -FCL 3
.
|-- database.db
|-- models.py
|-- templates/
|   |-- home.html
|   |-- list.html
|   |-- result.html
|   `-- students.html
`-- views.py
```
### 展示

#### 1. 主页

![](https://img2018.cnblogs.com/blog/720033/201907/720033-20190718114619823-875159732.png)

#### 2. 学生信息查看


![](https://img2018.cnblogs.com/blog/720033/201907/720033-20190718114634500-669078233.png)


#### 3. 添加学生信息

![](https://img2018.cnblogs.com/blog/720033/201907/720033-20190718114652463-2107114005.png)


### 技术

- Flask – SQLite的使用
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
print ('成功连接数据库')

conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
conn.commit()

print ('创建成功')
conn.close()
```


### views视图

```
from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/enternew')
def new_student():
    return render_template('students.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    """添加成员"""
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute(
                    "INSERT INTO students(name, addr, city, pin) VALUES(?, ?, ?, ?)", (nm, addr, city, pin))

                con.commit()
                msg = "添加成功"
        except:
            con.rollback()
            msg = "添加失败"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    """查询"""
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
```

### models模块

```
import sqlite3 as lite


class Database():

    def __init__(self, db='database.db'):

        self.con = lite.connect(db, check_same_thread=False)
        self.cur = self.con.cursor()

    def create_students(self):
        """创建表单"""
        with self.con:
            sql = """create table students(
                        id integer primary key autoincrement,
                        name TEXT not null,
                        addr TEXT not null,
                        city TEXT,
                        pin TEXT)"""
            self.cur.execute("DROP TABLE IF EXISTS students")
            self.cur.execute(sql)

    def insert_students(self, name, addr, city, pin):
        """插入用户信息"""
        with self.con:
            sql = "INSERT INTO students(name, addr, city, pin) VALUES(?, ?, ?, ?)"
            self.cur.execute(sql, (name, addr, city, pin))


if __name__ == '__main__':
    db = Database('database.db')
    db.create_students()
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
    <h1><a href = "/list">查看学生信息</a></h1>
    
    <br>
    <h1><a href = "/enternew">添加学生信息</a></h1>
</body>
</html>
```

### list列表页
```
<!doctype html>
<html>
   <body>
       <h1>学生表</h1>
       <hr>
      <table border = 1>
         <thead>
            <td>姓名</td>
            <td>地址</td>
            <td>城市</td>
            <td>区号</td>
         </thead>
         
         {% for row in rows %}
            <tr>
               <td>{{row["name"]}}</td>
               <td>{{row["addr"]}}</td>
               <td> {{ row["city"]}}</td>
               <td>{{row['pin']}}</td>  
            </tr>
         {% endfor %}
      </table>
      <br>
      <a href = "/">返回主页</a>
   </body>
</html>
```

### result消息结果页

```
<!doctype html>
<html>
   <body>
      <h3>添加结果 : {{ msg }}</h3><br>
      <h2><a href = "\">返回主页</a></h2>
   </body>
</html>
```

### studentst添加成员
```
<html>
   <body>
      <form action = "{{ url_for('addrec') }}" method = "POST">
         <h3>学生信息</h3>
         姓名<br>
         <input type = "text" name = "nm" /></br><br>
         
         地址<br>
         <textarea name = "add" ></textarea><br><br>
         
         城市<br>
         <input type = "text" name = "city" /><br><br>
         
         区号<br>
         <input type = "text" name = "pin" /><br><br>
         
         <input type = "submit" value = "输入" /><br>
      </form>
   </body>
</html>
```