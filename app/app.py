#!/usr/bin/env python3
from flask import Flask, make_response , request
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

class Hero_PowerSchema(mash.SQLAlchemySchema):

    class Meta:
        model = Hero_Power

    id = mash.auto_field()
    strength = mash.auto_field()
    powers_id = mash.auto_field()
    heroes_id = mash.auto_field()

    url = mash.Hyperlinks(
        {
            "collection":mash.URLFor("hero_powers")
        }
    )
hero_powers_schema = Hero_PowerSchema(many=True)

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
        
    def patch(self, id):
        
        power = Power.query.filter_by(id=id).first()

        if power:

            try:
                for attr in request.get_json():
                    setattr(power, attr, request.get_json()[attr])
                    db.session.commit()

                    response = make_response(
                        power_schema.dump(power),
                        201
                    )
                    return response

            except ValueError:
                response = make_response(
                    power_schema.dump({"errors": ["validation errors"]}),
                    401
                )
                return response
            
        else:
            return make_response({"error": "Power not found"}, 404)


api.add_resource(PowersById, '/powers/<int:id>')

class Hero_Powers(Resource):

    def post(self):

        data = request.get_json()

        try:

            new_heroItem = Hero_Power(
                strength = data["strength"],
                powers_id = data["powers_id"],
                heroes_id = data["heroes_id"],
            )
            db.session.add(new_heroItem)
            db.session.commit()

            response = make_response(
                powers_schema.dump(Hero.query.filter_by(id=new_heroItem.id).first()),
                201
            )
            return response

        except ValueError:
            response = make_response(
                power_schema.dump({"errors": ["validation errors"]}),
                401
            )
            return response

api.add_resource(Hero_Powers,'/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
