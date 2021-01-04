# Uses the RGB LED Module
from time import time,sleep
import datetime 
import board
import RPi.GPIO as GPIO
from flask import Flask, json, request
from urllib.parse import urlparse, parse_qs
from threading import Thread

lastAwayTime = 0
host = "192.168.1.206"
presenting = False

def set_light_color(color):
    if color == 'RED':
        RED.start(100)
        GREEN.start(0)
        BLUE.start(0)
    if color == 'GREEN':
        RED.start(0)
        GREEN.start(100)
        BLUE.start(0)
    if color == 'YELLOW':
        RED.start(100)
        GREEN.start(100)
        BLUE.start(0)
    if color == 'OFF':
        RED.start(0)
        GREEN.start(0)
        BLUE.start(0)

api = Flask(__name__)
@api.route('/teamsstatus', methods=['PUT'])
def set_teams_light():
    global lastAwayTime
    global presenting
    o = urlparse(request.url)
    query = parse_qs(o.query)
    status = query['status'][0]
    presenting = False
    if status == 'Available':
        set_light_color('GREEN')
    if status == 'Busy':
        set_light_color('RED')
    if status == 'InAMeeting':
        set_light_color('RED')
    if status == 'Presenting':
        presenting = True
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
    global presenting
    flash = False
    print('Background thread started ...')
    # Turns off light if 'Away' for more than 5 minutes.
    while (True):        
        if lastAwayTime != 0 and time() - lastAwayTime > 300:
            set_light_color('OFF')
            lastAwayTime = 0
        if presenting == True:
            if flash == False:
                set_light_color('RED')
                flash = True
            else:
                set_light_color('OFF')
                flash = False
        sleep(1)

def init_color_board():
    global RED
    global GREEN
    global BLUE
    GPIO.setmode(GPIO.BCM)

    red = 27
    green = 17
    blue = 22

    GPIO.setup(red, GPIO.OUT)
    GPIO.setup(green, GPIO.OUT)
    GPIO.setup(blue, GPIO.OUT)

    Freq = 100

    RED = GPIO.PWM(red, Freq)
    GREEN = GPIO.PWM(green, Freq)
    BLUE = GPIO.PWM(blue, Freq)

    RED.start(0)
    GREEN.start(0)
    BLUE.start(0)    


init_color_board()

# Run background thread to turn off light when away for too long
thread = Thread(target = threaded_task)
thread.daemon = True
thread.start()

api.run(port=8080, host=host)
