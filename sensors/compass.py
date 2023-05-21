import smbus
import math

#set up the compass
# Set up the I2C bus
compass_bus = smbus.SMBus(1)

# Compass I2C address
compass_address = 0x1e

# Initialize the compass
compass_bus.write_byte_data(compass_address, 0, 0b01110000)
compass_bus.write_byte_data(compass_address, 1, 0b00100000)
compass_bus.write_byte_data(compass_address, 2, 0b00000000)

#reads the compass data
def read_compass():
    compass_bus.write_byte_data(compass_address, 0, 0b01111000) # Set to 8 samples @ 15Hz
    compass_bus.write_byte_data(compass_address, 1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
    compass_bus.write_byte_data(compass_address, 2, 0b00000000) # Continuous sampling

    x = compass_bus.read_word_data(compass_address, 3)
    y = compass_bus.read_word_data(compass_address, 7)
    z = compass_bus.read_word_data(compass_address, 5)
    
    x = (x - 32768) if x > 32767 else x
    y = (y - 32768) if y > 32767 else y
    z = (z - 32768) if z > 32767 else z

    return (x, y, z)

#trun the compass data to degrees
#todo: needs to addjute it 
def compass_data_to_degrees(x, y):
    heading = math.atan2(y, x) * (180 / math.pi)
    if heading < 0:
        heading += 360
    return heading

#get the heading of the compass
def get_compass_heading():
    compass_data = read_compass()
    compass_degrees = compass_data_to_degrees(compass_data[0], compass_data[1])
    declination_angle_degrees = -1.39
    heading = compass_degrees + declination_angle_degrees
    # Correct for when signs are reversed.
    if heading < 0:
        heading += 2*math.pi;
        
    # Check for wrap due to addition of declination.
    if heading > 2*math.pi:
        heading -= 2*math.pi;
    return heading
