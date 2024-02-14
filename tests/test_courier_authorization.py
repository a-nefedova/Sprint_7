import pytest
import allure

from data import URLs
from helper import (register_new_courier_and_return_creds, incorrect_creds_list, valid_creds,
                    post_request_auth, one_empty_cred, post_request_register)


class TestCourierAuthorization:

    @allure.title('Проверяем, что для авторизации нужно передать все обязательные поля')
    @allure.description('Авторизуемся с существующими логином и паролем, проверяем, что в ответ приходит код 200')
    @allure.link(URLs.COURIER_AUTH)
    def test_auth_all_required_creds(self):
        courier = register_new_courier_and_return_creds()
        response = post_request_auth(courier)

        assert response.status_code == 200

    @allure.title('Проверяем, что система вернёт ошибку, если неправильно указать логин или пароль')
    @allure.description('Используем параметризацию, где в тестовых данных либо логин, либо пароль некорректный. '
                        'Проверяем, что возвращается ошибка 404: Учетная запись не найдена')
    @allure.link(URLs.COURIER_AUTH)
    @pytest.mark.parametrize('creds', incorrect_creds_list())
    def test_auth_incorrect_creds(self, creds):
        response = post_request_auth(creds[0], creds[1])
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 404 and message == "Учетная запись не найдена"

    @allure.title('Проверяем, что если одно из обязательных полей не заполнено, запрос возвращает ошибку')
    @allure.description('Используем параметризацию, где в тестовых данных либо логин, либо пароль отсутствует. '
                        'Проверяем, что возвращается ошибка 400: Недостаточно данных для входа')
    @allure.link(URLs.COURIER_AUTH)
    @pytest.mark.parametrize('creds', one_empty_cred())
    def test_only_one_required_creds(self, creds):
        response = post_request_auth(creds[0], creds[1])
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 400 and message == "Недостаточно данных для входа"

    @allure.title('Проверяем, что если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    @allure.description('Авторизуемся с рандомными учётными данными. '
                        'Проверяем, что возвращается ошибка 404: Учетная запись не найдена')
    @allure.link(URLs.COURIER_AUTH)
    def test_auth_random_creds(self):
        payload = valid_creds()
        response = post_request_auth(payload)
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 404 and message == "Учетная запись не найдена"

    @allure.title('Проверяем, что успешный запрос возвращает id')
    @allure.description('Авторизуемся с существующими логином и паролем, проверяем, что в ответ приходит id курьера')
    @allure.link(URLs.COURIER_AUTH)
    def test_correct_request_response_id(self):
        courier = register_new_courier_and_return_creds()
        response = post_request_auth(courier)

        assert 'id' in response.text
