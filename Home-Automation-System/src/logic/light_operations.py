import uyeelight
import utime
import config

bulb = uyeelight.Bulb(config.bulb_ip_addr)
auto_mode_on = False
last_motion_time = 0
motion_switch = False
no_motion_max_time = 900

def light_setup(ip_addr):
    global bulb
    bulb = uyeelight.Bulb(ip_addr)

def handle_set_brightness(value):
    bulb.set_brightness(value)

def handle_light_switch(value):
    bulb.turn_on() if value == 1 else bulb.turn_off()

def handle_auto_mode(value):
    global auto_mode_on
    auto_mode_on = value
    
def handle_motion_switch(value):
    global motion_switch
    motion_switch = value

def auto_mode_enabled():
    return auto_mode_on

def motion_switch_enabled():
    return motion_switch

def light_is_on():
    return bulb.is_on

def auto_mode_activate(motion):   
    global last_motion_time
    global no_motion_max_time
        
    if motion == 1:
        last_motion_time = utime.time()
        if not light_is_on: 
            handle_light_switch(True)
    else:
        if light_is_on and (utime.time() - last_motion_time) > no_motion_max_time:
            handle_light_switch(False)
        

