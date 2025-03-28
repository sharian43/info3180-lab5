# Add any model classes for Flask-SQLAlchemy here

from . import db

class Movie(db.Model):

    __tablename__='movies'

    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(255))
    description= db.Column(db.Text)
    poster= db.Column(db.String(255))
    created_at= db.Column(db.DateTime,default=db.func.now(), nullable=False)

    def __init__(self,title,description,poster):
        self.title = title
        self.description = description
        self.poster = poster