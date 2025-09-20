from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

class Farmer(UserMixin, db.Model):
    __tablename__ = 'farmers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    land_size = db.Column(db.Float, nullable=False)
    preferred_crops = db.Column(db.String(200))  # Comma separated crops
    password = db.Column(db.String(128), nullable=False)
    
    # Relationship with Advisory table
    advisory_history = db.relationship('Advisory', backref='farmer', lazy=True)

class Advisory(db.Model):
    __tablename__ = 'advisories'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    crop = db.Column(db.String(100))
    recommendation = db.Column(db.Text)
    fertilizer_guidance = db.Column(db.Text)
    pest_control_guidance = db.Column(db.Text)
