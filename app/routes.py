from flask import Blueprint, request, jsonify
from app import db
from app.models import Hero, Power, HeroPower

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

@bp.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    
    return jsonify(hero.to_dict(include_powers=True))

@bp.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@bp.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    
    return jsonify(power.to_dict())

@bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    
    data = request.get_json()
    if not data or 'description' not in data:
        return jsonify({'errors': ['Description is required']}), 400
    
    try:
        power.description = data['description']
        db.session.commit()
        return jsonify(power.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

@bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    if not data:
        return jsonify({'errors': ['Request body is required']}), 400
    
    required_fields = ['strength', 'power_id', 'hero_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'errors': [f'{field} is required']}), 400
    
    # Check if hero and power exist
    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])
    
    if not hero:
        return jsonify({'errors': ['Hero not found']}), 404
    if not power:
        return jsonify({'errors': ['Power not found']}), 404
    
    try:
        hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        
        db.session.add(hero_power)
        db.session.commit()
        
        return jsonify(hero_power.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

# Error handlers
@bp.app_errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@bp.app_errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500