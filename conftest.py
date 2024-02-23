import allure
import pytest
import requests

from helper import valid_creds, post_request_register, post_request_auth
from data import URLs


@allure.step('Создаём уникального курьера и возвращаем его учётные данные')
@pytest.fixture
def registered_courier():

    payload = valid_creds()
    post_request_register(payload)

    yield payload

    auth_response = post_request_auth(payload)
    courier_id = auth_response.json()['id']
    requests.delete(f'{URLs.COURIER_DELETE}{courier_id}')
