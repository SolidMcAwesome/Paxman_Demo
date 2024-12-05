import time
from inputimeout import inputimeout, TimeoutOccurred
import pax_temp_api, update_github

URL = "https://olayinka.net/tise"
user = 'Tise'
password = 'TEOh 8U6k 9UZD OVP8 rq9q qkhl'
tr_file_path = "P:pax_temp_raw.txt"

# Read temperatures from network drive
def get_temps():
    t_file = open(tr_file_path, "r")
    temperatures = t_file.read().split(",")
    t_file.close()
    
    update_github.run() # Update the files on github to match the network files
    return temperatures

# Continuous Monitoring
def continuous_monitoring():
    
    timeout = input("Enter update frequency (1 - 10) in seconds\n")
    if timeout == "": timeout = "1"
    timeout_length = int(timeout)
    
    print("\nContinuous temperature monitoring - enter 'x' to pause")
    Monitor = True
    while Monitor:
        ts = get_temps()
        temperatures = ts[0] + "°C    |    " + ts[1] + "°F\n"
        try:
            ii = inputimeout(prompt=temperatures, timeout=timeout_length)
            if ii == "x":
                option = input("\nPaused\nEnter x again to exit\nEnter any other key to continue\n")
                if option == "x":
                    Monitor = False
                    print("Exiting\n")
                else:
                    print("Resuming\n")
        except TimeoutOccurred:
            pass

# Alert Monitoring      
def trigger_alert(max, max_temp_setting, min_temp_setting, degree): # 0 = min, 1 = max
    if max:
        print("\nAlert!\nTemperature exceeding Maximum Value: " + max_temp_setting + degree)
    else:
        print("\nAlert!\nTemperature below Minimum Value: " + min_temp_setting + degree)
  
def alert_mode():
    d_c = input("\nChoose operation mode\nCelsius(1) or Fahrenheit(2) - Default = C\n")
    degree = "°C"
        
    min_temp = float(input("Enter Minimum Temperature\n"))
    max_temp = float(input("Enter Maximum Temperature\n"))
    
    print("\nTemperature Alert monitoring - enter 'x' to pause")
    if d_c == "1" or d_c == "":
        degree = "°C"
        d_c = 1
    if d_c == "2":
        degree = "°F"
        
    Triggered = False
    Monitor = True
    while Monitor:
        ts = get_temps()
        if d_c:
            temp = float(ts[0])
        else:
            temp = float(ts[1])
        
        if temp < min_temp:
            trigger_alert(0, str(max_temp), str(min_temp), degree)
            Triggered = True
        if temp > max_temp:
            trigger_alert(1, str(max_temp), str(min_temp), degree)
            Triggered = True
        if Triggered & (max_temp > temp > min_temp):
            print("\nTemperature Restored: " + str(temp) + degree)
            Triggered = False
            
        try:
            ii = inputimeout(prompt=f"Current Temperature: {temp}{degree}\n", timeout=2)
            if ii == "x":
                option = input("\nPaused\nEnter x again to exit\nEnter any other key to continue\n")
                if option == "x":
                    Monitor = False
                    print("Exiting\n")
                else:
                    print("Resuming\n")
        except TimeoutOccurred:
            pass

# Uploading to website
def api_upload_mode():
    Monitor = True
    while Monitor:
        pax_temp_api.upload()
        try:
            ii = inputimeout(prompt="\r", timeout=1)
            if ii == "x":
                option = input("\nPaused\nEnter x again to exit\nEnter any other key to continue\n")
                if option == "x":
                    Monitor = False
                    print("Exiting\n")
                else:
                    print("Resuming\n")
        except TimeoutOccurred:
            pass
    
Main = True
while Main:
    mode = input("\nWelcome to the Paxman Temperature Monitoring System\nSelect option\n1 - Continuous Monitoring mode\n2 - Alert mode\n3 - Online Mode\nx - Exit Program\n")
    match mode:
        case "1":
            continuous_monitoring()
        case "2":
            alert_mode()    
        case "3":
            api_upload_mode()
        case "x":
            Main = False
            print("Closing System")
            time.sleep(1)       
    time.sleep(1)