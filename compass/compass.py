import smbus
import time
import math

bus = smbus.SMBus(1)
HMC5883L_address = 0x1E

def initialize_HMC5883L():
    bus.write_byte_data(HMC5883L_address, 0x00, 0x70)
    bus.write_byte_data(HMC5883L_address, 0x01, 0xA0)
    bus.write_byte_data(HMC5883L_address, 0x02, 0x00)

def read_data():
    data = bus.read_i2c_block_data(HMC5883L_address, 0x03, 6)
    x = data[0] * 256 + data[1]
    if x > 32767:
        x -= 65536
    z = data[2] * 256 + data[3]
    if z > 32767:
        z -= 65536
    y = data[4] * 256 + data[5]
    if y > 32767:
        y -= 65536
    return x, y, z

def calculate_heading(x, y):
    heading_rad = math.atan2(x,y)
    heading_deg = math.degrees(heading_rad)
    heading_deg += 90
    if heading_deg < 0:
        heading_deg += 360
    # Convert to standard compass degrees
    heading_deg = (heading_deg + 90) % 360
    return heading_deg

def calibrate_compass(duration):
    start_time = time.time()
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')

    while time.time() - start_time < duration:
        x, y, _ = read_data()
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)
        time.sleep(0.1)

    offset_x = (max_x + min_x) / 2
    offset_y = (max_y + min_y) / 2
    scale_x = (max_x - min_x) / 2
    scale_y = (max_y - min_y) / 2

    return offset_x, offset_y, scale_x, scale_y

initialize_HMC5883L()
#print("Calibrating compass for 60 seconds...")
#offset_x, offset_y, scale_x, scale_y = calibrate_compass(60)
#print(f"Calibration results: offset_x = {offset_x}, offset_y = {offset_y}, scale_x = {scale_x}, scale_y = {scale_y}")

offset_x = -21.0
offset_y = -81.5
scale_x = 163.0
scale_y = 158.5

def get_compass_heading():
    x, y, z = read_data()
    x_calibrated = (x - offset_x) / scale_x
    y_calibrated = (y - offset_y) / scale_y
    heading = calculate_heading(x_calibrated, y_calibrated)
    return heading