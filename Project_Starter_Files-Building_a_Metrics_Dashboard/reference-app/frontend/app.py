from flask import Flask, render_template
import threading
import requests
import random
import time

app = Flask(__name__)
endpoints = ('error', 'foo')

def random_endpoint():
        try:
            target = random.choice(endpoints)
            requests.get("http://app:8080/%s" % target, timeout=1)

        except:
            pass

@app.route('/')
def homepage():
    return render_template("main.html")


if __name__ == "__main__":  
    
    app.run()
    threading.Thread(target=random_endpoint).start()
    