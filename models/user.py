from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from init_db import db

class User(db.Model):
    __tablename__ = 'Users'
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username
