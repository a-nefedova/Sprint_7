import allure
import pytest

from helper import (valid_creds, register_new_courier_and_return_creds, one_random_cred,
                    random_string, post_request_register)
from data import URLs


class TestCourierRegister:

    @allure.title('Проверяем, что нельзя создать двух курьеров с одинаковыми логинами')
    @allure.description('Регистрируем курьера, пытаемся зарегистрировать другого курьера с таким же логином, '
                        'проверяем, что возвращается ошибка 409: Этот логин уже используется. Попробуйте другой.')
    @allure.link(URLs.COURIER_REGISTER)
    def test_register_two_same_couriers_not_allowed(self):

        fst_courier = register_new_courier_and_return_creds()
        scnd_courier = {
            'login': fst_courier['login'],
            'password': random_string(),
        }

        second_courier_response = post_request_register(scnd_courier, fst_pass=fst_courier['password'])

        response_status_code = second_courier_response.status_code
        response_message = second_courier_response.json()['message']

        assert response_status_code == 409 and response_message == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Проверяем, что чтобы создать курьера, нужно передать в ручку все обязательные поля')
    @allure.description('Регистрируем курьера с заполненными логином и паролем, проверяем, что в ответ приходит '
                        'код 201')
    @allure.link(URLs.COURIER_REGISTER)
    def test_all_required_creds(self):
        payload = valid_creds()
        response = post_request_register(payload)

        assert response.status_code == 201

    @allure.title('Проверяем, что успешный запрос возвращает "ok": true')
    @allure.description('Регистрируем курьера с валидными учётными данными, проверяем, что тело ответа '
                        'содержит "ok": true')
    @allure.link(URLs.COURIER_REGISTER)
    def test_correct_request_success_response(self):
        payload = valid_creds()
        response = post_request_register(payload)

        assert response.text == '{"ok":true}'

    @allure.title('Проверяем, что если одно из обязательных полей не заполнено, запрос возвращает ошибку')
    @allure.description('Используем параметризацию, где в тестовых данных либо логин, либо пароль отсутствует. '
                        'Проверяем, что возвращается ошибка 400: Недостаточно данных для создания учетной записи')
    @allure.link(URLs.COURIER_REGISTER)
    @pytest.mark.parametrize('payload', one_random_cred())
    def test_unfilled_required_creds(self, payload):
        response = post_request_register(payload)

        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 400 and message == "Недостаточно данных для создания учетной записи"
