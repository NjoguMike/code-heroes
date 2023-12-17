from flask_sqlalchemy import SQLAlchemy, func, validates
from sqlalchemy import DateTime, func


db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)
    created_at = db.Column(DateTime(), server_default=func.now())
    updated_at = db.Column(DateTime(), server_default=func.now())

    powers = db.relationship('Hero_Powers', backref='hero_powers.powers')

class Powers(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(DateTime(), server_default=func.now())
    updated_at = db.Column(DateTime(), server_default=func.now())
    

@validates('description')
def validate_description(sef,key,value):
    if len(value) < 20:
        raise ValueError("Description must be atleast 20 characters in length")
    return value

class Hero_Powers(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.Foreignkey("heroes.id"), primary_key=True)
    power_id = db.Column(db.Integer, db.Foreignkey("powers.id"), primary_key=True)
    created_at = db.Column(DateTime(), server_default=func.now())
    updated_at = db.Column(DateTime(), server_default=func.now())

    powers = db.relationship('Powers')
    heroes = db.relationship('Hero')

@validates('strength')
def validate_description(sef,key,value):
    if value not in ['strong','weak','average']:
        raise ValueError("Please insert a valid strength value")
    return value

# add any models you may need. 