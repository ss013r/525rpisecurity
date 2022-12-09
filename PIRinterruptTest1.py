import signal #Not needed in final version
import sys #Not sure if needed
import RPi.GPIO as GPIO

PIR_PIN = 14

#don't copy in final version, testing purposes
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

#Callback interrupt function
def pir_tripped_callback(channel):
    #Do interrupt things here
    print("Motion Detected!")



#Interrupt setup code
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=pir_tripped_callback, bouncetime=100)

#Don't copy stuff from below here, just for testing
signal.signal(signal.SIGINT, signal_handler)
signal.pause()