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

