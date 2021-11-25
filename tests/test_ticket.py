import pytest
from sqlalchemy import desc

from src.database.tables import Ticket, ReservedTicket, BoughtTicket, session
import requests


url = 'http://127.0.0.1:5000'

ADMIN_email = "mail@mail.mail"
ADMIN_password = "root"

User_email = "user@user.user"
User_password = "user"

def login_as_admin():
    query = requests.post(url + '/user/login', json={"email": ADMIN_email, "password": ADMIN_password})
    access_token = query.json()["access_token"]
    return access_token


def login_as_user():
    query = requests.post(url + '/user/login', json={"email": User_email, "password": User_password})
    access_token = query.json()["access_token"]
    return access_token


def test_ticket_post():
    bd_size = len(Ticket.query.filter().all())

    user_access_token = login_as_user()
    user_auth = {'Authorization': 'Bearer ' + user_access_token}
    res = requests.post(url + '/ticket', headers=user_auth, json={"id_event": "1",
                                                                  "price": "000"})
    assert res.status_code == 401

    admin_access_token = login_as_admin()
    admin_auth = {'Authorization': 'Bearer ' + admin_access_token}
    res_2 = requests.post(url + '/ticket', headers=admin_auth, json={"id_event": "1",
                                                                     "price": "000"})
    session.commit()
    assert res_2.status_code == 200

    bd_size_after = len(session.query(Ticket).filter().all())
    assert bd_size_after == bd_size + 1


def test_ticket_get():
    user_access_token = login_as_user()
    user_auth = {'Authorization': 'Bearer ' + user_access_token}

    res = requests.get(url + f'/ticket/1', headers=user_auth)

    assert res.status_code == 200


def test_ticket_reserve_post():
    bd_size = len(ReservedTicket.query.filter().all())

    ticket_all = session.query(Ticket).order_by(desc(Ticket.id)).all()
    ticket = ticket_all[0]

    user_access_token = login_as_user()
    user_auth = {'Authorization': 'Bearer ' + user_access_token}
    res = requests.post(url + f'/ticket/reserve/{ticket.id}', headers=user_auth)
    session.commit()
    assert res.status_code == 200

    bd_size_after = len(session.query(ReservedTicket).filter().all())
    assert bd_size_after == bd_size + 1

    assert ticket.status == 'reserved'


def test_ticket_reserve_delete():
    bd_size = len(ReservedTicket.query.filter().all())

    ticket_all = session.query(Ticket).order_by(desc(Ticket.id)).all()
    ticket = ticket_all[0]

    user_access_token = login_as_user()
    user_auth = {'Authorization': 'Bearer ' + user_access_token}

    res = requests.delete(url + f'/ticket/reserve/cancel/{ticket.id}', headers=user_auth)
    session.commit()
    assert res.status_code == 200

    ticket_all = session.query(Ticket).filter().order_by(desc(Ticket.id)).all()
    ticket = ticket_all[0]
    assert ticket.status == "valid"

    bd_size_after = len(session.query(ReservedTicket).filter().all())
    assert bd_size_after == bd_size - 1


def test_ticket_buy_post():
    bd_size = len(BoughtTicket.query.filter().all())

    ticket_all = session.query(Ticket).order_by(desc(Ticket.id)).all()
    ticket = ticket_all[0]

    user_access_token = login_as_user()
    user_auth = {'Authorization': 'Bearer ' + user_access_token}
    res = requests.post(url + f'/ticket/buy/{ticket.id}', headers=user_auth)
    session.commit()
    assert res.status_code == 200

    bd_size_after = len(session.query(BoughtTicket).filter().all())
    assert bd_size_after == bd_size + 1

    assert ticket.status == 'bought'

    bought_ticket = session.query(BoughtTicket).order_by(desc(BoughtTicket.id)).first()
    session.delete(bought_ticket)
    session.commit()


def test_ticket_put():
    access_token = login_as_admin()
    auth = {'Authorization': 'Bearer ' + access_token}

    ticket_all = session.query(Ticket).order_by(desc(Ticket.id)).all()
    ticket = ticket_all[0]

    res = requests.put(url + f'/fixticket/{ticket.id}', headers=auth, json={"id_event": "1",
                                                                            "price": "999"})
    session.commit()
    assert res.status_code == 200

    ticket_all = session.query(Ticket).filter().order_by(desc(Ticket.id)).all()
    ticket = ticket_all[0]

    assert ticket.price == 999

    ticket = session.query(Ticket).order_by(desc(Ticket.id)).first()
    session.delete(ticket)
    session.commit()
