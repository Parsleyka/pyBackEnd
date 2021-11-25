from flask import jsonify, request, Blueprint
from src.database.tables import *
from flask_jwt_extended import jwt_required, get_jwt_identity

uquery = Blueprint('uquery', __name__)


@uquery.route('/user/create', methods=['POST'])
def reg_user():
    try:
        params = request.json
        user = User(**params)
        session.add(user)
        session.commit()
        session.close()
        return jsonify('Successful operation'), 200
    except Exception:
        return jsonify('Unsuccessful operation'), 403


@uquery.route('/user/login', methods=['POST'])
def auth_user():
    try:
        params = request.json
        user = User.authentication(**params)
        token = user.get_token()
        return {'access_token': token}, 200
    except Exception:
        return jsonify('Unsuccessful operation'), 403


@uquery.route('/user/<string:nickname>', methods=['PUT'])
@jwt_required()
def update_user(nickname):
    try:
        user_id = get_jwt_identity()

        user = User.query.filter(User.id == user_id).first()
        if not user:
            return jsonify("Invalid ID supplied"), 401

        if not user.nickname == nickname:
            return jsonify('It is not your account'), 404

        params = request.json

        for key, value in params.items():
            setattr(user, key, value)

        session.commit()
        session.close()
        return jsonify('Successful operation'), 200
    except Exception:
        return jsonify('Unsuccessful operation'), 403


@uquery.route('/user/<string:nickname>', methods=['DELETE'])
@jwt_required()
def delete_user(nickname):
    try:
        user_id = get_jwt_identity()
        user = User.query.filter(User.id == user_id).first()
        if not user.permissions == 'admin':
            return jsonify('Do not have permissions'), 401

        user_to_delete = User.query.filter(User.nickname == nickname).first()
        if not user_to_delete:
            return jsonify('Invalid ID supplied'), 402

        session.delete(user_to_delete)
        session.commit()
        session.close()
        return jsonify('Successful operation'), 200
    except Exception:
        return jsonify('Unsuccessful operation'), 403
