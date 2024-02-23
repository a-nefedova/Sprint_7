import pytest
import allure

from data import URLs
from helper import valid_creds, random_string, post_request_auth


class TestCourierAuthorization:

    @allure.title('Проверяем, что для авторизации нужно передать все обязательные поля')
    @allure.description('Авторизуемся с существующими логином и паролем, проверяем, что в ответ приходит код 200'
                        ' и тело ответа содержит id курьера')
    @allure.link(URLs.COURIER_AUTH)
    def test_auth_all_required_creds(self, registered_courier):

        response = post_request_auth(registered_courier)

        assert response.status_code == 200 and 'id' in response.text

    @allure.title('Проверяем, что система вернёт ошибку, если неправильно указать логин или пароль')
    @allure.description('Используем параметризацию, где в тестовых данных либо логин, либо пароль некорректный. '
                        'Проверяем, что возвращается ошибка 404: Учетная запись не найдена')
    @allure.link(URLs.COURIER_AUTH)
    @pytest.mark.parametrize('cred', ['login', 'password'])
    def test_auth_incorrect_creds(self, registered_courier, cred):

        courier = registered_courier.copy()
        courier[cred] = random_string()

        response = post_request_auth(courier)
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 404 and message == "Учетная запись не найдена"

    @allure.title('Проверяем, что если одно из обязательных полей не заполнено, запрос возвращает ошибку')
    @allure.description('Используем параметризацию, где в тестовых данных либо логин, либо пароль отсутствует. '
                        'Проверяем, что возвращается ошибка 400: Недостаточно данных для входа')
    @allure.link(URLs.COURIER_AUTH)
    @pytest.mark.parametrize('cred', ['login', 'password'])
    def test_only_one_required_creds(self, registered_courier, cred):

        courier = registered_courier.copy()
        courier[cred] = ''

        response = post_request_auth(courier)
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 400 and message == "Недостаточно данных для входа"

    @allure.title('Проверяем, что если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    @allure.description('Авторизуемся с рандомными учётными данными. '
                        'Проверяем, что возвращается ошибка 404: Учетная запись не найдена')
    @allure.link(URLs.COURIER_AUTH)
    def test_auth_random_creds(self):

        courier = valid_creds()

        response = post_request_auth(courier)
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 404 and message == "Учетная запись не найдена"
