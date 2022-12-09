from picamera import PiCamera
import time
from timestampModule import *
from cameraModule import *

camera = PiCamera()
time.sleep(2)

ts = getCurrentTimestamp()
imgPath = takePhoto(camera, ts)

print("Saved image: " + imgPath)