import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
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

#Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D23)
while True:
     try:
          # Print the values to the serial port
          temperature_c = dhtDevice.temperature
          temperature_f = temperature_c * (9 / 5) + 32
          humidity = dhtDevice.humidity
          print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% "
               .format(temperature_f, temperature_c, humidity))
          print("Checking temp ranges.")
          if temperature_f < 70.0 :
               print("Red light")
               RED.start(100)
               GREEN.start(0)
               BLUE.start(0)
          if temperature_f >= 70.0 and temperature_f < 75.0 :
               print("Green light")
               RED.start(0)
               GREEN.start(100)
               BLUE.start(0)
          if temperature_f >= 75.0 :
               print("Yellow light")
               # Yellow
               RED.start(100)
               GREEN.start(100)
               BLUE.start(0)

     except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
          print(error.args[0])
     except KeyboardInterrupt:
     #the purpose of this part is, when you interrupt the code, it will stop the while loop and turn off the pins, which means your LED won't light anymore
          RUNNING = False
          GPIO.cleanup()          
     time.sleep(2.0)
