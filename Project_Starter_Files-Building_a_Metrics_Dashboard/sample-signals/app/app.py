import time
import random

from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
PrometheusMetrics(app)

endpoints = ('one', 'two', 'three', 'four', 'five', 'error', 'foo')

class InvalidHandle(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        error_message = dict(self.payload or ())
        error_message['message'] = self.message
        return error_message

@app.route('/one')
def first_route():
    time.sleep(random.random() * 0.2)
    return 'ok'

@app.route('/two')
def the_second():
    time.sleep(random.random() * 0.4)
    return 'ok'

@app.route('/three')
def test_3rd():
    time.sleep(random.random() * 0.6)
    return 'ok'

@app.route('/four')
def fourth_one():
    time.sleep(random.random() * 0.8)
    return 'ok'

@app.route('/error')
def oops():
    return ':(', 500

@app.errorhandler(InvalidHandle)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/foo')
def get_error():
    raise InvalidHandle('error occur', status_code=410)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)
