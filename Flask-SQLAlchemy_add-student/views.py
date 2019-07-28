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
