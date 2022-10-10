from email.policy import default
from enum import unique
from time import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(5000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(3000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    BlogPost_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(35), nullable=False)
    blog_posts = db.relationship('BlogPost')
    comments = db.relationship('Comment')