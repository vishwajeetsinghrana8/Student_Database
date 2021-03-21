import os
from forms import AddForm, DelForm, AddFatherForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = "knowledgeshelf"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app,db)

######Models######
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    father = db.relationship('Father',backref='student',uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.father:
            return f"Student name is {self.name}, id is {self.id} and father name is {self.father.name}."
        else:
            return f"Student name is {self.name}, id is {self. id} and father name is not available."

class Father(db.Model):
    __tablename__ = 'fathers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def  __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def __repr__(self):
        return f"Father name: {self.name}"


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add_father',methods=['GET','POST'])
def add_father():

    form = AddFatherForm()

    if form.validate_on_submit():
        name = form.name.data
        stu_id = form.stu_id.data

        new_father = Father(name, stu_id)
        db.session.add(new_father)
        db.session.commit()

        return redirect(url_for('list_student'))
    return render_template('add_father.html', form=form)

@app.route('/add',methods=['GET','POST'])
def add_student():

    form = AddForm()

    if form.validate_on_submit():

        name = form.name.data

        new_student = Student(name)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('list_student'))

    return render_template('add.html', form=form)

@app.route('/list')
def list_student():

    students = Student.query.all()
    return render_template('list.html', students=students)

@app.route('/delete',methods=['GET','POST'])
def del_student():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('list_student'))

    return render_template('delete.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)