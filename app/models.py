from flask_sqlalchemy import SQLAlchemy, func
from sqlalchemy import DateTime, func


db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)
    created_at = db.Column(DateTime(), server_default=func.now())
    updated_at = db.Column(DateTime(), server_default=func.now())

class Powers(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(DateTime(), server_default=func.now())
    updated_at = db.Column(DateTime(), server_default=func.now())

class Hero_Powers(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, primary_key=True)
    power_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(DateTime(), server_default=func.now())
    updated_at = db.Column(DateTime(), server_default=func.now())

# add any models you may need. 