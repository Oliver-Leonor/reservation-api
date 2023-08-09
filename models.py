from datetime import datetime, timedelta
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import func
from extensions import db

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservation_datetime = db.Column(db.DateTime, nullable=False)
    reservation_first_name = db.Column(db.String(100), nullable=False)
    reservation_last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    number_of_guests = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Reservation {self.id} - {self.reservation_first_name} {self.reservation_last_name}>'

    @hybrid_method
    def reservations_in_time_slot(cls, datetime):
        return db.session.query(func.count(cls.id)).filter(cls.reservation_datetime == datetime).scalar()
    
    @hybrid_property
    def is_editable(self):
        return datetime.utcnow() <= self.reservation_datetime - timedelta(days=2)

    @hybrid_property
    def is_deletable(self):
        return datetime.utcnow() <= self.reservation_datetime - timedelta(days=2)

    
    def serialize(self):
        return {
            'id': self.id,
            'reservation_datetime': self.reservation_datetime.isoformat() if self.reservation_datetime else None,
            'reservation_first_name': self.reservation_first_name,
            'reservation_last_name': self.reservation_last_name,
            'phone_number': self.phone_number,
            'number_of_guests': self.number_of_guests,
            'is_editable': self.is_editable,
            'is_deletable': self.is_deletable
        }
