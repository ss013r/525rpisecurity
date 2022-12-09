import RPi.GPIO as GPIO
from pad4pi import rpi_gpio
import time

keypadStr = "" #Global variable

KEYPAD = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

ROW_PINS = [5, 6, 13, 19] #BCM Numbering
COL_PINS = [26, 16, 20, 21] #BCM Numbering

def print_key(key):
    #Blink blue LED quickly to indicate successful press here?
    print("You entered " + key) #Don't put in final project
    #Put logic here


try:
    #SETUP INTERUPT AND HANDLER
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD,row_pins=ROW_PINS, col_pins=COL_PINS)
    
    keypad.registerKeyPressHandler(print_key)
    
    #security_state = "armed"
    
    print("Press buttons now. Ctrl-C to exit.") #Don't copy over, debugging
    
    while True:
        time.sleep(1)
        ##RUN REST OF PROGRAM IN WHILE LOOP?
        
except KeyboardInterrupt:
    print("Exit looping")
finally:
    keypad.cleanup()