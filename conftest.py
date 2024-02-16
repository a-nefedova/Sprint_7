import allure
import pytest
import requests

from helper import valid_creds, post_request_register, post_request_auth
from data import URLs


@allure.step('Создаём уникального курьера и возвращаем его учётные данные')
@pytest.fixture
def registered_courier():

    payload = valid_creds()
    response = post_request_register(payload)
    assert response.status_code == 201 and response.text == '{"ok":true}'

    yield payload

    auth_response = post_request_auth(payload)
    courier_id = auth_response.json()['id']
    delete_response = requests.delete(f'{URLs.COURIER_DELETE}{courier_id}')
    assert delete_response.status_code == 200 and response.text == '{"ok":true}'
