import serial
import time
import pynmea2

port = "/dev/ttyAMA0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)
dataout = pynmea2.NMEAStreamReader()

def get_gps_data():
    gps_data = None
    while gps_data is None:
        newdata = ser.readline()
        #filter the position data
        if newdata[0:6] == b"$GNGGA":
            newmsg = pynmea2.parse(newdata.decode())
            lat = newmsg.latitude
            lng = newmsg.longitude
            #check if module connected to the satellite
            gps_data = {
                "x": lat,
                "y": lng,
            }
    return gps_data
