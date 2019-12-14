from time import sleep
import paho.mqtt.client as mqtt
from signal import pause

from gpiozero import LED
from hx711 import HX711
import time
import sys

print("Initializing...")


print("Setting up LEDs and Buttons")
led = LED(18)

print("Connecting MQTT")
mqttc = mqtt.Client("Pi")
mqttc.username_pw_set(username="DAeAD91yDJJrGk9TyQPyTr2rXcfrxQf0fjoIid6KMDZiNZ0aDFykWqBHqGZNl4Cq", password="")

mqttc.connect("mqtt.flespi.io", 1883)


def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("[DEBUG] message received " , msg)

    if msg == "true":
        led.on()

    if msg == "false":
        led.off()



mqttc.on_message = on_message
mqttc.subscribe("notification/mail")


mqttc.loop_forever()