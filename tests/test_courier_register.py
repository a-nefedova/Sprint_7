import allure
import pytest

from helper import valid_creds, random_string, post_request_register
from data import URLs


class TestCourierRegister:

    @allure.title('Проверяем, что нельзя создать двух курьеров с одинаковыми логинами')
    @allure.description('Пытаемся зарегистрировать курьера под уже существующим логином, '
                        'проверяем, что возвращается ошибка 409: Этот логин уже используется. Попробуйте другой.')
    @allure.link(URLs.COURIER_REGISTER)
    def test_register_two_same_couriers_not_allowed(self, registered_courier):

        courier = registered_courier.copy()
        courier['password'] = random_string()

        response = post_request_register(courier)
        response_status_code = response.status_code
        response_message = response.json()['message']

        assert response_status_code == 409 and response_message == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Проверяем, что чтобы создать курьера, нужно передать в ручку все обязательные поля')
    @allure.description('Регистрируем курьера с заполненными логином и паролем, проверяем, что в ответ приходит '
                        'код 201')
    @allure.link(URLs.COURIER_REGISTER)
    def test_all_required_creds(self):

        courier = valid_creds()
        response = post_request_register(courier)

        assert response.status_code == 201 and response.text == '{"ok":true}'

    @allure.title('Проверяем, что если одно из обязательных полей не заполнено, запрос возвращает ошибку')
    @allure.description('Используем параметризацию, где в тестовых данных либо логин, либо пароль отсутствует. '
                        'Проверяем, что возвращается ошибка 400: Недостаточно данных для создания учетной записи')
    @allure.link(URLs.COURIER_REGISTER)
    @pytest.mark.parametrize('cred', ['login', 'password'])
    def test_unfilled_required_creds(self, cred):

        courier = valid_creds()
        courier[cred] = ''

        response = post_request_register(courier)
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 400 and message == "Недостаточно данных для создания учетной записи"
