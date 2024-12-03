# import os

# Enable onewire and temperature modules
# os.system('modprobe w1-gpio') 
# os.system('modprobe w1-therm') 
 
import glob

devices_dir = '/sys/bus/w1/devices/' # Used to find devices connected through the onewire bus
sensor_folder = glob.glob(devices_dir + '28*')[0] # The connected device we want (temp sens) is the folder 28-etc
sensor_file = sensor_folder + '/temperature' # This file contains the temperature we want in degrees C

def read_temp(): 
    # Reads the file storing the temperature
    file = open(sensor_file, 'r')
    temperature = file.read()
    file.close()
    
    t_c = float(temperature) / 1000.0 # The file does not have the decimal point, this adds it back in
    t_f = (t_c * (9.0 / 5.0)) + 32.0 # Conversion to fahrenheit 
    return str(t_c), str(round(t_f,3)) # Rounds F to 3dp to match C
    
def save_temp(temp_c, temp_f):
    # Save for display
    t_file = open("/home/tise/shared/pax_temp.txt", "w")
    t_file.write(temp_c + "°C    |    " + temp_f + "°F")
    t_file.close()
    
    # Save raw to csv
    tr_file = open("/home/tise/shared/pax_temp_raw.txt", "w")
    tr_file.write(temp_c + "," + temp_f)
    tr_file.close()
    
    # Read to terminal
    t_file = open("/home/tise/shared/pax_temp.txt", "r")
    print(t_file.read())
	
while True:
    temperature_c, temperature_f = read_temp()
    save_temp(temperature_c, temperature_f)