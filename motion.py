import time
import RPi.GPIO as io

io.setmode(io.BCM)

door_pin = 23
sensor_triggered = True

io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)

count = 0
total_inches = 0
revolutions = 0
wheel_circumference = 33

def convert(inches):
    feet = float(inches) / 12.0
    if feet < 1000:
        return str(feet) + ' ft'
    if feet > 1000:
        miles = feet / 5280.0
        return str(miles) + ' mi'

while True:
    if not io.input(door_pin):
        if not sensor_triggered:
            print count
            if count % 2 == 0:
                revolutions += 1
                total_inches += wheel_circumference 
                print("Total revolutions", revolutions)
                print("Total distance", convert(total_inches))
            sensor_triggered = True
            count += 1
    if io.input(door_pin):
        if sensor_triggered:
            sensor_triggered = False
