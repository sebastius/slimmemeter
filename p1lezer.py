#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import serial

ser = serial.Serial('/dev/ttyMetertrekker', 115200, timeout=1, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_user = "p1meter"
mqtt_password = ""
mqtt_qos = 0
mqtt_retain = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect to MQTT broker with error code: ", rc)

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with error code: ", rc)
    time.sleep(5)
    client.reconnect()

client = mqtt.Client()
client.username_pw_set(username=mqtt_user, password=mqtt_password)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(mqtt_broker, mqtt_port)


while True:
    data = ser.readline().decode('utf-8').strip()
    if "(" in data: 
        topic = data.split("(")[0]
        #print(topic)
        message = data[data.find("(") + 1:data.find(")")]
        remainder = ""
        if "*" in message:
            message, remainder = message.split("*")
            #remainder = remainder[:-1]
        if remainder:
            message = f"{message} {remainder}"
        topic = 'p1meter/' + topic
        print(topic, message)
        client.publish(topic, message)

client.disconnect()

