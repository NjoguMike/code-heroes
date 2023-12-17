#!/usr/bin/env python3
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Hero, Powers, Hero_Powers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

CORS(app)

mash = Marshmallow(app)


class HeroesSchema(mash.SQLAlchemySchema):

    class meta:
        model = Hero

    id = mash.auto_field()
    name = mash.auto_field()
    super_name = mash.auto_field()

    url = mash.HyperlinkRelated(
        {
            "self": mash.URLFor(
                "heroesbyid", values=dict(id="<id>")),
            "collection":mash.URLFor("heores")
        }
    )

hero_schema = HeroesSchema()
heroes_schema = HeroesSchema(many=True)


api = Api(app)

@app.route('/')
def home():
    return "Welcome to the Home of SuperHeroes"

class Heroes(Resource):

    def get(self):

        heroes = Hero.query.all()
        response = make_response(
            heroes_schema.dump(heroes) ,
            200
        )
        return response

api.add_resource('/heroes', Heroes)

class HeroesbyId(Resource):

    def get(self,id):

        hero = Hero.query.filter_by(id=id).first()

        response = make_response(
            hero_schema.dump(hero) ,
            200
        )
        return response

api.add_resource('/heroes/<int:id>', Heroes)


if __name__ == '__main__':
    app.run(port=5555)
