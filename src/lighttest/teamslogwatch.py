import time
import requests
import json

# Update the IP address of the Raspberry Pi and the location of the Teams logfile. 
pi_url = "http://<IP Address>:8080"
teams_logfile = "/mnt/c/Users/<user>/AppData/Roaming/Microsoft/Teams/logs.txt"

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    logfile = open(teams_logfile,"r")
    loglines = follow(logfile)
    for line in loglines:
        if "StatusIndicatorStateService: Added " in line:
            statusstr = line.split("Added ",1)[1]
            status = statusstr.split()[0]
            # Available
            # Busy
            # DoNotDisturb
            # BeRightBack
            # AppearAway
            # Away
            # Presenting            
            # Offline
            statusdata = {'status' : status}
            headers = {'Content-Type' : 'application/json'}
            print('Calling teams light API with ' + status)
            while(True):
                try:
                    response = requests.put(pi_url + "/teamsstatus?status=" + status)
                    print(response)
                    break
                except:
                    print('Retrying connection to ' + pi_url)
                    time.sleep(5)
