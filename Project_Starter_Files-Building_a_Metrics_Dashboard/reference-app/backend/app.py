from flask import Flask, render_template, request, jsonify
import time
import random
import pymongo
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics
from jaeger_client import Config
import logging

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'example-mongodb'
app.config['MONGO_URI'] = 'mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb'

mongo = PyMongo(app)
PrometheusMetrics(app)

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

@app.route('/error')
def oops():
    return ':(', 500

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

tracer = init_tracer('backend')

@app.errorhandler(InvalidHandle)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/foo')
def get_error():
    raise InvalidHandle('error occur', status_code=410)

@app.route('/')
def homepage(): 
    with tracer.start_span('hello-world'):
        return "Hello World"

@app.route('/api')
def my_api():
    with tracer.start_span('api'):
        answer = "something"
    return jsonify(repsonse=answer)

# This will return 405 error
@app.route('/star', methods=['POST'])
def add_star():
  star = mongo.db.stars
  name = request.json['name']
  distance = request.json['distance']
  star_id = star.insert({'name': name, 'distance': distance})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'distance' : new_star['distance']}
  return jsonify({'result' : output})

@app.route('/healthz')
def healthcheck():
    app.logger.info('Status request successfull')
    return jsonify({"result": "OK - healthy"})
    

if __name__ == "__main__":
    app.run(threaded=True)
