# Uses the Traffic Light Module
from time import time,sleep
from RPi import GPIO
from flask import Flask, json, request
from urllib.parse import urlparse, parse_qs
from threading import Thread

lastAwayTime = 0
host = "192.168.1.206"

def set_light_color(color):
    if color == 'RED':
        GPIO.output(9, True)
        GPIO.output(10, False)
        GPIO.output(11, False)
    if color == 'GREEN':
        GPIO.output(9, False)
        GPIO.output(10, False)
        GPIO.output(11, True)
    if color == 'YELLOW':
        GPIO.output(9, False)
        GPIO.output(10, True)
        GPIO.output(11, False)
    if color == 'OFF':
        GPIO.output(9, False)
        GPIO.output(10, False)
        GPIO.output(11, False)

api = Flask(__name__)
@api.route('/teamsstatus', methods=['PUT'])
def set_teams_light():
    global lastAwayTime
    o = urlparse(request.url)
    query = parse_qs(o.query)
    status = query['status'][0]
    if status == 'Available':
        set_light_color('GREEN')
    if status == 'Busy':
        set_light_color('RED')
    if status == 'InAMeeting':
        set_light_color('RED')
    if status == 'Presenting':
        # TODO: Flashing RED light when presenting. For now it just makes it RED.
        set_light_color('RED')
    if status == 'OnThePhone':
        set_light_color('RED')
    if status == 'DoNotDisturb':
        set_light_color('RED')
    if status == 'Away':
        set_light_color('YELLOW')
        if lastAwayTime == 0:
            lastAwayTime = time()
    if status == 'BeRightBack':
        set_light_color('YELLOW')
    return "Set status to " + status,200

def threaded_task():
    global lastAwayTime
    print('Background thread started ...')
    # Turns off light if 'Away' for more than 5 minutes.
    while (True):
        if lastAwayTime != 0 and time() - lastAwayTime > 300:
            set_light_color('OFF')
            lastAwayTime = 0
        sleep(5)

def init_color_board():
    GPIO.setmode(GPIO.BCM)

    red = 9
    green = 11
    yellow = 10

    GPIO.setup(red, GPIO.OUT)
    GPIO.setup(green, GPIO.OUT)
    GPIO.setup(yellow, GPIO.OUT)


init_color_board()

# Run background thread to turn off light when away for too long
thread = Thread(target = threaded_task)
thread.daemon = True
thread.start()

try:
    api.run(port=8080, host=host)
finally:
    print('Cleaning up GPIO ...')
    GPIO.cleanup()
