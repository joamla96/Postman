from time import sleep
import paho.mqtt.client as mqtt
from signal import pause
import RPi.GPIO as GPIO
from gpiozero import LED
from hx711 import HX711
import time
import sys

# because fuck python
true = True
false = False

ledBlue = LED(17)
ledRed = LED(16)

leds = {ledBlue, ledRed }

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.

referenceUnit = 9000

# Write Debug
debug = true

print("Initializing...")

print("Check LEDs")
for led in leds:
    led.on()
    sleep(2)
    led.off()

print("Connecting MQTT")
mqttc = mqtt.Client("Pi")
mqttc.username_pw_set(username="DAeAD91yDJJrGk9TyQPyTr2rXcfrxQf0fjoIid6KMDZiNZ0aDFykWqBHqGZNl4Cq", password="")

mqttc.connect("mqtt.flespi.io", 1883)

print("Defining Behavior")
def sensorWeight(value):
    ledBlue.on()
    value = value * -1 # Flip the value, because we put the sensor reverse
    if debug:
        print("[DEBUG] Pulled weight, publishing " + str(value))

    mqttc.publish("sensor/weight", value, 0)


    if debug:
        print("[Debug] Published")
    sleep(1)
    ledBlue.off()

def cleanAndExit():
    ledRed.on()
    print("Shutting down MQTT")
    mqttc.publish("sensor/weight", "shutdown", 0)
    mqttc.disconnect()

    print("Cleaning...")
    for led in leds:
        led.close()

    print("Bye!")
    sys.exit()


hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)

print("Doing Tare, keep weight clear!")

# We wanna count down from 5, but we're too lazy to wait 5 seconds soo
print("5")
ledRed.on()
sleep(0.33)
ledRed.off()
sleep(0.33)

print("4")
ledRed.on()
sleep(0.33)
ledRed.off()
sleep(0.33)

print("3")
ledRed.on()
sleep(0.33)
ledRed.off()
sleep(0.33)

print("2")
ledRed.on()
sleep(0.33)
ledRed.off()
sleep(0.33)

print("1")
ledRed.on()
sleep(0.33)
ledRed.off()
sleep(0.33)

hx.reset()
hx.tare()

print("Tare done!")

while true:
    # noinspection PyBroadException
    # fuck python ^^ too broad exception my ass
    try:
        val = hx.get_weight(5)
        print("[Debug] Sensor Value: " + str(val))
        sensorWeight(val)

        hx.power_down() # Why? Its unknown.
        hx.power_up()
        time.sleep(3.1) # Just to not kill the cpu

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

    except Exception:
        mqttc.publish("sensor/weight", "dead", 0)
        while true:
            ledRed.on()
            time.sleep(2)
            led.off()
            time.sleep(1)
