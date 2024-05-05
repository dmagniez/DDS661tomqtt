#!/usr/bin/env python3
import minimalmodbus
import serial
import paho.mqtt.client as mqtt
import time

delay = 5
Mqtt_target = "192.168.1.40"

MqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"Energymeter")
MqttClient.connect(Mqtt_target,1883)
MqttClient.loop_start()


instrument = minimalmodbus.Instrument('/dev/ttyAMA0', 1)  # port name, slave address (in decimal)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_EVEN
instrument.serial.stopbits = 1
instrument.serial.timeout  = 1          # seconds
instrument.mode = minimalmodbus.MODE_RTU
instrument.clear_buffers_before_each_transaction = True

while True:
  time.sleep(delay)

  for counter, n in [('chauffage',2),('ECS',3),('PV',1)]:
    instrument.address = n

    active_power = instrument.read_float(0x12, functioncode=4)
    MqttClient.publish(counter+"/power", active_power)
    total_power = instrument.read_float(0x0100, functioncode=4)
    MqttClient.publish(counter+"/counter", total_power)

    text = f"[{counter}]Active: {active_power:.2f} KWh    "
    text += f"[{counter}]Total: {total_power:.2f} KWh    "

    print(text)