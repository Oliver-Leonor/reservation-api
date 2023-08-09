from flask_restful import Resource, reqparse
from models import Reservation
from extensions import db
from datetime import datetime

class ReservationResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('reservation_datetime', type=str, required=True, help="Date and time of reservation is required.")
    parser.add_argument('reservation_first_name', type=str, required=True, help="First name is required.")
    parser.add_argument('reservation_last_name', type=str, required=True, help="Last name is required.")
    parser.add_argument('phone_number', type=str, required=True, help="Phone number is required.")
    parser.add_argument('number_of_guests', type=int, required=True, help="Number of guests is required.")

    def get(self, reservation_id=None):
        if reservation_id:
            reservation = Reservation.query.get(reservation_id)
            if reservation:
                return reservation.serialize()
            return {"message": "Reservation not found"}, 404
        else:
            reservations = Reservation.query.all()
            return [r.serialize() for r in reservations]

    def post(self):
        data = ReservationResource.parser.parse_args()
        reservation = Reservation(
            reservation_datetime=datetime.fromisoformat(data['reservation_datetime']),
            reservation_first_name=data['reservation_first_name'],
            reservation_last_name=data['reservation_last_name'],
            phone_number=data['phone_number'],
            number_of_guests=data['number_of_guests']
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation.serialize(), 201

    def put(self, reservation_id):
        data = ReservationResource.parser.parse_args()
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            reservation.reservation_datetime = datetime.fromisoformat(data['reservation_datetime'])
            reservation.reservation_first_name = data['reservation_first_name']
            reservation.reservation_last_name = data['reservation_last_name']
            reservation.phone_number = data['phone_number']
            reservation.number_of_guests = data['number_of_guests']
            db.session.commit()
            return reservation.serialize()
        return {"message": "Reservation not found"}, 404


    def delete(self, reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            db.session.delete(reservation)
            db.session.commit()
            return {"message": "Reservation deleted successfully."}
        return {"message": "Reservation not found"}, 404
