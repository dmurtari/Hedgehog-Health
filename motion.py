import time
import RPi.GPIO as io

io.setmode(io.BCM)

door_pin = 23
sensor_triggered = True

io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)

count = 0
while True:
    if not io.input(door_pin):
        if not sensor_triggered:
            print("Sensor closed", count)
            sensor_triggered = True
            count += 1
    if io.input(door_pin):
        if sensor_triggered:
            print("Sensor opened", count)
            sensor_triggered = False
            count += 1
