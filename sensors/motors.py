import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

ESC_GPIO_PIN = 13
ESC_FREQUENCY = 50
ESC_MIN_DUTY_CYCLE = 5
ESC_ARM_TIME = 2
ESC_MAX_DUTY_CYCLE = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_GPIO_PIN, GPIO.OUT)

pwm = None  # PWM object instance

def get_pwm_instance():
    global pwm
    if pwm is None:
        pwm = GPIO.PWM(ESC_GPIO_PIN, ESC_FREQUENCY)
    return pwm

def arm_motors():
    pwm = get_pwm_instance()
    pwm.start(ESC_MIN_DUTY_CYCLE)
    time.sleep(ESC_ARM_TIME)

def ChangeDutyCycle(distance):
    pwm = get_pwm_instance()
    print("The distance is: %.2f cm" % distance)
    if distance > 200:
        speed = ESC_MAX_DUTY_CYCLE
        print("distance > 200 and speed",speed)
    else:
        speed = ESC_MIN_DUTY_CYCLE
        print(" and speed",speed)

    pwm.ChangeDutyCycle(speed)
