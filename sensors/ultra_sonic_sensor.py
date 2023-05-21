import RPi.GPIO as GPIO
import math
import time

trigPin = 24  # GPIO pin for the ultrasonic sensor's trigger
echoPin = 23  # GPIO pin for the ultrasonic sensor's echo

# setup ultra sonic sensor

def setup_ultra_sonic_sensor():
    GPIO.setmode(GPIO.BCM)      # use PHYSICAL GPIO Numbering
    GPIO.setup(trigPin, GPIO.OUT)   # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN)    # set echoPin to INPUT mode
# Function to measure distance
def measure_distance():
    # Send a pulse on the trigger pin
    GPIO.output(trigPin, True)
    time.sleep(0.00001)
    GPIO.output(trigPin, False)

    # Wait for the echo pin to go high and then low
    pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(echoPin) == 0:
        pulse_start = time.time()
    while GPIO.input(echoPin) == 1:
        pulse_end = time.time()

    # Calculate the duration of the pulse and the distance in cm
    pulse_duration = pulse_end - pulse_start
    distance_cm = pulse_duration * 17150

    return distance_cm