class URLs:
    BASE = 'http://qa-scooter.praktikum-services.ru/'
    COURIER_REGISTER = f'{BASE}api/v1/courier'
    COURIER_AUTH = f'{BASE}api/v1/courier/login'
    COURIER_DELETE = f'{BASE}api/v1/courier/'
    ORDER = f'{BASE}api/v1/orders'


class OrderData:
    order_data = {
        'firstName': 'Анастасия',
        'lastName': 'Нефёдова',
        'address': 'ул. Разбитых фонарей, 42',
        'metroStation': 4,
        'phone': '12345678901',
        'rentTime': 3,
        'deliveryDate': '2025-01-01',
        'comment': 'Хорошего дня!'
    }

    colors = [
            ["BLACK", ""],
            ["GREY", ""],
            ["BLACK", "GREY"],
            []
        ]
