## Sample Folight server API readme

Setting up Flask to make your simple server.

### Required package
* python3.7
<br>https://installvirtual.com/install-python-3-7-on-raspberry-pi/

### Setting up virtual environments
```
$ python3.7 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```
### Start a read only sensor example.
```shell
(venv) $ python3 read-only-sensor.py
```
### Start a smart switch example.
```shell
(venv) $ python3 smart-switch.py
```
