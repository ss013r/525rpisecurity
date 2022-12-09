from flask import Flask, render_template, request, g
import multiprocessing

conn1, conn2 = multiprocessing.Pipe(duplex=True)
stateConn1, stateConn2 = multiprocessing.Pipe(duplex=True) #current system state

secretCode = "1234"

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
    user_input = request.form['user_input']
    conn2.send(user_input)
    return render_template('ActiveHTML.html', user_input=user_input, current_state=stateConn2.recv())

def system():
    
    current_state = "disarmed"
    stateConn1.send(current_state) #send the state immediately

    while(1):
        #handle case: system is disarmed, set it to armed if code is input on webpage
        if current_state == "disarmed":
            print("disarmed")
            while(1):
                if conn1.recv() == secretCode:
                    print("Code accepted while disarmed, arming...")
                    current_state = "armed"
                    stateConn1.send(current_state)
                    break
                else:
                    print("Incorrect code sent while disarmed.")
                    stateConn1.send(current_state)
                    break

        #handle case: system is armed, set it to disarmed if code is input on webpage
        elif current_state == "armed":
            print("armed")
            while(1):
                if conn1.recv() == secretCode:
                    print("Code accepted while armed, disarming...")
                    current_state = "disarmed"
                    stateConn1.send(current_state)
                    break
                else:
                    print("Incorrect code sent while armed.")
                    stateConn1.send(current_state)
                    break


        #handle case: system is triggered, set it to disarmed if code is input on keypad
        elif current_state == "triggered":
            print("triggered")

        #handle case: system is alerted, send out the photo and maybe do other things?
        elif current_state == "alert":
            print("alert")
            

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