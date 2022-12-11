from picamera import PiCamera
#import time

#Put the following lines at the top of main?
#camera = PiCamera()
#time.sleep(2)



def takePhoto(cam, timeStamp):
    directory = "/home/Hat/ECE525/FinalProject/SecurityCam/"
    imagePath = directory + "/img" + timeStamp + ".jpg"
    cam.capture(imagePath)
    
    return imagePath

#Testing code
#path = takePhoto("2022-12-07 14:54:44.002068")
#print(path)
