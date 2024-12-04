import time
from inputimeout import inputimeout, TimeoutOccurred
import pax_temp_api

URL = "https://olayinka.net/tise"
user = 'Tise'
password = 'TEOh 8U6k 9UZD OVP8 rq9q qkhl'
tr_file_path = "P:pax_temp_raw.txt"
unit = 0
degree = "°C"

# Read temperatures from network drive
def get_temps():
    t_file = open(tr_file_path, "r")
    temperatures = t_file.read().split(",")
    t_file.close()
    
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
        temperatures = ts[unit] + degree
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
    min_temp = float(input("Enter Minimum Temperature\n"))
    max_temp = float(input("Enter Maximum Temperature\n"))
    
    print("\nTemperature Alert monitoring - enter 'x' to pause")
        
    Triggered = False
    Monitor = True
    while Monitor:
        ts = get_temps()
        temp = float(ts[unit])
        
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

def change_unit():
    global degree, unit
    selection = input("\nSelect Unit: Default = Celcius\n1 - Celcius\n2 - Fahrenheit\n")
    if selection == "2":
        degree = "°F"
        unit = 1
    else:
        degree = "°C"
        unit = 0
    
Main = True
while Main:
    mode = input("\nWelcome to the Paxman Temperature Monitoring System\nSelect option\n1 - Continuous Monitoring mode\n2 - Alert mode\n3 - Online Mode\n4 - Change unit of Temperature\nx - Exit Program\n")
    match mode:
        case "1":
            continuous_monitoring()
        case "2":
            alert_mode()    
        case "3":
            api_upload_mode()
        case "4":
            change_unit()
        case "x":
            Main = False
            print("Closing System")
            time.sleep(1)
            
    time.sleep(1)