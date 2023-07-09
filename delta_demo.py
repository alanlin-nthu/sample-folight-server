from flask import Flask, Response, request
import json

app = Flask(__name__)
unique_id = 0xdddd


class LightState:
    def __init__(self):
        self.onOff_1 = 0
        self.level_1 = 0
        self.cct_1 = 0

    def __str__(self):
        print("onOff: " + str(self.onOff_1))
        print("level_1: " + str(self.level_1))
        print("cct_1: " + str(self.onOff_1))

@app.route('/', methods=['GET'])
def home():
    return "<p>This site is a prototype for Delta server.</p>"

@app.route('/v3/device/uuid/<string:name>/', methods=['GET'])
def get_sensor_status_uuid(name: str):
    if request.method == 'GET':
        global my_state
        try:
            if my_state is None:
                my_state = LightState()  # Bad code [FixIt later], I just wanna have a singleton...
        except NameError as e:
            my_state = LightState()
        print("get_sensor_status_uuid : " + name)
        response = Response(mimetype='application/json')
        response.status_code = 200
        response.data = json.dumps({
            "status": "success",
            "code": 200,
            "message": "",
            "payload": {
                "devices": [
                    {
                        "id": 1,
                        "name": "DT8_1",
                        "uniAddress": 4,
                        "uuid": "68b542e0-244b-045c-4460-fa2687d22507",
                        "state": {
                            "onOff": my_state.onOff_1,
                            "level": my_state.level_1,
                            "cct": my_state.cct_1
                        }
                    }
                ]
            }
        })
        return response

@app.route('/v3/device', methods=['GET', 'PATCH'])
def get_sensor_status():
    global my_state
    try:
        if my_state is None:
            my_state = LightState()  # Bad code [FixIt later], I just wanna have a singleton...
    except NameError as e:
        my_state = LightState()

    if request.method == 'GET':
        response = Response(mimetype='application/json')
        response.status_code = 200
        response.data = json.dumps({
            "status": "success",
            "code": 200,
            "message": "",
            "payload": {
                "devices": [
                    {
                        "id": 1,
                        "name": "DT8_1",
                        "uniAddress": 4,
                        "uuid": "68b542e0-244b-045c-4460-fa2687d22507",
                        "state": {
                            "onOff": my_state.onOff_1,
                            "level": my_state.level_1,
                            "cct": my_state.cct_1
                        }
                    },
                    {
                        "id": 2,
                        "name": "DT6_2",
                        "uniAddress": 8,
                        "uuid": "24219b10-e7cf-93cc-6cb6-e7c906b22507",
                        "state": {
                            "onOff": 1,
                            "level": 255,
                            "cct": 0
                        }
                    }
                ]
            }
        })

    if request.method == 'PATCH':

        # "{
        #    "device": {
        #        "id": 1,
        #        "uniAddress": 4,
        #        "state": {
        #            "onOff": 0
        #         }
        #    }
        # }"

        request_payload = json.loads(request.data)
        print("Req++")
        print(request_payload["device"]["state"])
        for control_type, control_value in request_payload["device"]["state"].items():
            if control_type == "onOff":
                my_state.onOff_1 = control_value
                print("Control: onOff == " + str(my_state.onOff_1))
            elif control_type == "level":
                my_state.level_1 = control_value
                print("Control: level == " + str(my_state.level_1))
            elif control_type == "cct":
                my_state.cct_1 = control_value
                print("Control: cct == " + str(my_state.cct_1))
            break

        print("Req--")

        # response return back the payload #
        response = Response(mimetype='application/json')
        response.status_code = 200
        response.data = json.dumps({
            "status": "success",
            "code": 200,
            "message": "",
            "payload": {
                "devices": [
                    {
                        "id": 1,
                        "deviceDescription": "0",
                        "state": {
                            "onOff": my_state.onOff_1,
                            "level": my_state.level_1,
                            "cct": my_state.cct_1
                        }
                    }
                ]
            }
        })

    print("Resp++")
    print(response.data)
    print("Resp--")

    return response


app.run(host='0.0.0.0', port=8088)
