import pytest
import allure

from data import OrderData, URLs
from helper import post_request_order, get_request_orders


class TestOrder:

    @allure.title('Проверяем, что при заказе можно выбрать 0, 1 или 2 цвета')
    @allure.description('Используем параметризацию с разными значениями ключа color. '
                        'Проверяем, что в ответ приходит код 201 и тело ответа содержит track')
    @allure.link(URLs.ORDER)
    @pytest.mark.parametrize('color', OrderData.colors)
    def test_order_scooter_colors(self, color):
        OrderData.order_data['color'] = color
        response = post_request_order(OrderData.order_data)

        assert response.status_code == 201 and 'track' in response.text

    @allure.title('Проверяем, что в тело ответа возвращается список заказов')
    @allure.link(URLs.ORDER)
    def test_get_orders_list(self):
        response = get_request_orders()

        assert type(response.json()["orders"]) == list
