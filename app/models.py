from app import db
from sqlalchemy.orm import validates

class Hero(db.Model):
    __tablename__ = 'heroes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)
    
    # Relationships
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')
    powers = db.relationship('Power', secondary='hero_powers', back_populates='heroes', viewonly=True)
    
    def to_dict(self):
        hero_dict = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }
        return hero_dict
    
    def to_dict_with_powers(self):
        hero_dict = self.to_dict()
        hero_dict['hero_powers'] = [hp.to_dict() for hp in self.hero_powers]
        return hero_dict

class Power(db.Model):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    # Relationships
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')
    heroes = db.relationship('Hero', secondary='hero_powers', back_populates='powers', viewonly=True)
    
    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise ValueError('Description must be present')
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id', ondelete='CASCADE'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id', ondelete='CASCADE'), nullable=False)
    
    # Relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')
    
    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError(f'Strength must be one of: {", ".join(valid_strengths)}')
        return strength
    
    def to_dict(self):
        return {
            'id': self.id,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'strength': self.strength,
            'hero': self.hero.to_dict() if self.hero else None,
            'power': self.power.to_dict() if self.power else None
        }