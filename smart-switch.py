from xmlrpc.client import Boolean
from flask import Flask, request, Response
import json

app = Flask(__name__)

class Switch:
    def __init__(self, value):
        self._switch = value  
    def getEnable(self):
        return self._switch
    def setEnable(self, enable):
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
        if (type(currentSwitch.getEnable()) == Boolean): # Switch state normal case
            print("server 200")
            response.status_code = 200
            response.data = json.dumps({
                "is_enable": currentSwitch.getEnable() # Define more content here
            })
        else:                                            # Switch state abnormal case
            print("server 500")
            response.status_code = 500
            response.data = json.dumps({
                "err": "Check your switch availability cannot read" # Handle more error here
            })

        print(response)
        return response

    if request.method == "POST":
        response = Response(mimetype='application/json')
        set_data = request.get_json()  
        print("set_data")
        print(set_data)

        set_result = currentSwitch.setEnable(set_data['enable'])
        print("is_valid_type")
        is_valid_type = type(set_data['enable']) == Boolean
        print(is_valid_type)
        print(type(set_data['enable']))
        print("is_success")
        is_success = set_result & is_valid_type
        print(is_success)
        if (is_success): # Switch state normal case
            print("server 200")
            response.status_code = 200
            response.data = json.dumps({
                "is_enable": currentSwitch.getEnable(),          # Define more content here
            })
        else:            # Switch state abnormal case
            print("server 500")
            response.status_code = 500
            response.data = json.dumps({
                "err": "Check your switch availability cannot write" # Handle more error here
            })

        print(response)
        return response


app.run(host='0.0.0.0', port=8090)
