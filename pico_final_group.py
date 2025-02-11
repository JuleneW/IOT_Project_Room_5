# Rfinal_group.py

import time
import board
import pwmio
import wifi
import socketpool
import adafruit_requests
import ssl

# Wi-Fi Credentials
WIFI_SSID = "Victory2"
WIFI_PASSWORD = "Lassieke"

# ThingSpeak API Details
THINGSPEAK_CHANNEL_ID_GEWENST = "2792381"
THINGSPEAK_API_KEY_GEWENST = "94U2IKT6YRPREMPN"
THINGSPEAK_CHANNEL_ID_WAARDES = "2792379"
THINGSPEAK_API_KEY_WAARDES = "0OOB9HY94B6XQ63M"
THINGSPEAK_FIELD = 5
THINGSPEAK_URL_GEWENST = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID_GEWENST}/fields/{THINGSPEAK_FIELD}/last.json?api_key={THINGSPEAK_API_KEY_GEWENST}"
THINGSPEAK_URL_WAARDES = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID_WAARDES}/fields/{THINGSPEAK_FIELD}/last.json?api_key={THINGSPEAK_API_KEY_WAARDES}"

# Initialize Wi-Fi
print("Connecting to Wi-Fi...")
if not wifi.radio.ipv4_address:
    print("Failed to connect to Wi-Fi.")
    while True:
        pass  # Stop the program if no Wi-Fi connection
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()
requests = adafruit_requests.Session(pool, ssl_context)

# Set up PWM for TEMP control
RED = pwmio.PWMOut(board.GP11, frequency=1000)
GREEN = pwmio.PWMOut(board.GP12, frequency=1000)
BLUE = pwmio.PWMOut(board.GP13, frequency=1000)
    
def get_thingspeak_value_GEWENST():
    try:
        response_temp_GEWENST = requests.get(THINGSPEAK_URL_GEWENST)
        data_temp_GEWENST = response_temp_GEWENST.json()
        value_temp_GEWENST = float(data_temp_GEWENST["field5"])  # Adjust for your field
        
        return value_temp_GEWENST
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    
def get_thingspeak_value_WAARDES():
    try:
        response_temp_WAARDES = requests.get(THINGSPEAK_URL_WAARDES)
        data_temp_WAARDES = response_temp_WAARDES.json()
        value_temp_WAARDES = float(data_temp_WAARDES["field5"])  # Adjust for your field
        
        return value_temp_WAARDES
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def set_rgb_color(red, green, blue):
    # Set the RGB LED color using PWM values (0 to 65535)
    RED.duty_cycle = red
    GREEN.duty_cycle = green
    BLUE.duty_cycle = blue
    
while True:
    # Read value from ThingSpeak
    value_temp_WAARDES = get_thingspeak_value_WAARDES()
    value_temp_GEWENST = get_thingspeak_value_GEWENST()
    if value_temp_WAARDES is not None and value_temp_GEWENST is not None:
        print(f"Room temperature: {value_temp_WAARDES} °C")
        print(f"Desired temperature: {value_temp_GEWENST} °C")
        print("-----------------------------")
        if value_temp_GEWENST == value_temp_WAARDES:
            set_rgb_color(0, 65535, 0)  # GREEN
            print("Temperature ok")
        elif value_temp_GEWENST > value_temp_WAARDES:
            set_rgb_color(65535, 0, 0)  # RED
            print("Heater on")
        else:
            set_rgb_color(0, 0, 65535)  # BLUE
            print("Airco on")
        print("-----------------------------")
    
    time.sleep(10)
