import datetime

def getCurrentTimestamp():
    now = datetime.datetime.now()
    ct = str(now)
    
    return ct

#Test Code
#timeStamp = getCurrentTimestamp()
#print(timeStamp)