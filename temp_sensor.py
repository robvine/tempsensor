#! /usr/bin/python3

import time
#import math
import bme280_sensor
#import statistics
#from datetime import datetime
#from datetime import date
#import requests
import paho.mqtt.client as mqtt
#import board
#import busio

hasl = 743
inside_pressure = []
#today = date.today()
broker_address="192.168.1.3"
username = "mqttuser"
password = "mqttpass"

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    
def on_log(client, userdata, level, buf):
    print("log: ",buf)

#Loop to measure wind speed and report at 5-second intervals   

while True:
    #start_time = time.time()
    inside_humidity, pressure, inside_temp = bme280_sensor.read_all()
    inside_pressure = pressure + ((pressure * 9.80665 * hasl)/(287 * (273 + inside_temp + (hasl/400))))

    print("Humidity:",inside_humidity)
    print("Pressure:",inside_pressure)
    print("Inside Temp:",inside_temp)
    
    #Send to Home Assistant
    client = mqtt.Client("P1") #create new instance
    client.on_message=on_message #attach function to callback
    client.username_pw_set(username=username,password=password)
    client.connect(broker_address) #connect to broker
    client.loop_start() #start the loop
    client.subscribe("house/weather/inside_temp")
    client.subscribe("house/weather/inside_humidity")
    client.subscribe("house/weather/inside_pressure")
    client.publish("house/weather/inside_temp",('{:.2f}'.format(inside_temp)))
    client.publish("house/weather/inside_humidity",('{:.2f}'.format(inside_humidity)))
    client.publish("house/weather/inside_pressure",('{:.2f}'.format(inside_pressure)))

    client.on_log=on_log
    #time.sleep(4) # wait
    client.loop_stop() #stop the loop
    time.sleep(60)
