from flask import Blueprint, render_template, jsonify, request
from app.models import Room, Reservation
from flask_login import current_user
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/rooms')
def rooms():
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)

@bp.route('/api/rooms')
def get_rooms():
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms])

@bp.route('/api/check-availability', methods=['POST'])
def check_availability():
    data = request.get_json()
    check_in = datetime.strptime(data['check_in'], '%Y-%m-%d').date()
    check_out = datetime.strptime(data['check_out'], '%Y-%m-%d').date()
    room_id = data['room_id']

    # Check if room is available for the given dates
    conflicting_reservations = Reservation.query.filter(
        Reservation.room_id == room_id,
        Reservation.status != 'cancelled',
        ((Reservation.check_in_date <= check_in) & (Reservation.check_out_date > check_in)) |
        ((Reservation.check_in_date < check_out) & (Reservation.check_out_date >= check_out))
    ).first()

    return jsonify({'available': not bool(conflicting_reservations)}) 