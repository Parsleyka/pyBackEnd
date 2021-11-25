from flask_restful import Resource
from flask import jsonify, request, Blueprint
from src.database.tables import *
from flask_jwt_extended import jwt_required, get_jwt_identity

evquery = Blueprint('evquery', __name__)


class EventAPI(Resource):
    def get(self):
        try:
            events = Event.query.all()
            serialised = []
            for event in events:
                serialised.append({
                    'id': event.id,
                    'name': event.name,
                    'description': event.description,
                    'location': event.location,
                    'date': event.date
                })
            return jsonify(serialised), 200
        except Exception:
            return jsonify('Unsuccessful operation'), 403

    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            user = User.query.filter(User.id == user_id).first()
            if not user.permissions == 'admin':
                return jsonify('Do not have permissions'), 401

            new_event = Event(**request.json)
            session.add(new_event)
            session.commit()
            session.close()
            return jsonify('Successful operation'), 200
        except Exception:
            return jsonify('Unsuccessful operation'), 403


class EventParamAPI(Resource):
    @jwt_required()
    def put(self, event_id):
        try:
            user_id = get_jwt_identity()
            user = User.query.filter(User.id == user_id).first()
            if not user.permissions == 'admin':
                return jsonify('Do not have permissions'), 401

            params = request.json
            item = Event.query.filter(Event.id == event_id).first()
            if not item:
                return jsonify("Invalid ID supplied"), 402

            for key, value in params.items():
                setattr(item, key, value)
            session.commit()
            session.close()

            return jsonify('Successful operation'), 200
        except Exception:
            return jsonify('Unsuccessful operation'), 403

    @jwt_required()
    def delete(self, event_id):
        try:
            user_id = get_jwt_identity()
            user = User.query.filter(User.id == user_id).first()
            if not user.permissions == 'admin':
                return jsonify('Do not have permissions'), 401

            item = Event.query.filter(Event.id == event_id).first()
            if not item:
                return jsonify('Invalid ID supplied'), 402

            session.delete(item)
            session.commit()
            session.close()

            return jsonify('Successful operation'), 200
        except Exception:
            return jsonify('Unsuccessful operation'), 403


evquery.add_url_rule('/event', view_func=EventAPI.as_view("eventAPI"))
evquery.add_url_rule('/event/<int:event_id>', view_func=EventParamAPI.as_view("eventParamAPI"))
