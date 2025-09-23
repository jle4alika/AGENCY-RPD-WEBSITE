import flask
from flask import Flask
from flask import request

from prometheus_flask_exporter import PrometheusMetrics

from telethon import TelegramClient
import asyncio

import sys

import logging

logging.basicConfig(level=logging.INFO,
                    filename='logs.txt',
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

logger = logging.getLogger(__name__)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Метрики
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP Request Latency',
    ['method', 'endpoint']
)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route('/')
def main():
    return flask.render_template('main.html')

@app.route('/advert')
def advert():
    return flask.render_template('advert.html')

@app.route('/design')
def design():
    return flask.render_template('design.html')

@app.route('/developing')
def developing():
    return flask.render_template('developing.html')

@app.route('/application', methods=['GET'])
def application():
    return flask.render_template('application.html')

async def send_new_building(name: str, email: str, phone_number: str, details: str):
    client = TelegramClient(
        'anon',
        api_id=25172187,
        api_hash='c163275c64658d29c719f13786a92cbb',
        app_version="4.16.30",
        system_version="4.16.30-vxCUSTOM",
        device_model="Desktop",
    )
    await client.start()
    await client.send_message(entity=-1002779911845,
                              reply_to=735,
                              message=f'НОВЫЙ ЗАКАЗ от <b><i>{name}</i></b>'
                                    f'\n\nПочта: <code>{email}</code>'
                                    f'\nНомер телефона: <code>{phone_number}</code>'
                                    f'\n\n<blockquote>{details}</blockquote>',
                              parse_mode='html')

    await client.disconnect()


@app.route('/application', methods=['POST'])
def filled_application():
    name = request.form.get('name')
    email = request.form.get('email')
    phone_number = request.form.get('phone-number', '')
    details = request.form.get('details')

    asyncio.run(send_new_building(name, email, phone_number, details))

    print(name, email, phone_number, '\n', details)
    return flask.render_template('main.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
