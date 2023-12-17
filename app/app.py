#!/usr/bin/env python3
from flask import Flask, make_response
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from models import db, Hero, Powers, Hero_Powers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

mash = Marshmallow(app)
api = Api(app)

class HeroesSchema(mash.SQLAlchemySchema):

    class Meta:
        model = Hero

    id = mash.auto_field()
    name = mash.auto_field()
    super_name = mash.auto_field()

    url = mash.Hyperlinks(
        {
            "self":mash.URLFor(
                "heroesbyid",
                values=dict(id="<id>")),
            "collection":mash.URLFor("heroes")
        }
    )

hero_schema = HeroesSchema()
heroes_schema = HeroesSchema(many=True)

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

        response = make_response(
            hero_schema.dump(hero),
            200
        )
        return response

api.add_resource(HeroesbyId, '/heroes/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
