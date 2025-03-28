# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField
from wtforms.validators import InputRequired,DataRequired
from wtforms import FileField
from flask_wtf.file import FileRequired,FileAllowed

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description =TextAreaField('Description', validators=[DataRequired()])
    poster= FileField('Poster', validators=[FileAllowed(['jpg','jpeg', 'jfif', 'png', 'gif'], 'Images only')])
