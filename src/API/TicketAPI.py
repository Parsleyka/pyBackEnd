from flask import jsonify, request, Blueprint
from src.database.tables import *
from flask_jwt_extended import jwt_required, get_jwt_identity

tiquery = Blueprint('tiquery', __name__)


@tiquery.route("/ticket/<int:event_id>", methods=['GET'])
@jwt_required()
def get_tickets(event_id):
    try:
        tickets = Ticket.query.filter(Ticket.id_event == event_id)
        if not tickets:
            return 'Invalid ID supplied', 402

        serialised = []
        for ticket in tickets:
            serialised.append({
                'id': ticket.id,
                'price': float(ticket.price),
                'status': ticket.status
            })
        return jsonify(serialised), 200
    except Exception:
        return 'Unsuccessful operation', 403


@tiquery.route('/ticket', methods=['POST'])
@jwt_required()
def post_ticket():
    try:
        user_id = get_jwt_identity()
        user = User.query.filter(User.id == user_id).first()
        if not user.permissions == 'admin':
            return 'Do not have permissions', 401

        new_ticket = Ticket(**request.json)
        new_ticket.status = 'valid'
        session.add(new_ticket)
        session.commit()
        session.close()

        return 'Successful operation', 200
    except Exception:
        return 'Unsuccessful operation', 403


@tiquery.route('/ticket/buy/<int:ticket_id>', methods=['POST'])
@jwt_required()
def post_new_bought_ticket(ticket_id):
    try:
        user_id = get_jwt_identity()

        ticket = Ticket.query.filter(Ticket.id == ticket_id).first()
        if not ticket:
            return 'Invalid ID supplied', 401

        if ticket.status == 'bought':
            return 'Ticket is bought', 402

        if ticket.status == 'reserved':
            reserved_ticket = ReservedTicket.query.filter(ReservedTicket.id_ticket == ticket_id).first()
            if not reserved_ticket.id_user == user_id:
                return 'Ticket is reserved', 405
            session.delete(reserved_ticket)
            session.commit()

        new_bought_ticket = BoughtTicket(id_ticket=ticket_id, id_user=user_id)
        session.add(new_bought_ticket)

        ticket.status = 'bought'

        session.commit()
        session.close()

        return 'Successful operation', 200
    except Exception:
        return 'Unsuccessful operation', 403


@tiquery.route('/ticket/reserve/<int:ticket_id>', methods=['POST'])
@jwt_required()
def post_reserved_ticket(ticket_id):
    try:
        user_id = get_jwt_identity()

        ticket = Ticket.query.filter(Ticket.id == ticket_id).first()
        if not ticket:
            return 'Invalid ID supplied', 401

        if not ticket.status == 'valid':
            return 'Ticket is invalid', 402

        new_reserved_ticket = ReservedTicket(id_ticket=ticket_id, id_user=user_id)
        session.add(new_reserved_ticket)

        ticket.status = 'reserved'

        session.commit()
        session.close()

        return 'Successful operation', 200
    except Exception:
        return 'Unsuccessful operation', 403


@tiquery.route('/fixticket/<int:ticket_id>', methods=['PUT'])
@jwt_required()
def put_ticket(ticket_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.filter(User.id == user_id).first()
        if not user.permissions == 'admin':
            return 'Do not have permissions', 401

        params = request.json

        item = Ticket.query.filter(Ticket.id == ticket_id).first()
        if not item:
            return "Invalid ID supplied", 402

        for key, value in params.items():
            setattr(item, key, value)

        session.commit()
        session.close()

        return 'Successful operation', 200
    except Exception:
        return 'Unsuccessful operation', 403


@tiquery.route('/ticket/reserve/cancel/<int:ticket_id>', methods=['DELETE'])
@jwt_required()
def delete_reserved_ticket(ticket_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.filter(User.id == user_id).first()
        reserved_ticket = ReservedTicket.query.filter(ReservedTicket.id_user == user.id and
                                                      ReservedTicket.id_ticket == ticket_id).first()

        if not reserved_ticket:
            return 'You do not have reservation', 402

        ticket = Ticket.query.filter(Ticket.id == ticket_id).first()
        ticket.status = 'valid'

        session.delete(reserved_ticket)
        session.commit()
        session.close()

        return 'Successful operation', 200
    except Exception:
        return 'Unsuccessful operation', 403
