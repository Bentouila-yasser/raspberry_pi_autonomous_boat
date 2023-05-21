import serial
import adafruit_gps
#set up the gps 
ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=10)

# Create a GPS object and set the update rate
gps = adafruit_gps.GPS(ser, debug=False)
gps.send_command(b'PMTK220,1000')
gps.update_rate = 1000

def get_gps_data():
    gps.update()
    print(gps.has_fix)
    
    if gps.has_fix:
        if gps.latitude is not None and gps.longitude is not None:
            gps_data = {
                "x": gps.latitude,
                "y": gps.longitude,
            }
            return gps_data
        else:
            print('Latitude & Longitude: No data')
            return False

while True:
    gps_data = get_gps_data()
    print(gps_data)