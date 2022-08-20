from flask import Flask
import random
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<p>This site is a prototype API for read-only sensor.</p>"


@app.route('/status', methods=['GET'])
def getTemperature():
    temperature = random.uniform(25.0, 39.9)
    ret = json.dumps(temperature)
    print(ret)
    return ret

app.run(host='0.0.0.0', port=80)
