from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):

    name = StringField("Name of Student: ")
    submit = SubmitField("Add Student:")

class DelForm(FlaskForm):

    id = IntegerField("Id no. of student to remove: ")
    submit = SubmitField("Remove Student: ")

class AddFatherForm(FlaskForm):
    name = StringField("Name of Father: ")
    stu_id = IntegerField("Id of Student:")
    submit = SubmitField("Add Student")