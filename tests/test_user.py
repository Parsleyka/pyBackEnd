import pytest
import requests
from src.database.tables import User, session

url = 'http://127.0.0.1:5000'

ADMIN_email = "mail@mail.mail"
ADMIN_password = "root"

Test_User_email = "test@test.test"
Test_User_password = "test"


def login_as_admin():
    query = requests.post(url + '/user/login', json={"email": ADMIN_email, "password": ADMIN_password})
    access_token = query.json()["access_token"]
    return access_token


def login_as_testuser():
    query = requests.post(url + '/user/login', json={"email": Test_User_email, "password": Test_User_password})
    access_token = query.json()["access_token"]
    return access_token


def test_user_login():
    res = requests.post(url + '/user/login', json={"email": ADMIN_email, "password": ADMIN_password})
    assert res.status_code == 200


def test_user_create():
    bd_size = len(User.query.filter().all())
    res = requests.post(url + '/user/create', json={"nickname": "test",
                                                    "name": "test",
                                                    "surname": "test",
                                                    "email": Test_User_email,
                                                    "password": Test_User_password})
    session.commit()
    assert res.status_code == 200

    bd_size_after = len(session.query(User).filter().all())
    assert bd_size_after == bd_size + 1


def test_user_put():
    access_token = login_as_testuser()
    auth = {'Authorization': 'Bearer ' + access_token}
    res = requests.put(url + '/user/' + 'test', headers=auth, json={"nickname": "test",
                                                                    "name": "success",
                                                                    "surname": "test",
                                                                    "email": "test@test.test"})
    session.commit()
    updated_user = session.query(User).filter(User.nickname == 'test').first()

    assert res.status_code == 200
    assert updated_user.name == 'success'


def test_user_delete():
    admin_access_token = login_as_admin()
    admin_auth = {'Authorization': 'Bearer ' + admin_access_token}

    user_access_token = login_as_testuser()
    user_auth = {'Authorization': 'Bearer ' + user_access_token}

    bd_size = len(User.query.filter().all())

    res = requests.delete(url + '/user/' + 'test', headers=user_auth)
    assert res.status_code == 401

    res_2 = requests.delete(url + '/user/' + 'test', headers=admin_auth)
    session.commit()
    assert res_2.status_code == 200

    bd_size_after = len(session.query(User).filter().all())
    assert bd_size_after == bd_size - 1
