from flask import Flask, render_template, request
import multiprocessing
import time
import re #regex
import final_project #final_project.py code

#system/webserver pipe for sending secret code between processes:
conn1, conn2 = multiprocessing.Pipe(duplex=False) #system is receive-only
#system/webserver pipe for sending current state between processes:
stateConn2, stateConn1 = multiprocessing.Pipe(duplex=False) #webserver is receive-only
#system/sensor pipe for syncing current state between processes:
sensorConn2, sensorConn1 = multiprocessing.Pipe(duplex=True) #Two-way
#secret code that disarms system:
SECRET_CODE = "1234"
#initial state of system at boot; this gets changed by system():
INITIAL_STATE = "disarmed"
#Maximum time webserver will have to wait for response, in seconds:
POLLING_INTERVAL = 0.1
#Default input code to be sent when no POST is made:
BLANK_CODE = ""

app = Flask(__name__)

#Root directory for website:
@app.route('/')
def index():
    conn2.send(BLANK_CODE)
    return render_template('ActiveHTML.html', user_input=BLANK_CODE, 
                           current_state=stateConn2.recv())

#Root directory for website with POST:
@app.route('/', methods=['POST'])
def display_input():
    user_input = request.form['user_input'] #secret code attempt
    if(user_input == ""):
        return index()
    #Enforce regex pattern: four digits (sanitize input)
    fourDigitPattern = re.compile("([0-9]){4}") 
    if(fourDigitPattern.fullmatch(user_input) == None):
        print("HTML POST did not match expected pattern!")
        return index()
    #Matched regex, forward input to System
    conn2.send(fourDigitPattern.fullmatch(user_input).string)
    return render_template('ActiveHTML.html', user_input=user_input, 
                           current_state=stateConn2.recv())

def system():
    current_state = INITIAL_STATE
    while(1):
        #Case 1: System is disarmed, set it to armed if secret code is input on webpage
        while(current_state == "disarmed"):
            #Block System process until a webserver request:
            receivedCode = conn1.recv() 
            if receivedCode == SECRET_CODE: #correct code received
                print("Code accepted while disarmed, arming...")
                current_state = "armed"
                sensorConn1.send(current_state) #arm the sensors
            elif receivedCode == BLANK_CODE: #no code received
                print("Blank code, no POST.")
            else:
                print("Incorrect code sent while disarmed.") #bad code received
            stateConn1.send(current_state)

        #Case 2: System is armed, set it to disarmed if code is input on webpage,
        #...but will be able to be triggered by sensors as well.
        while(current_state == "armed"):
            #Avoid blocking, poll for webserver request first
            if conn1.poll():
                #Webserver request came in, handle it:
                receivedCode = conn1.recv() #flush pipe
                if receivedCode == SECRET_CODE:
                    print("Code accepted while armed, disarming...")
                    current_state = "disarmed"
                    sensorConn1.send(current_state) #arm the sensors
                elif receivedCode == BLANK_CODE:
                    print("Blank code, no POST.")
                else:
                    print("Incorrect code sent while armed.")
                stateConn1.send(current_state)
            else:
                if(sensorConn1.poll()):
                    #New state came in the sensors (triggered?):
                    current_state = sensorConn1.recv()
                    print("New state from sensor while armed:", current_state)
                time.sleep(POLLING_INTERVAL)
                continue

        #Case 3: System is triggered and counting down, set to disarmed if sensors allow for it
        while(current_state == "triggered"):
            #Still handle webserver requests:
            if conn1.poll():
                receivedCode = conn1.recv() #don't care about web server codes(?)
                stateConn1.send(current_state)
            #New state came in the sensors (disarmed?):
            if(sensorConn1.poll()):
                current_state = sensorConn1.recv()
            time.sleep(POLLING_INTERVAL)
            #Do NOT send out triggered state over sensorConn! Handled by final_project.py


def run_website():
    app.run(host='0.0.0.0', port=1234)

def main():
    processes = []
    #web server (Flask) process:
    process = multiprocessing.Process(target=run_website)
    process.start()
    processes.append(process)
    #System process:
    process = multiprocessing.Process(target=system)
    process.start()
    processes.append(process)
    #Sensor/input logic for connected devices:
    process = multiprocessing.Process(target=final_project.IntrusionDetection, 
                                      args=(sensorConn2,))
    process.start()
    processes.append(process)
    #wait for all processes to finish
    for process in processes:
        process.join()

if __name__ == '__main__':
    main()