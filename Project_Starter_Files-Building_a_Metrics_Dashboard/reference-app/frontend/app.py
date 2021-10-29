from flask import Flask, render_template, jsonify
import threading
import requests
import random
import time
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

app = Flask(__name__)
# metrics = GunicornInternalPrometheusMetrics(app)
endpoints = ('error', 'foo')

def random_endpoint():
        try:
            target = random.choice(endpoints)
            requests.get("http://app:8081/%s" % target, timeout=1)

        except:
            pass

@app.route('/')
def homepage():
    return render_template("main.html")


@app.route('/healthz')
def healthcheck():
    app.logger.info('Status request successfull')
    return jsonify({"result": "OK - healthy"})

if __name__ == "__main__":  
    
    app.run()
    threading.Thread(target=random_endpoint).start()
    