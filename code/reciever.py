# import time
from paho.mqtt import client as mqtt_client

broker = 'rule28.i4t.swin.edu.au'
port = 1883
topic = 'public'  # Use the same topic as the publishing code
# topic = '<103819717>/random'  # Use the same topic as the publishing code
username = '<103819717>'
password = '<103819717>'

# Function to handle incoming messages
def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client):
    def on_subscribe(client, userdata, mid, granted_qos):
        print(f"Subscribed to topic `{topic}`")

    client.subscribe(topic)
    client.on_message = on_message  # Attach the message handling function
    client.on_subscribe = on_subscribe

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()  # Start the loop to continuously check for messages

if __name__ == '__main__':
    run()
