#!/usr/bin/env python3
from flask import Flask, make_response
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from models import db, Hero, Power, Hero_Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

mash = Marshmallow(app)
api = Api(app)

class HeroSchema(mash.SQLAlchemySchema):

    class Meta:
        model = Hero

    id = mash.auto_field()
    name = mash.auto_field()
    super_name = mash.auto_field()
    powers = mash.auto_field()

    url = mash.Hyperlinks(
        {
            "self":mash.URLFor(
                "heroesbyid",
                values=dict(id="<id>"))
        }
    )

hero_schema = HeroSchema()

class HeroesSchema(mash.SQLAlchemySchema):

    class Meta:
        model = Hero

    id = mash.auto_field()
    name = mash.auto_field()
    super_name = mash.auto_field()

    url = mash.Hyperlinks(
        {
            "collection":mash.URLFor("heroes")
        }
    )
heroes_schema = HeroesSchema(many=True)

class PowerSchema(mash.SQLAlchemySchema):

    class Meta:
        model = Power

    id = mash.auto_field()
    name = mash.auto_field()
    description = mash.auto_field()

    url = mash.Hyperlinks(
        {
            "self":mash.URLFor(
                "powersbyid",
                values=dict(id="<id>"))
        }
    )

power_schema = PowerSchema()

class PowersSchema(mash.SQLAlchemySchema):

    class Meta:
        model = Power

    id = mash.auto_field()
    name = mash.auto_field()
    description = mash.auto_field()

    url = mash.Hyperlinks(
        {
            "collection":mash.URLFor("powers")
        }
    )
powers_schema = PowersSchema(many=True)

class Index(Resource):

    def get(self):
        
        response = make_response(
            "Welcome to the Home of SuperHeroes",
            200
        )

        return response

api.add_resource(Index, '/')


class Heroes(Resource):

    def get(self):

        heroes = Hero.query.all()
        response = make_response(
            heroes_schema.dump(heroes),
            200
        )
        return response

api.add_resource(Heroes,'/heroes')

class HeroesbyId(Resource):

    def get(self,id):

        hero = Hero.query.filter_by(id=id).first()

        if hero:

            response = make_response(
                hero_schema.dump(hero),
                200
            )
            return response
        else:
            return make_response({"error": "Hero not found"}, 404)
        

api.add_resource(HeroesbyId, '/heroes/<int:id>')

class Powers(Resource):

    def get(self):

        power= Power.query.all()
        response = make_response(
            powers_schema.dump(power),
            200
        )
        return response

api.add_resource(Powers,'/powers')

class PowersById(Resource):

    def get(self,id):

        power = Power.query.filter_by(id=id).first()

        if power:
            response = make_response(
                power_schema.dump(power),
                200
            )
            return response
        else:
            return make_response({"error": "Power not found"}, 404)
        

api.add_resource(PowersById, '/powers/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
