from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class NoteForm(FlaskForm):
    title = StringField("标题", validators=[DataRequired(message="标题不能为空。")])
    content = TextAreaField("内容", validators=[DataRequired(message="内容不能为空。")])