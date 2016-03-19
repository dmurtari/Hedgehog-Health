import time
import datetime
import RPi.GPIO as io
import csv

from temperature import TemperatureSensor as temperature
from tweeter import HedgehogTweeter

io.setmode(io.BCM)

door_pin = 23
sensor_triggered = True

io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)

count = total_inches = total_distance = revolutions = d_prev = top_speed = 0
start = now = datetime.datetime.now()
written = tweeted = False
wheel_circumference = 33
t_prev = start
temp_reader = temperature()
filename = str(now.day) + str(now.month) + 'night.csv'

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
    with open(filename, 'a') as csv_file:
        hedge_writer = csv.writer(csv_file, delimiter=',', quotechar='|')
        hedge_writer.writerow([time, revs, dist, v_i, v_a, temp])

def reset():
    count = total_inches = total_distance = revolutions = d_prev = top_speed = 0
    start = now = datetime.datetime.now()
    written = tweeted = False
    filename = str(now.day) + str(now.month) + 'night.csv'
    
while True:
    if not io.input(door_pin):
        if not sensor_triggered:
            d_prev = total_distance
            t_prev = now
            now = datetime.datetime.now()
            revolutions += 1
            total_inches += wheel_circumference 
            total_distance = convert(total_inches)
            print("Total Revolutions", revolutions)
            speed = str(velocity(t_prev, now, d_prev, total_distance))[:3]
            if speed > top_speed and speed < 5:
                top_speed = speed
                
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

    current_time = datetime.datetime.now()

    if current_time.hour == 7 and not tweeted:
       tweeter = HedgehogTweeter()
       tweeter.tweet(total_distance, top_speed)
       tweeted = True

    if current_time.hour == 17 and current_time.minute == 0 and current_time.second == 0:
        reset()
