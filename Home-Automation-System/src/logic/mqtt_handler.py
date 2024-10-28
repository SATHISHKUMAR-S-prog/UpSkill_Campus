import json
import utime
from mqtt import MQTTClient
import ac_operations as ac
import light_operations as light

client = None
check_msg_last_executed = 0
pub_topic = b'devices/picowboard'
sub_topics = [
    b'devices/picowboard/ac_switch',
    b'devices/picowboard/ac_auto_mode',
    b'devices/picowboard/ac_turn_on_at',
    b'devices/picowboard/ac_turn_off_at',
    b'devices/picowboard/light_switch',
    b'devices/picowboard/light_brightness',
    b'devices/picowboard/light_auto_mode',
    b'devices/picowboard/motion_switch'
]

def setup_mqtt(client_id):
    global client
    client = MQTTClient(client_id,
                        server = config.mosquitto_ip_addr,
                        user = config.mosquitto_user,
                        password = config.mosquitto_pass,
                        port = 1883)

    client.set_callback(sub_cb)
    client.connect()

    for topic in sub_topics:
        client.subscribe(topic)
    print('MQTT connected')


def publish_msg(msg, topic = pub_topic):
    try:
        client.publish(topic=topic, msg=msg) 
    except Exception as e:
        print("Pub error: " + str(e))

def check_msg():
    global check_msg_last_executed
    if utime.time() - check_msg_last_executed >= 5:
        try:
            client.check_msg()
        except Exception as e:
            print("Sub error: " + str(e))
            
        check_msg_last_executed = utime.time()


def sub_cb(topic, msg):
    print((topic, msg))

    if topic in sub_topics:
        value = 0
        try:
            value = int(msg.decode())
        except (TypeError, ValueError, KeyError) as e:
            print(e)

        handle_topic(topic, value)


def handle_topic(topic, value):
    if topic == sub_topics[0]:
        ac.handle_ac_switch(value)
    elif topic == sub_topics[1]: 
        ac.handle_auto_mode(value)
    elif topic == sub_topics[2]: 
        ac.handle_turn_on_at(value)
    elif topic == sub_topics[3]: 
        ac.handle_turn_off_at(value)
    elif topic == sub_topics[4]:
        light.handle_light_switch(value)
    elif topic == sub_topics[5]:
        light.handle_set_brightness(value)
    elif topic == sub_topics[6]:
        light.handle_auto_mode(value)
    elif topic == sub_topics[7]:
        light.handle_motion_switch(value)
