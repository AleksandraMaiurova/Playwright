from playwright.sync_api import APIRequestContext,Playwright
from typing import Generator
import pytest
import json
import requests

@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
)-> Generator[APIRequestContext,None,None]:
    request_context = playwright.request.new_context()
    yield request_context
    request_context.dispose()
def test_auth(api_request_context: APIRequestContext) -> None:
    headers = {"Content-type": "application/json"}
    data = {
        "username": "admin",
        "password": "password123"
    }
    response = api_request_context.post(f"https://restful-booker.herokuapp.com/auth", data=data, headers=headers)
    assert response.status == 200

@pytest.fixture(scope="session")
def auth():
    login = "admin"
    password = "password123"
    response_token = requests.post('https://restful-booker.herokuapp.com/auth', json={
        "username": login, "password": password})
    return json.loads(response_token.text).get('token')

def test_booking(api_request_context: APIRequestContext) -> None:
    headers = {"Content-type": "application/json"}
    response = api_request_context.get(f"https://restful-booker.herokuapp.com/booking", headers=headers)
    assert response.status == 200
    assert isinstance(response.json(), list)
    print(response.json()[0]['bookingid'])
    assert response.json()[0]['bookingid'] is not None

@pytest.fixture(scope="session")
def idbooking():
    headers = {"Content-type": "application/json"}
    response = requests.get(f"https://restful-booker.herokuapp.com/booking", headers=headers)
    return response.json()[0]['bookingid']

def test_GetBooking (idbooking, api_request_context: APIRequestContext) -> None:
    headers = {"Content-type": "application/json"}
    response = api_request_context.get(f'https://restful-booker.herokuapp.com/booking/{idbooking}', headers=headers)
    assert response.status == 200
    print(response.json())
    assert isinstance(response.json(), dict)
    assert response.json()["firstname"] == "John"
    assert response.json()["lastname"] == "Smith"
    assert response.json()["totalprice"] == 111

def test_CreateBooking (api_request_context: APIRequestContext) -> None:
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json"}
    data = {
        "firstname": "Aleksandra",
        "lastname": "Maiurova",
        "totalprice": 112,
        "depositpaid": True,
        "bookingdates": {
         "checkin": "2023-01-01",
         "checkout": "2023-05-01"
        },
        "additionalneeds": "Breakfast for my cat"
    }
    response = api_request_context.post(f"https://restful-booker.herokuapp.com/booking", data=data, headers=headers)
    assert response.status == 200
    assert response.json()['bookingid'] is not None

def test_DeleteBooking (auth, idbooking, api_request_context: APIRequestContext) -> None:
    headers = {"Content-type": "application/json",
               "Cookie": f'token={auth}'}
    response = api_request_context.delete(f'https://restful-booker.herokuapp.com/booking/{idbooking}', headers=headers)
    assert response.status == 201




