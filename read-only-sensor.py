from flask import Flask, Response
import random
import json

app = Flask(__name__)
unique_id = 0x1111


@app.route('/', methods=['GET'])
def home():
    return "<p>This site is a prototype API for read-only sensor.</p>"


@app.route('/sensor_status', methods=['GET'])
def get_sensor_status():
    value = random.uniform(25.0, 39.9)
    response = Response(mimetype='application/json')
    response.status_code = 200
    response.data = json.dumps({
        "unique_id": unique_id,
        "value": value,  # Define more content here
    })
    print(response.data)
    return response


app.run(host='0.0.0.0', port=8090)
