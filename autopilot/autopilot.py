import threading
import time
from ultra_sonic_sensor.ultra_sonic_sensor import measure_distance, setup_ultra_sonic_sensor
from gps.gps import get_gps_data
from compass.compass import get_compass_heading
from motors.motors import arm_motors,set_speed,disarm_motors

#golab variable to define if stops the thread
global is_autopilot_running
is_autopilot_running = False

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # radius of Earth in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance * 1000  # convert to meters

def calculate_bearing(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Calculate difference in longitude
    diff_lon = lon2 - lon1

    # Calculate bearing using Haversine formula
    y = math.sin(diff_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(diff_lon)
    bearing = math.atan2(y, x)

    # Convert bearing to degrees
    bearing = math.degrees(bearing)

    # Normalize bearing to range from 0 to 360 degrees
    bearing = (bearing + 360) % 360

    return bearing
    
#golab variable to define if  stops the thred
def autopilot_function():
    global is_autopilot_running
    is_autopilot_running = True
    print("starting the autopilot",is_autopilot_running)
    # Initialize the ultrasonic sensor
    setup_ultra_sonic_sensor()
    if is_autopilot_running == True:
        print("autopilot started")
    # Start the autopilot loop
    while is_autopilot_running:
        # Check for obstacles using the ultrasonic sensor
        distance_to_obstacle = measure_distance()
        print('distance_to_obstacle',distance_to_obstacle)
        if distance_to_obstacle > 200 :
            set_speed(100,100)
        elif distance_to_obstacle > 100 :
            set_speed(50,50)
        else :
            set_speed(0,0)
        time.sleep(1)
        
    # Stop the motors and cleanup the GPIO pins
    set_speed(0,0)
    print("Autopilot stopped")

def stop_autopilot():
    global is_autopilot_running
    is_autopilot_running = False