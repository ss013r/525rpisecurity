# import required libraries
import RPi.GPIO as GPIO
from datetime import datetime
import time
from picamera import PiCamera, PiCameraError
from pad4pi import rpi_gpio
import threading
from emailModule import *


# global variables
global deviceId
global intruderAlert
global keypadString
global sensorConn2


deviceId = "1234"
intruderAlert = False
keypadString = ""

# GPIO setup

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# this GPIO pin is connected to the infared sensor

PIR_PIN = 14

# Initialize GPIO ports for the led

GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# this GPIO pin is connected to the led light

LED_PIN_RED = 17
LED_PIN_GRN = 27
LED_PIN_BLU = 22

# Initialize GPIO ports for the LED

GPIO.setup(LED_PIN_RED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_PIN_GRN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_PIN_BLU, GPIO.OUT, initial=GPIO.LOW)

# these GPIO pins are connected to the keypad
L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 26
C2 = 16
C3 = 20
C4 = 21

KEYPAD = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

ROW_PINS = [L1, L2, L3, L4]
COL_PINS = [C1, C2, C3, C4]

# initialize the keypad library
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(
    keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

# function to disarm/reset the device


def disarmDevice():
    # send via pipe that the device is now disarmed to inform the web/system process
    sensorConn2.send("disarmed")
    # set intruder alert to false (turns off the LED and breaks out of the main while function)
    intruderAlert = False

# keypad button press interupt function


def keypadPress(key):
    if intruderAlert:
        # add key to the end of the keypadString
        keypadString = keypadString + key
        # print code to screen
        print(keypadString)
        if (len(keypadString) == 4):
         # 4 symbols were typed, compare the string with that of the password
            if (keypadString == "1234"):
                # disarm the device
                disarmDevice()
            else:
                # indicate that the user inputted incorrect pin inside of the console
                print("Incorrect Password, Please retype the correct code")
                # reset the keypadString
                keypadString == ""


keypad.registerKeyPressHandler(keypadPress)

# initialize the camera
try:
    camera = PiCamera()
except PiCameraError: # for debugging:
    print("Error: camera could not be initialized. Continuing...")


def init():
    print("Setting up device...")
    time.sleep(2)
    print("Finished setting up device!")


def flashLED():
    while intruderAlert:
        GPIO.output(LED_PIN_RED, GPIO.HIGH)
        GPIO.output(LED_PIN_GRN, GPIO.LOW)
        GPIO.output(LED_PIN_BLU, GPIO.LOW)
        time.sleep(1)
        GPIO.output(LED_PIN_RED, GPIO.LOW)
        GPIO.output(LED_PIN_GRN, GPIO.HIGH)
        GPIO.output(LED_PIN_BLU, GPIO.LOW)
        time.sleep(1)
        GPIO.output(LED_PIN_RED, GPIO.LOW)
        GPIO.output(LED_PIN_GRN, GPIO.LOW)
        GPIO.output(LED_PIN_BLU, GPIO.HIGH)
        time.sleep(1)


def takePhoto():
    timeStamp = str(datetime.datetime.now())
    directory = "/home/Hat/ECE525/FinalProject/SecurityCam/"
    imagePath = directory + "/img" + timeStamp + ".jpg"
    camera.capture(imagePath)
    print("Saved image: " + imagePath)
    return imagePath


def timerEnd(imagePath):
    # send email to the user as an alert, this picture should hold the timestamp and image that is stored on the pi
    sendEmailAlert(imagePath)
    print("email sent.")


def intruderDetected():
    # send via pipe that the device is triggered to inform the web/system process
    sensorConn2.send("triggered")
    # remove the PIR_PIN listener
    GPIO.remove_event_detect(PIR_PIN)
    # capture and store an image from the camera
    imagePath = takePhoto()
    # set global variable intruderAlert to True
    intruderAlert = True
    t = threading.Thread(target=flashLED)
    t.start()
    # start the 30 second timer in a different thread
    S = threading.Timer(30.0, timerEnd(imagePath))
    S.start()

# sensorConn2 is a Connection object for a Pipe, given by flaskapp.py/System
def IntrusionDetection(sensorConn2):
    try:
        init()
        # program while loop
        while True:
            # poll pipe for current state, then handle a change in state from System
            if sensorConn2.poll():
                receivedState = sensorConn2.recv()  # flush pipe
                if (receivedState == "armed"):
                    # add the PIR_PIN listener interupt
                    GPIO.add_event_detect(PIR_PIN, GPIO.RISING,
                                          callback=intruderDetected, bouncetime=100)
                elif (receivedState == "disarmed"):
                    # remove the PIR_PIN listener
                    GPIO.remove_event_detect(PIR_PIN)
            # no change in state from System
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nApplication stopped!")
    finally:
        GPIO.cleanup()
        keypad.cleanup()
