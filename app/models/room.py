from app import db
from datetime import datetime

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # e.g., 'Single', 'Double', 'Suite', 'Riad Suite'
    price_per_night = db.Column(db.Float, nullable=False)  # Price in MAD (Moroccan Dirham)
    capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    amenities = db.Column(db.Text)  # Stored as comma-separated values
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reservations = db.relationship('Reservation', backref='room', lazy=True)

    def __repr__(self):
        return f'<Room {self.number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'type': self.type,
            'price_per_night': self.price_per_night,
            'capacity': self.capacity,
            'description': self.description,
            'amenities': self.amenities.split(',') if self.amenities else [],
            'is_available': self.is_available,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        } 