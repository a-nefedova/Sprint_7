from data import URLs

import requests
import random
import string
import allure


def random_string(length=10):
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters)[:length] for i in range(length))
    return random_str


@allure.step('Создаём уникального курьера и возвращаем его учётные данные')
def register_new_courier_and_return_creds():
    payload = valid_creds()
    response = post_request_register(payload, False)
    if response.status_code == 201:
        return payload


@allure.step(f'Отправляем данные на регистрацию курьера')
def post_request_register(payload, auto_delete=True, fst_pass=''):
    response = requests.post(URLs.COURIER_REGISTER, data=payload)
    try:
        return response
    finally:
        if response.status_code == 201 and auto_delete:
            delete_courier(payload)
        elif response.status_code == 409 and fst_pass:
            payload['password'] = fst_pass
            delete_courier(payload)


@allure.step(f'Отправляем данные на авторизацию')
def post_request_auth(payload, initial_payload=''):
    response = requests.post(URLs.COURIER_AUTH, data=payload)
    try:
        return response
    finally:
        if response.status_code == 200:
            delete_courier(payload)
        elif initial_payload:
            delete_courier(initial_payload)


@allure.step(f'Отправляем данные на заказ')
def post_request_order(payload):
    return requests.post(URLs.ORDER, data=payload)


@allure.step('Отправляем запрос на получение списка заказов')
def get_request_orders():
    return requests.get(URLs.ORDER)


def incorrect_creds_list():
    courier = register_new_courier_and_return_creds()
    incorrect_creds = [
        [{'login': courier['login'], 'password': random_string()}, courier],
        [{'login': random_string(), 'password': courier['password']}, courier]
    ]
    return incorrect_creds


def one_random_cred():
    creds_list = [
        {'login': '', 'password': random_string()},
        {'login': random_string(), 'password': ''}
    ]
    return creds_list


def one_empty_cred():
    courier = register_new_courier_and_return_creds()
    creds_list = [
        [{'login': courier['login'], 'password': ''}, courier],
        [{'login': '', 'password': courier['password']}, courier]
    ]
    return creds_list


@allure.step('Генерируем словарь с уникальными учётными данными')
def valid_creds():
    payload = {
        'login': random_string(),
        'password': random_string()
    }
    return payload


def delete_courier(payload):
    response = requests.post(URLs.COURIER_AUTH, data=payload)
    if response.status_code == 404:
        return
    courier_id = response.json()['id']
    delete_response = requests.delete(f'{URLs.COURIER_DELETE}{courier_id}')
    assert delete_response.status_code == 200
