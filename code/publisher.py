import random
import time
from paho.mqtt import client as mqtt_client

broker = 'rule28.i4t.swin.edu.au'
port = 1883
topic = 'public'
# topic = '<103819717>/random'
username = '<103819717>'
password = '<103819717>'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result.rc
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    time.sleep(2)  # Allow some time for all messages to be sent before stopping the loop
    client.loop_stop()
    client.disconnect()

if __name__ == '__main__':
    run()
