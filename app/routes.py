# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import Produce, TraceabilityLog
from . import db
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/inventory')
def inventory():
    produce = Produce.query.all()
    return render_template('inventory.html', produce=produce)

@main.route('/api/receive', methods=['POST'])
def receive_produce():
    data = request.json
    produce = Produce(
        name=data['name'],
        source=data['source'],
        quantity=data['quantity'],
        storage_zone=data['storage_zone'],
        packaging_type=data['packaging_type'],
        shelf_life_days=data['shelf_life_days']
    )
    db.session.add(produce)
    db.session.commit()
    
    log = TraceabilityLog(produce_id=produce.id, action='Received')
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': 'Produce received successfully', 'produce_id': produce.id}), 201

@main.route('/api/shelf-life/<int:produce_id>', methods=['GET'])
def get_shelf_life(produce_id):
    produce = Produce.query.get_or_404(produce_id)
    received_date = produce.received_at
    shelf_life_end_date = received_date + timedelta(days=produce.shelf_life_days)
    
    remaining_days = (shelf_life_end_date - datetime.utcnow()).days
    
    if remaining_days < 0:
        status = "expired"
    elif remaining_days == 0:
        status = "expires today"
    else:
        status = f"expires in {remaining_days} days"
    
    return jsonify({
        'produce_id': produce.id,
        'name': produce.name,
        'shelf_life_end_date': shelf_life_end_date,
        'status': status
    }), 200
