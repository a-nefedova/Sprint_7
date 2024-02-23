# Sprint_7

# Проект автоматизации тестирования API учебного сервиса Яндекс Самокат.
https://qa-scooter.praktikum-services.ru/docs/

#
1. Основа для написания автотестов — фреймворк pytest
2. Установка проекта:
```
git clone https://github.com/a-nefedova/Sprint_7
pip install -r requirements.txt
```
3. Запуск проекта: 
```
pytest tests --alluredir=allure_results
allure serve allure_results 
```
