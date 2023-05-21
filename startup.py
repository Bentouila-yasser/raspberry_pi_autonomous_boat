import subprocess
import time

# Define the maximum number of retries
max_retries = 5
retries = 0

# run pub/sub connection
while retries < max_retries:
    try:
        subprocess.run([
            "python3", "main.py",
            "--endpoint", "a1uvcpocd2nibh-ats.iot.us-east-1.amazonaws.com",
            "--ca_file", "certs/root-CA.crt",
            "--cert", "certs/Pie_boat.cert.pem",
            "--key", "certs/Pie_boat.private.key",
            "--client_id", "basicPubSub",
            "--topic", "sdk/test/python",
        ], check=True)
        break  # If the connection is successful, exit the loop

    except subprocess.CalledProcessError:
        # Connection failed, turn on the red LED and turn off the green LED
        print("connection failed")
        retries += 1  # Increment the retry counter
        if retries < max_retries:
            time.sleep(5)  # Wait for 5 seconds before trying again