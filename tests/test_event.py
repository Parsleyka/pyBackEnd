import pytest
import requests
from sqlalchemy import desc

from src.database.tables import Event, session

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


def test_event_get():
    res = requests.get(url + '/event')

    assert res.status_code == 200


def test_event_post():
    bd_size = len(Event.query.filter().all())

    user_access_token = login_as_user()
    user_auth = {'Authorization': 'Bearer ' + user_access_token}
    res = requests.post(url + '/event', headers=user_auth, json={"date": "0000-00-00 00:00:00",
                                                                 "description": "test",
                                                                 "location": "test",
                                                                 "name": "test"})
    assert res.status_code == 401

    admin_access_token = login_as_admin()
    admin_auth = {'Authorization': 'Bearer ' + admin_access_token}
    res_2 = requests.post(url + '/event', headers=admin_auth, json={"date": "0000-00-00 00:00:00",
                                                                    "description": "test",
                                                                    "location": "test",
                                                                    "name": "test"})
    session.commit()

    assert res_2.status_code == 200

    bd_size_after = len(session.query(Event).filter().all())
    assert bd_size_after == bd_size + 1


def test_event_put():
    access_token = login_as_admin()
    auth = {'Authorization': 'Bearer ' + access_token}

    event_all = session.query(Event).order_by(desc(Event.id)).all()
    event = event_all[0]

    res = requests.put(url + f'/event/{event.id}', headers=auth, json={"date": "0000-00-00 00:00:00",
                                                                       "description": "success",
                                                                       "location": "test",
                                                                       "name": "test"})
    session.commit()
    assert res.status_code == 200

    event_all = session.query(Event).order_by(desc(Event.id)).all()
    event = event_all[0]
    assert event.description == "success"


def test_event_delete():
    bd_size = len(Event.query.filter().all())

    event = Event.query.filter(Event.name == 'test').first()

    user_access_token = login_as_user()
    user_auth = {'Authorization': 'Bearer ' + user_access_token}

    res = requests.delete(url + '/event/' + str(event.id), headers=user_auth)
    assert res.status_code == 401

    access_token = login_as_admin()
    auth = {'Authorization': 'Bearer ' + access_token}

    res_2 = requests.delete(url + '/event/' + str(event.id), headers=auth)
    session.commit()
    assert res_2.status_code == 200

    bd_size_after = len(session.query(Event).filter().all())
    assert bd_size_after == bd_size - 1
