# import required libraries
import RPi.GPIO as GPIO
from datetime import datetime
from picamera import PiCamera
import time
import threading
from emailModule import *


# global variables
global deviceId
global deviceIsArmed
global intruderAlert
global flashTheLED
global pollTheKeypad
global keypadString


deviceId = "1234"
deviceIsArmed = False
intruderAlert = False
flashTheLED = False
pollTheKeypad = False
keypadString = ""


# this GPIO pin is connected to the infared sensor

PIR = 0

# Initialize GPIO ports for the led

GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# this GPIO pin is connected to the led light

LED = 0

# Initialize GPIO ports for the LED

GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

# these GPIO pins are connected to the keypad
L1 = 0
L2 = 0
L3 = 0
L4 = 0

C1 = 0
C2 = 0
C3 = 0
C4 = 0


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Initialize the GPIO pins for the 4x4 keypad

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# The readLine function sends out a single pulse to one of the given rows of the keypad
# and then checks each column for changes
# If it detects a change, the user pressed the button that connects the given line
# to the detected column

# initialize the camera
camera = PiCamera()


def init():
    time.sleep(2)


def flashLED():
    while flashTheLED:
        GPIO.output(LED, GPIO.HIGH)  # Turn on
        time.sleep(1)                  # Sleep for 1 second
        GPIO.output(LED, GPIO.LOW)  # Turn off
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
    # remove the PIR listener
    GPIO.remove_event_detect(PIR)
    # capture and store an image from the camera
    imagePath = takePhoto()
    # turn on the flashing LED and set global variable flashTheLED to true
    flashTheLED = True
    flashLED()
    # start the 30 second timer in a different thread
    S = threading.Timer(30.0, timerEnd(imagePath))
    S.start()
    # set global variable intruderAlert to True
    intruderAlert = True


def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if (GPIO.input(C1) == 1):
        keypadString = keypadString + characters[0]
        print(characters[0])
    if (GPIO.input(C2) == 1):
        keypadString = keypadString + characters[1]
        print(characters[1])
    if (GPIO.input(C3) == 1):
        keypadString = keypadString + characters[2]
        print(characters[2])
    if (GPIO.input(C4) == 1):
        keypadString = keypadString + characters[3]
        print(characters[3])
    GPIO.output(line, GPIO.LOW)


def unarmDevice():
    # reset the device's armed state
    deviceIsArmed = False
    # set intruder alert to false
    intruderAlert = False
    # turn off the flashing LED
    flashTheLED = False


def keyboardPolling():
    while pollTheKeypad:
        # call the readLine function for each row of the keypad
        readLine(L1, ["1", "2", "3", "A"])
        readLine(L2, ["4", "5", "6", "B"])
        readLine(L3, ["7", "8", "9", "C"])
        readLine(L4, ["*", "0", "#", "D"])
        if keypadString[len(keypadString) - 1] == "#" and len(keypadString) == 5:
            # remove last char in string (#)
            typedKeyCode = keypadString[:-1]
            # database call with the device id, if code matches then reset
            if typedKeyCode == "password":
                unarmDevice()
    time.sleep(0.1)


try:
    init()
    # program while loop
    while True:
        # if the device is armed add an event detector for the PIR sensor
        if deviceIsArmed and not intruderAlert:
            GPIO.add_event_detect(PIR, GPIO.RISING, callback=intruderDetected)
        while intruderAlert:
            # keypad polling, probably don't need a new thread here... (Using pad4pi interrupt package)
            t = threading.Thread(target=keyboardPolling)
            t.start()

except KeyboardInterrupt:
    print("\nApplication stopped!")
