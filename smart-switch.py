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


@app.route('/read_switch', methods=['POST'])
def get_status():
    if request.method == "POST":
        response = Response()

        if (type(currentSwitch.getEnable()) == Boolean): # Switch state normal case
            print("server 200")
            response.status_code = 200
            response.data = json.dumps({
                "switch_enable": currentSwitch.getEnable() # Define more content here
            })

        else:                                            # Switch state abnormal case
            print("server 500")
            response.status_code = 500
            response.data = json.dumps({
                "err": "Check your switch availability cannot read" # Handle more error here
            })

        print(response)
        return response

@app.route('/write_switch', methods=['POST'])
def set_status():
    if request.method == "POST":
        response = Response()
        set_data = json.loads(request.get_data(as_text=True))        
        
        set_result = currentSwitch.setEnable(set_data['enable'])
        is_valid_type = type(set_data['enable']) == Boolean
        is_success = set_result & is_valid_type

        if (is_success): # Switch state normal case
            print("server 200")
            response.status_code = 200
            response.data = json.dumps({
                "switch_enable": currentSwitch.getEnable(),          # Define more content here
            })

        else:            # Switch state abnormal case
            print("server 500")
            response.status_code = 500
            response.data = json.dumps({
                "err": "Check your switch availability cannot write" # Handle more error here
            })

        print(response)
        return response


app.run()
