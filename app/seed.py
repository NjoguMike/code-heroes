from models import Hero, Power, Hero_Power, db
from app import app
import random
from faker import Faker

with app.app_context():

  Hero.query.delete()
  Power.query.delete()
  Hero_Power.query.delete()
  db.session.commit()

  fake = Faker()

  strengths = ["Strong", "Weak", "Average"]

  powers = ['stretch', "super_speed", "super_strength", "thunder", "fistman"]
  s_names = ['elastic', "flashy", "thor", "thunder_bolt", "the_fister"]

  power_list = []
  for item in powers:
    power = Power(name=random.choice(powers) , description=fake.sentence())
    power_list.append(power)

    db.session.add(power)
    db.session.commit()

  heroes_list = []
  for person in range(10):
    hero = Hero(name=fake.name() , super_name=random.choice(s_names))
    heroes_list.append(hero)

    db.session.add(hero)
    db.session.commit()

  status = ['strong','weak','average']
  for hp in range(10):
    hero_powers = Hero_Power(strength=random.choice(status), heroes_id=random.choice(heroes_list).id,  powers_id=random.choice(power_list).id)

    db.session.add(hero_powers)
    db.session.commit()
