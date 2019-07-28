# crdb.py

import sqlite3

conn = sqlite3.connect('database1.db')
print ('成功连接数据库')

conn.execute('drop table if exists entries')
conn.execute('create table entries (id integer primary key autoincrement,title string, text string)')
conn.execute("insert into entries(title,text) values('第1条','起床锻炼')")
conn.commit()

print ('创建成功');

conn.close()