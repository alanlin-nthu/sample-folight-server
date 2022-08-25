from xmlrpc.client import Boolean
from flask import Flask, request, Response
import json

app = Flask(__name__)


class Switch:
    # Here define the GPIO or sensor reading.

    def __init__(self, value):
        self._switch = value

    def get_enable(self):
        return self._switch

    def set_enable(self, enable):
        self._switch = enable
        return True


currentSwitch = Switch(False)  # Default switch is false


@app.route('/', methods=['GET'])
def home():
    return "<p>This site is a prototype API for smart switch.</p>"


@app.route('/smart_switch', methods=['GET', 'POST'])
def get_status():
    if request.method == "GET":
        response = Response(mimetype='application/json')
        if type(currentSwitch.get_enable()) == Boolean:  # Switch state normal case
            print("server 200")
            response.status_code = 200
            response.data = json.dumps({
                "is_enable": currentSwitch.get_enable()  # Define more content here
            })
        else:  # Switch state abnormal case
            print("server 500")
            response.status_code = 500
            response.data = json.dumps({
                "err": "Check your switch availability cannot read"  # Handle more error here
            })

        print(response)
        return response

    if request.method == "POST":
        response = Response(mimetype='application/json')
        set_data = request.get_json()

        set_result = currentSwitch.set_enable(set_data['enable'])
        is_valid_type = type(set_data['enable']) == Boolean
        is_success = set_result & is_valid_type

        if is_success:  # Switch state normal case
            print("server 200")
            response.status_code = 200
            response.data = json.dumps({
                "is_enable": currentSwitch.get_enable(),  # Define more content here
            })
        else:  # Switch state abnormal case
            print("server 500")
            response.status_code = 500
            response.data = json.dumps({
                "err": "Check your switch availability cannot write"  # Handle more error here
            })

        print(response)
        return response


app.run(host='0.0.0.0', port=8091)
