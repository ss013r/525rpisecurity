from flask import Flask, render_template, request, g
import multiprocessing
import time

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

@app.route('/') #root directory for website
def index():
    conn2.send(BLANK_CODE)
    return render_template('ActiveHTML.html', user_input=BLANK_CODE, current_state=stateConn2.recv())

@app.route('/', methods=['POST']) #root directory for website, POST
def display_input():
    user_input = request.form['user_input'] #the user's input for the secret code
    conn2.send(user_input)
    return render_template('ActiveHTML.html', user_input=user_input, current_state=stateConn2.recv())

def system():
    current_state = INITIAL_STATE
    while(1):
        #Case 1: System is disarmed, set it to armed if secret code is input on webpage
        while(current_state == "disarmed"):
            print("current_state set to disarmed")
            #Block System process until a webserver request:
            receivedCode = conn1.recv() 
            if receivedCode == SECRET_CODE: #correct code received
                print("Code accepted while disarmed, arming...")
                current_state = "armed"
            elif receivedCode == BLANK_CODE: #no code received
                print("Blank code, no POST.")
            else:
                print("Incorrect code sent while disarmed.") #bad code received
            stateConn1.send(current_state)

        #Case 2: System is armed, set it to disarmed if code is input on webpage,
        #...but will be able to be triggered by sensors as well.
        while(current_state == "armed"):
            print("current_state set to armed")
            receivedCode = conn1.poll() #Avoid blocking, poll for webserver request first
            if receivedCode is not None:
                #Webserver request came in, handle it:
                receivedCode = conn1.recv() #flush pipe
                if receivedCode == SECRET_CODE:
                    print("Code accepted while armed, disarming...")
                    current_state = "disarmed"
                elif receivedCode == BLANK_CODE:
                    print("Blank code, no POST.")
                else:
                    print("Incorrect code sent while armed.")
                stateConn1.send(current_state)
            else:
                #Do other things related to sensor/keypad polling here
                time.sleep(POLLING_INTERVAL)
                continue

        #Case 3: System is triggered, set it to disarmed if code is input on keypad
        while(current_state == "triggered"):
                print("current_state set to triggered")
                #Do NOT send out triggered state to final_project.py! It will handle that.

        #Case 4: System is alerted, send out the photo and maybe do other things?
        while(current_state == "alert"):
                print("current_state set to alert")

            

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
    # process = multiprocessing.Process(target=bradyMain)
    # process.start()
    # processes.append(process)
    #wait for all processes to finish
    for process in processes:
        process.join()

if __name__ == '__main__':
    main()