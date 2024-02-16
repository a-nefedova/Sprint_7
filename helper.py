from data import URLs

import requests
import random
import string
import allure


def random_string(length=10):
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters)[:length] for i in range(length))
    return random_str


@allure.step('Генерируем словарь с уникальными учётными данными')
def valid_creds():
    payload = {
        'login': random_string(),
        'password': random_string()
    }
    return payload


@allure.step(f'Отправляем данные на регистрацию курьера')
def post_request_register(payload):
    response = requests.post(URLs.COURIER_REGISTER, data=payload)
    return response


@allure.step(f'Отправляем данные на авторизацию')
def post_request_auth(payload):
    response = requests.post(URLs.COURIER_AUTH, data=payload)
    return response


@allure.step(f'Отправляем данные на заказ')
def post_request_order(payload):
    return requests.post(URLs.ORDER, data=payload)


@allure.step('Отправляем запрос на получение списка заказов')
def get_request_orders():
    return requests.get(URLs.ORDER)
