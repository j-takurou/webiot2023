from flask import Flask
from flask import request
from .sg90_sg92 import SG90_92R_Class
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/rotate/")
def rotate():
    if request.method == "POST":
        data = request.get_data()
        status = data["status"] # close or open
        command = data["command"] # lock or unlock
        direction = data["direction"]
        Servo = SG90_92R_Class(Pin=4,ZeroOffsetDuty=0)
        # 回転方向を保証できるかどうかが怖い
        Servo.SetPos(45)
    return "<p>rotate!</p>"


@app.route("/key-polling/")
def exist_restroom():
    if request.method == "GET":
        data = request.get_data()
        status = data["status"] # close or open
        command = data["command"] # lock or unlock
        direction = data["direction"]
        Servo = SG90_92R_Class(Pin=4,ZeroOffsetDuty=0)
        # 回転方向を保証できるかどうかが怖い
        Servo.SetPos(45)
    return "<p>rotate!</p>"