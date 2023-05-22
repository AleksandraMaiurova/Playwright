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

def test_status_code(api_request_context: APIRequestContext) -> None:
    headers = {"Content-type": "application/json"}
    data = {
        "username": "skhalipa@gmail.com",
        "password": "skhalipa@gmail.com"
    }
    response = api_request_context.post(
        f"https://k-ampus.dev/api/v1/login", data=data, headers=headers
    )
    assert response.status == 200

def test_body_token(api_request_context: APIRequestContext) -> None:
    headers = {"Content-type": "application/json"}
    data = {
        "username": "skhalipa@gmail.com",
        "password": "skhalipa@gmail.com"
    }
    response = api_request_context.post(
        f"https://k-ampus.dev/api/v1/login", data=data, headers=headers
    )
    print(response.json()['accessToken'])
    assert response.json()['accessToken'] is not None

@pytest.fixture(scope="session")
def auth():
    response_token = requests.post('https://k-ampus.dev/api/v1/login', json={
        "username": "skhalipa@gmail.com",
        "password": "skhalipa@gmail.com"
    }, timeout=5)
    return json.loads(response_token.text).get('accessToken')

def test_status_code_competence(auth, api_request_context: APIRequestContext) -> None:
    headers = {'Authorization':f'Bearer {auth}'}
    response = api_request_context.get(
        f"https://k-ampus.dev/api/v1/competence", headers=headers
    )
    assert response.status == 200

def test_competence_content(auth, api_request_context: APIRequestContext) -> None:
    headers = {'Authorization':f'Bearer {auth}'}
    response = api_request_context.get(
        f"https://k-ampus.dev/api/v1/competence", headers=headers
    )
    assert  isinstance(response.json()['content'], list)

def test_competence_content_types(auth, api_request_context: APIRequestContext) -> None:
    headers = {'Authorization':f'Bearer {auth}'}
    response = api_request_context.get(
        f"https://k-ampus.dev/api/v1/competence", headers=headers
    )
    contents = response.json()['content']
    for content in contents:
        for k, v in content.items():
            if k == 'id':
                assert isinstance(v, int)
            elif k == 'name':
                assert isinstance(v, str)
            elif k == 'isHardSkill':
                assert isinstance(v, bool)
            elif k == 'skillIds':
                assert isinstance(v, list)
            else:
                pytest.fail(reason="Unexpected content item")
