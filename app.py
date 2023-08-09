from flask import Flask
from flask_restful import Api
from resources import ReservationResource
from extensions import db, migrate
from flask_cors import CORS # type: ignore

def create_app():
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress modification tracking warning

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
     db.create_all()

    api.add_resource(ReservationResource, '/api/reservations', '/api/reservations/<int:reservation_id>')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
