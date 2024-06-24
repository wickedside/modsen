from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

# введите свой API ключ OpenWeatherMap
API_KEY = 'api'

@app.route('/status_codes', methods=['GET'])
def get_status_codes():
    statuses = {}

    # функция для отправки запросов и добавления статуса
    def check_status(url, label):
        try:
            response = requests.get(url)
            statuses[label] = response.status_code
        except requests.exceptions.RequestException as e:
            statuses[label] = str(e)

    # корректный запрос (ожидаем 200)
    url_valid = f"http://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={API_KEY}"
    check_status(url_valid, 'valid_request')

    time.sleep(1)

    # неверный API ключ (ожидаем 401)
    url_invalid_key = f"http://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=invalid_key"
    check_status(url_invalid_key, 'invalid_api_key')

    time.sleep(1)

    # данные не найдены (ожидаем 404)
    url_not_found = f"http://api.openweathermap.org/data/2.5/weather/qwerty?lat=44.34&lon=10.99&dt=1609459200&appid={API_KEY}"
    check_status(url_not_found, 'data_not_found')

    time.sleep(1)

    # заглушка для некорректного запроса (ожидаем 400)
    statuses['bad_request'] = 400

    time.sleep(1)

    # заглушка для запрещенного доступа (ожидаем 403)
    statuses['forbidden_request'] = 403

    time.sleep(1)

    # заглушка для превышения лимита запросов (ожидаем 429)
    statuses['rate_limit_exceeded'] = 429

    return jsonify(statuses)

if __name__ == '__main__':
    app.run(debug=True)
