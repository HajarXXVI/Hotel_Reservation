from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import Room, Reservation, User
from app import db
from functools import wraps
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need to be an admin to access this page.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/rooms', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_rooms():
    if request.method == 'POST':
        room = Room(
            number=request.form['number'],
            type=request.form['type'],
            price_per_night=float(request.form['price_per_night']),
            capacity=int(request.form['capacity']),
            description=request.form['description'],
            description_fr=request.form['description_fr'],
            description_ar=request.form['description_ar'],
            amenities=request.form['amenities'],
            view_type=request.form['view_type'],
            floor=int(request.form.get('floor', 1)),
            size_sqm=float(request.form['size_sqm']),
            has_balcony='has_balcony' in request.form,
            has_air_conditioning='has_air_conditioning' in request.form,
            has_heating='has_heating' in request.form,
            has_wifi='has_wifi' in request.form,
            smoking_allowed='smoking_allowed' in request.form
        )
        db.session.add(room)
        try:
            db.session.commit()
            flash('Room added successfully')
        except Exception as e:
            db.session.rollback()
            flash('Error adding room: Room number might be duplicate')
        return redirect(url_for('admin.manage_rooms'))
    
    rooms = Room.query.all()
    return render_template('admin/rooms.html', 
                         rooms=rooms,
                         room_types=Room.get_room_types(),
                         view_types=Room.get_view_types())

@bp.route('/reservations')
@login_required
@admin_required
def manage_reservations():
    reservations = Reservation.query.all()
    return render_template('admin/reservations.html', reservations=reservations)

@bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/api/room/<int:room_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
@admin_required
def manage_room(room_id):
    room = Room.query.get_or_404(room_id)
    
    if request.method == 'DELETE':
        db.session.delete(room)
        db.session.commit()
        return jsonify({'message': 'Room deleted successfully'})
    
    if request.method == 'GET':
        return jsonify(room.to_dict())
    
    data = request.get_json()
    for key, value in data.items():
        if hasattr(room, key):
            setattr(room, key, value)
    
    db.session.commit()
    return jsonify(room.to_dict()) 