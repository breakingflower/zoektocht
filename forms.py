from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileAllowed

from wtforms.validators import DataRequired

class AnswerForm(FlaskForm):

    answer = StringField('Antwoord', validators=[DataRequired()])
    submit = SubmitField('Ga door')

class ImageForm(FlaskForm): 

    picture = FileField('Foto', validators=[FileAllowed(['png', 'jpeg', 'jpg'])])
    submit = SubmitField('Ga door')