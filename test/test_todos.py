from test.test_main import client
from main import app
from fastapi import status


def test_read_todos():
    response =client.get('/')
    assert response.status_code ==status.HTTP_401_UNAUTHORIZED