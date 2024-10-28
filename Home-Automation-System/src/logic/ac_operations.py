import time
import urequests
import utime
import config

auto_mode_on = False
turn_on_at = 26 # default
turn_off_at = 24 # default
last_request_time = 0
auto_mode_request_interval = 900 # 15 min

def handle_auto_mode(value):
    global auto_mode_on 
    auto_mode_on = value

def handle_ac_switch(value):
    ac_switch(value)

def handle_turn_on_at(value):
    global turn_on_at
    turn_on_at = value

def handle_turn_off_at(value):
    global turn_off_at
    turn_off_at = value

def ac_switch(value):
    event = config.iftt_ac_on_event if value == True else config.iftt_ac_off_event
    send_ifttt_webhook(event)

def auto_mode_enabled():
    global auto_mode_on
    return auto_mode_on == True


def auto_mode_activate(temperature):   
    global last_request_time
 
    # Check if a request already has been sent in the last 15 min
    if (utime.time() - last_request_time) < auto_mode_request_interval:
        return
    if temperature >= turn_on_at:
        ac_switch(True)
    elif temperature <= turn_off_at:
        ac_switch(False)
    last_request_time = utime.time()


def send_ifttt_webhook(event):
    url = f"https://maker.ifttt.com/trigger/{event}/with/key/"

    response = urequests.post(url + key)
    
    if response.status_code == 200:
        print("Webhook request sent successfully.")
    else:
        print(f"Error sending webhook request. Status code: {response.status_code}")

    response.close()
