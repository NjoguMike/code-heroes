from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    powers = db.relationship('Hero_Power' , back_populates="hero")

    def __repr__(self):
        return f"Hero(id={self.id}, name={self.name}, super_name={self.super_name})"

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    heroes = db.relationship('Hero_Power' , back_populates="power")

    def __repr__(self):
        return f"Power(id={self.id}, name={self.name}, description={self.description})"
    

@validates('description')
def validate_description(sef,key,value):
    if len(value) < 20:
        raise ValueError("Description must be atleast 20 characters in length")
    return value

class Hero_Power(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())
    heroes_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    powers_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    
    hero = db.relationship('Hero' , back_populates="powers")
    power = db.relationship('Power' , back_populates="heroes")

    def __repr__(self):
        return f"Hero_Power(id={self.id}, strength={self.strength}, hero_id={self.hero_id}, power_id={self.power_id})"

@validates('strength')
def validate_description(sef,key,value):
    if value not in ['strong','weak','average']:
        raise ValueError("Please insert a valid strength value")
    return value

# add any models you may need. 