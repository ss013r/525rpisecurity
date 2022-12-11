import RPi.GPIO as GPIO
import time

LED_PIN_RED = 17
LED_PIN_GRN = 27
LED_PIN_BLU = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_RED, GPIO.OUT)
GPIO.setup(LED_PIN_GRN, GPIO.OUT)
GPIO.setup(LED_PIN_BLU, GPIO.OUT)

try:
    while True:
        #Cyles through red, green and blue
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
        
except KeyboardInterrupt:
    print("Done")
finally:
    GPIO.cleanup()