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

