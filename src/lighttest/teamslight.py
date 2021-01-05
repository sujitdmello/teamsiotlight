# Uses the RGB LED Module
from time import time,sleep
import datetime 
import board
import RPi.GPIO as GPIO
from flask import Flask, json, request
from urllib.parse import urlparse, parse_qs
from threading import Thread

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

lastAwayTime = 0
host = "192.168.1.206"
presenting = False

RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Load default font.
font = ImageFont.truetype('good.ttf', 16)
# Initialize library.
disp.begin()

def clear_display():
    # Clear display.
    disp.clear()
    disp.display()
    
clear_display()

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
        display_message('Free', 'Come on', 'down')
    if status == 'Busy':
        set_light_color('RED')
        display_message('Busy', 'Not on a', 'call')
    if status == 'InAMeeting':
        set_light_color('RED')
        display_message('Meeting', 'Keep quiet', 'please')
    if status == 'Presenting':
        presenting = True
        display_message('Presenting', 'do not', 'disturb')
        set_light_color('RED')
    if status == 'OnThePhone':
        set_light_color('RED')
        display_message('Phone', 'Keep quiet', 'please')
    if status == 'DoNotDisturb':
        set_light_color('RED')
        display_message('Focused', 'Keep quiet', 'please')        
    if status == 'Away':
        set_light_color('YELLOW')
        display_message('Away', 'Goofing', 'Off')        
        if lastAwayTime == 0:
            lastAwayTime = time()
    if status == 'BeRightBack':
        set_light_color('YELLOW')
        display_message('Away', 'Be right', 'back')         
    if status == 'Offline':
        set_light_color('OFF')
        display_message('Offline', 'Gone', 'Fishing')            
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
            clear_display()
            lastAwayTime = 0
        if presenting == True:
            if flash == False:
                set_light_color('RED')
                flash = True
            else:
                set_light_color('OFF')
                flash = False
        sleep(5)

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

def display_message(message1, message2, message3):
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Write two lines of text.

    draw.text((x, top),       "STATUS",  font=font, fill=255)
    draw.text((x, top+16),     message1, font=font, fill=255)
    draw.text((x, top+32),     message2,  font=font, fill=255)
    draw.text((x, top+48),     message3,  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()

init_color_board()

# Run background thread to turn off light when away for too long
thread = Thread(target = threaded_task)
thread.daemon = True
thread.start()

api.run(port=8080, host=host)
