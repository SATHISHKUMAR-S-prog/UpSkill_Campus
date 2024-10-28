import json
import dht                
from machine import Pin
import machine
import utime
import ubinascii
import mqtt_handler
import ac_operations as ac
import light_operations as light

# Client id used in MQTT setup
client_id = ubinascii.hexlify(machine.unique_id())

# MQTT setup
try:
    mqtt_handler.setup_mqtt(client_id)
except Exception as e:
    print("Setup error: " + str(e))

# Sensors
tempSensor = dht.DHT11(Pin(27))
PIR_sensor = Pin(26, Pin.IN, Pin.PULL_UP)
LED = Pin("LED", Pin.OUT)
LED.off()

temperature_publish_interval = 900
motion_publish_interval = 60 

temperature_last_published = 0
motion_last_published = 0

def temperature_logic():
   global tempSensor
   global temperature_last_published

   tempSensor.measure()
   temperature = tempSensor.temperature()
   humidity = tempSensor.humidity()

   if utime.time() - temperature_last_published >= temperature_publish_interval:
      print("Temperature is {} degrees Celsius and Humidity is {}%".format(temperature, humidity))
      data = json.dumps({"temperature": temperature, "humidity": humidity})   
      mqtt_handler.publish_msg(msg=data)
      temperature_last_published = utime.time()

   if ac.auto_mode_enabled():
      ac.auto_mode_activate(temperature)

def motion_light_logic():
   global PIR_sensor
   global motion_last_published
   global LED
   if light.auto_mode_enabled() or light.motion_switch_enabled():
      motion = PIR_sensor.value()
      if motion == 1:
         LED.on()
         print("Motion Detected!")
         if utime.time() - motion_last_published >= motion_publish_interval:
            data = json.dumps({"motion": motion})
            mqtt_handler.publish_msg(msg=data)
            motion_last_published = utime.time()
      else:
         LED.off()
         print("No motion detected")

      if light.auto_mode_enabled():
         light.auto_mode_activate(motion)
   elif not light.motion_switch_enabled():
      LED.off()

while True:

   temperature_logic()

   motion_light_logic()

   mqtt_handler.check_msg()

   utime.sleep(1)

