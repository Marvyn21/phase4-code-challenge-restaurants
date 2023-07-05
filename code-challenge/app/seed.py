import random
from app import db, Hero, Power, HeroPower

powers = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
]

heroes = [
    {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    {"name": "Doreen Green", "super_name": "Squirrel Girl"},
    {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
    {"name": "Janet Van Dyne", "super_name": "The Wasp"},
    {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
    {"name": "Carol Danvers", "super_name": "Captain Marvel"},
    {"name": "Jean Grey", "super_name": "Dark Phoenix"},
    {"name": "Ororo Munroe", "super_name": "Storm"},
    {"name": "Kitty Pryde", "super_name": "Shadowcat"},
    {"name": "Elektra Natchios", "super_name": "Elektra"}
]

strengths = ["Strong", "Weak", "Average"]

# Seeding powers
print("🦸‍♀️ Seeding powers...")
power_ids = []
for power in powers:
    power_obj = Power(name=power["name"], description=power["description"])
    db.session.add(power_obj)
    db.session.commit()
    power_ids.append(power_obj.id)

# Seeding heroes
print("🦸‍♀️ Seeding heroes...")
for hero in heroes:
    hero_obj = Hero(name=hero["name"], super_name=hero["super_name"])
    db.session.add(hero_obj)
    db.session.commit()

# Adding powers to heroes
print("🦸‍♀️ Adding powers to heroes...")
all_heroes = Hero.query.all()
for hero in all_heroes:
    num_powers = random.randint(1, 3)
    for _ in range(num_powers):
        power_id = random.choice(power_ids)
        strength = random.choice(strengths)
        hero_power = HeroPower(hero_id=hero.id, power_id=power_id, strength=strength)
        db.session.add(hero_power)
        db.session.commit()

print("🦸‍♀️ Done seeding!")
