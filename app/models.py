# app/models.py
from . import db
from datetime import datetime

class Produce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)
    storage_zone = db.Column(db.String(50), nullable=False)
    packaging_type = db.Column(db.String(50), nullable=False)
    shelf_life_days = db.Column(db.Integer, nullable=False)

class TraceabilityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produce_id = db.Column(db.Integer, db.ForeignKey('produce.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
