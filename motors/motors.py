import pigpio
import time
import keyboard
import subprocess



# Pin configuration
ESC_PIN_1 = 12
ESC_PIN_2 = 13

# ESC parameters
#YELLOW means YELLOW ESC, CUZ THEY ARE DIFFERENT IN THE pulse width in microseconds
YELLOW_MIN_PULSE_WIDTH = 1474  # Minimum pulse width in microseconds
YELLOW_MAX_PULSE_WIDTH = 1555  # Maximum pulse width in microseconds
BLEU_MIN_PULSE_WIDTH = 1144  # Minimum pulse width in microseconds
BLEU_MAX_PULSE_WIDTH = 2015  # Maximum pulse width in microseconds
ARM_DELAY = 3           # Arm delay in seconds
SPEED_INCREMENT = 5    # Speed increment in percentage

# Create pigpio object
piy = pigpio.pi()
pib = pigpio.pi()

def arm_motors():
    print("Arming ESCs...")
    piy.set_servo_pulsewidth(ESC_PIN_1,YELLOW_MIN_PULSE_WIDTH)
    pib.set_servo_pulsewidth(ESC_PIN_2, BLEU_MIN_PULSE_WIDTH)
    time.sleep(ARM_DELAY)
    time.sleep(3)  # Wait for the daemon to start
    print("ESCs armed")

def disarm_motors():
    print("Disarming ESCs...")
    piy.set_servo_pulsewidth(ESC_PIN_1, 0)
    pib.set_servo_pulsewidth(ESC_PIN_2, 0)
    time.sleep(ARM_DELAY)
    piy.stop()
    pib.stop()
    print("ESCs disarmed")

def set_speed(speed1, speed2):
    duty_cycle1 = YELLOW_MIN_PULSE_WIDTH + (speed1 / 100.0) * (YELLOW_MAX_PULSE_WIDTH - YELLOW_MIN_PULSE_WIDTH)
    duty_cycle2 = BLEU_MIN_PULSE_WIDTH + (speed2 / 100.0) * (BLEU_MAX_PULSE_WIDTH - BLEU_MIN_PULSE_WIDTH)
    duty_cycle1 = max(min(duty_cycle1, YELLOW_MAX_PULSE_WIDTH), YELLOW_MIN_PULSE_WIDTH)  # Ensure duty_cycle is within valid range
    duty_cycle2 = max(min(duty_cycle2, BLEU_MAX_PULSE_WIDTH), BLEU_MIN_PULSE_WIDTH)  # Ensure duty_cycle is within valid range
    piy.set_servo_pulsewidth(ESC_PIN_1, duty_cycle1)
    pib.set_servo_pulsewidth(ESC_PIN_2, duty_cycle2)
    print(f"Speed set to {speed1}% (duty cycle: {duty_cycle1})")
    print(f"Speed set to {speed2}% (duty cycle: {duty_cycle2})")