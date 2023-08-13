from dataclasses import dataclass
from flask import Flask, Response, request
import json

app = Flask(__name__)
unique_id = 0xdddd


@dataclass
class DeltaLightData:
    """ Delta data stored in the DataUpdateCoordinator."""
    uuid: str
    on_off: int
    level: int
    cct: int
    id: int
    uniAddress: int
    name: str

    def __str__(self):
        return "My Light is {uuid} on:{on_off} l:{level} cct:{cct} id:{id} u{uniAddress} name{name}" \
            .format(uuid=self.uuid,
                    on_off=self.on_off,
                    level=self.level,
                    cct=self.cct,
                    id=self.id,
                    uniAddress=self.uniAddress,
                    name=self.name
                    )


light_err = DeltaLightData(uuid="error",
                           on_off=-1,
                           level=-1,
                           cct=-1,
                           id=-1,
                           uniAddress=-1,
                           name="alan_err")

light1 = DeltaLightData(uuid="68b542e0-244b-045c-4460-fa2687d22507",
                        on_off=1,
                        level=1,
                        cct=1,
                        id=1,
                        uniAddress=4,
                        name="alan1")

light2 = DeltaLightData(uuid="24219b10-e7cf-93cc-6cb6-e7c906b22507",
                        on_off=0,
                        level=2,
                        cct=2,
                        id=2,
                        uniAddress=5,
                        name="alan2")

all_light: [DeltaLightData] = [light1, light2]


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

        chosen_light = light_err
        for light in all_light:
            if light.uuid == name:
                chosen_light = light
                print("get_sensor_status_uuid chosen ok")

        response = Response(mimetype='application/json')
        response.status_code = 200
        response.data = json.dumps({
            "status": "success",
            "code": 200,
            "message": "",
            "payload": {
                "devices": [
                    {
                        "id": chosen_light.id,
                        "name": chosen_light.name,
                        "uniAddress": chosen_light.uniAddress,
                        "uuid": chosen_light.uuid,
                        "state": {
                            "onOff": chosen_light.on_off,
                            "level": chosen_light.level,
                            "cct": chosen_light.cct
                        }
                    }
                ]
            }
        })
        print("Resp single light uuid light++")
        print(response.data)
        print("Resp single light uuid light--")
        return response


@app.route('/v3/device', methods=['GET', 'PATCH'])
def get_sensor_status():
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
                        "id": light1.id,
                        "name": light1.name,
                        "uniAddress": light1.uniAddress,
                        "uuid": light1.uuid,
                        "state": {
                            "onOff": light1.on_off,
                            "level": light1.level,
                            "cct": light1.cct,
                        }
                    },
                    {
                        "id": light2.id,
                        "name": light2.name,
                        "uniAddress": light2.uniAddress,
                        "uuid": light2.uuid,
                        "state": {
                            "onOff": light2.on_off,
                            "level": light2.level,
                            "cct": light2.cct,
                        }
                    }
                ]
            }
        })
        print("Resp All light++")
        print(response.data)
        print("Resp All light--")
        return response

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
        print(request_payload["device"]["state"])
        chosen_light = light_err
        for light in all_light:
            if light.id == request_payload["device"]["id"] and light.uniAddress == request_payload["device"]["uniAddress"]:
                chosen_light = light

        for control_type, control_value in request_payload["device"]["state"].items():
            if control_type == "onOff":
                chosen_light.on_off = control_value
            elif control_type == "level":
                chosen_light.level = control_value
            elif control_type == "cct":
                chosen_light.cct = control_value
            print("Update:" + chosen_light.__str__())
            break

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
                        "id": chosen_light.id,
                        "deviceDescription": "0",
                        "state": {
                            "onOff": chosen_light.on_off,
                            "level": chosen_light.level,
                            "cct": chosen_light.cct
                        }
                    }
                ]
            }
        })
        print("Resp Single ++")
        print(response.data)
        print("Resp Single --")
        return response


app.run(host='0.0.0.0', port=8088)
