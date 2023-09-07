# folder.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from init_db import db


class Folder(db.Model):
    __tablename__ = 'folders'
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120), nullable=False)
    folder = db.Column(db.String(120),unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
