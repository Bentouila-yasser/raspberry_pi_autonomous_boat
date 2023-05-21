import serial
import time
import pynmea2

port = "/dev/ttyAMA0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)
dataout = pynmea2.NMEAStreamReader()

def get_gps_data():
    global gps
    gps = None
    while gps is None:
        newdata = ser.readline()
        if newdata[0:6] == b"$GNGGA":
            newmsg = pynmea2.parse(newdata.decode())
            lat = newmsg.latitude
            lng = newmsg.longitude
            if lat != 0.0 and lng != 0.0:  # Use '!=' for comparison
                gps_data = {
                    "x": lat,
                    "y": lng,
                }
                gps = gps_data
    print(gps)
    return gps
