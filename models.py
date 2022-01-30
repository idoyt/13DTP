from os import path
from app import db, app

# GET - GET, POST - ADD, PUT - UPDATE,  DELETE - DELETE


class Post(db.Model):
    __tablename__ = ''

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    post = db.Column(db.Text, nullable=False)



