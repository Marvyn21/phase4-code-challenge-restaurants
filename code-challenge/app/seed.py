from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, Hero, Power, hero_powers
fake = Faker()
with app.app_context():
    Hero.query.delete()
    Power.query.delete()
    heroes = []
    for i in range(25):
        h = Hero(
            name=fake.name(),
            super_name=fake.name(),
            description=fake.text(),
            )
        heroes.append(h)
    db.session.add_all(heroes)
    powers = []
    for i in range(25):
        p = Power(
            name= fake.name(),
            description=fake.text(),
        )
        powers.append(p)
    db.session.add_all(powers)
    combinations=set()
    strengths = ["Strong","Weak", "Average"]
    for _ in range (25):
        hero_id= randint(1,25)
        power_id= randint(1,25)
        strength = rc(strengths)
        if (hero_id, power_id, strength ) in combinations:
            continue
        combinations.add((hero_id, power_id, strength))
        hero_power_data={"hero_id":hero_id, "power_id":power_id, "strength":strength}
        statement=db.insert(hero_powers).values(hero_power_data)
        db.session.execute(statement)
        db.session.commit()
