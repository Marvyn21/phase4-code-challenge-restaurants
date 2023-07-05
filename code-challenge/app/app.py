#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [
        {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }
        for hero in heroes
    ]
    return jsonify(hero_list)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        powers = [
            {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }
            for power in hero.powers
        ]
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': powers
        }
        return jsonify(hero_data)
    else:
        return jsonify({'error': 'Hero not found'}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [
        {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        for power in powers
    ]
    return jsonify(power_list)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.json
        description = data.get('description')
        try:
            power.description = description
            db.session.commit()
            return jsonify({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        except ValueError as e:
            return jsonify({'errors': [str(e)]}), 400
    else:
        return jsonify({'error': 'Power not found'}), 404

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    try:
        hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
        db.session.add(hero_power)
        db.session.commit()

        hero = Hero.query.get(hero_id)
        powers = [
            {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }
            for power in hero.powers
        ]

        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': powers
        }
        return jsonify(hero_data), 201
    except ValueError as e:
        return jsonify({'errors': [str(e)]}), 400

if __name__ == '__main__':
    app.run(port=5555)

