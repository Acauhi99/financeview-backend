from http import HTTPStatus

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

def test_preflight_handler_return_empty_dict_and_code_ok():
    response = client.options("/test")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {}

def test_root_return_welcome_message_and_code_ok():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "FinanceView API"}