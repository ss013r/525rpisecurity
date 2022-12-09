from flask import Flask, render_template, request, g
import multiprocessing

#system/webserver pipe for sending secret code between processes
conn1, conn2 = multiprocessing.Pipe(duplex=False) #system is receive-only
#system/webserver pipe for sending current state between processes
stateConn2, stateConn1 = multiprocessing.Pipe(duplex=False) #webserver is receive-only
#secret code that disarms system
SECRET_CODE = "1234"
#initial state of system at boot; this gets changed by system().
INITIAL_STATE = "disarmed"

app = Flask(__name__)

    #shows hello world:
##@app.route('/')
##def index():
##    return 'Hello, world!'
@app.route('/')
def index():
    return render_template('ActiveHTML.html', user_input="",current_state=stateConn2.recv())

@app.route('/', methods=['POST'])
def display_input():
    user_input = request.form['user_input'] #the user's input for the secret code
    conn2.send(user_input)
    return render_template('ActiveHTML.html', user_input=user_input, current_state=stateConn2.recv())

def system():
    current_state = INITIAL_STATE
    stateConn1.send(current_state) #send the default state for web server right away
    while(1):
        #Handle case: System is disarmed, set it to armed if code is input on webpage
        if current_state == "disarmed":
            print("disarmed")
            while(1):
                if conn1.recv() == SECRET_CODE:
                    print("Code accepted while disarmed, arming...")
                    current_state = "armed"
                    break
                else:
                    print("Incorrect code sent while disarmed.")
                    break

        #Handle case: System is armed, set it to disarmed if code is input on webpage
        elif current_state == "armed":
            print("armed")
            while(1):
                if conn1.recv() == SECRET_CODE:
                    print("Code accepted while armed, disarming...")
                    current_state = "disarmed"
                    break
                else:
                    print("Incorrect code sent while armed.")
                    break

        #Handle case: System is triggered, set it to disarmed if code is input on keypad
        elif current_state == "triggered":
            print("triggered")

        #Handle case: System is alerted, send out the photo and maybe do other things?
        elif current_state == "alert":
            print("alert")

        stateConn1.send(current_state) #end of system loop: send current state
            

def run_website():
    app.run(host='0.0.0.0', port=1234)

def main():
    processes = []

    process = multiprocessing.Process(target=run_website)
    process.start()
    processes.append(process)

    process = multiprocessing.Process(target=system)
    process.start()
    processes.append(process)
 
    for process in processes:
        process.join()


if __name__ == '__main__':
    main()