import time
import datetime
import RPi.GPIO as io
import csv

from temperature import TemperatureSensor as temperature

io.setmode(io.BCM)

door_pin = 23
sensor_triggered = True

io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)

count = 0
total_inches = 0
total_distance = 0
revolutions = 0
wheel_circumference = 33
start = datetime.datetime.now()
now = datetime.datetime.now()
d_prev = 0
t_prev = start
temp_reader = temperature()
written = False

def convert(inches):
    feet = float(inches) / 12.0
    return feet

def velocity(t1, t2, d1, d2):
    delta_t = (t2 - t1).seconds
    us_difference = (t2 - t1).microseconds
    delta_t = delta_t + us_difference / 1000000.0 
    delta_x = d2 - d1
    v = delta_x / delta_t
    v_converted = v * (3600.0 / 5280.0)
    return v_converted

def write_output(time, revs, dist, v_a, v_i, temp):
    with open('wheel1.csv', 'a') as csv_file:
        hedge_writer = csv.writer(csv_file, delimiter=',', quotechar='|')
        hedge_writer.writerow([time, revs, dist, v_i, v_a, temp])

while True:
    if not io.input(door_pin):
        if not sensor_triggered:
            print count
            if count % 2 == 0:
                d_prev = total_distance
                t_prev = now
                now = datetime.datetime.now()
                revolutions += 1
                total_inches += wheel_circumference 
                total_distance = convert(total_inches)
                print("Total Revolutions", revolutions)
                print("Total Distance", total_distance) 
                print("Average Velocity", str(velocity(start, now, 0, total_distance))[:3])
                print("Instant Velocity", str(velocity(t_prev, now, d_prev, total_distance))[:3])
            sensor_triggered = True
            count += 1
    if io.input(door_pin):
        if sensor_triggered:
            sensor_triggered = False
    if now.minute % 5 != 0 and written:  
        written = False
    if now.minute % 5 == 0 and not written:
        write_output(now, revolutions, total_distance, \
                     str(velocity(start, now, 0, total_distance))[:3], \
                     str(velocity(t_prev, now, d_prev, total_distance))[:3], \
                     str(temp_reader.read_temp()[1])[:4])
        written = True                                                           

                                  
                                  
