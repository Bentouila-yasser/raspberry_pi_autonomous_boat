import subprocess
from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
import json
from utils.command_line_utils import CommandLineUtils
import math
from autopilot.autopilot import autopilot_function, stop_autopilot, is_autopilot_running
from motors.motors import arm_motors,disarm_motors
from gps.gps import get_gps_data
from compass.compass import get_compass_heading

cmdData = CommandLineUtils.parse_sample_input_pubsub()
received_all_event = threading.Event()

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))

    
# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)

def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))

# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    msg = json.loads(payload.decode())
    print(f"Received message on topic {topic}: {msg}")
    # Check for autopilot start/stop messages
    global is_autopilot_running
    if "autopilot" in msg:  
        if msg["autopilot"] == "start":
            if not is_autopilot_running:
                #get the waypoints object
                #waypoints = msg.get("waypoints")
                #!modify it
                # Start a new thread
                autopilot_thread = threading.Thread(target=autopilot_function)
                autopilot_thread.start()
        elif msg["autopilot"] == "stop":
            stop_autopilot()
    else:
        # Handle other message types here
        pass

if __name__ == '__main__':
    # Start the pigpio daemon
    subprocess.run(["sudo", "pigpiod"])
    time.sleep(1)  # Wait for the daemon to start
    arm_motors()
    # Create the proxy options if the data is present in cmdData
    proxy_options = None
    if cmdData.input_proxy_host is not None and cmdData.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=cmdData.input_proxy_host,
            port=cmdData.input_proxy_port)

    # Create a MQTT connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=cmdData.input_endpoint,
        port=cmdData.input_port,
        cert_filepath=cmdData.input_cert,
        pri_key_filepath=cmdData.input_key,
        ca_filepath=cmdData.input_ca,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdData.input_clientId,
        clean_session=False,
        keep_alive_secs=30,
        http_proxy_options=proxy_options)

    if not cmdData.input_is_ci:
        print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")
    else:
        print("Connecting to endpoint with client ID")
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
# Connection successful, turn on the green LED and turn off the red LED
    print("connection success")

    message_count = cmdData.input_count
    message_topic = cmdData.input_topic
    message_string = cmdData.input_message
    # Subscribe
    print("Subscribing to topic '{}'...".format(message_topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=message_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))

    # Publish message to server desired number of times.
    # This step is skipped if message is blank.
    # This step loops forever if count was set to 0.
    while (True):
        print("starting")
        heading = get_compass_heading() #get the boat heading from the compass
        print("heading")
        position = get_gps_data() #get the boat heading from the compass
        print("position")
        message = {"heading": heading,"position":position}
        print("Publishing message to topic '{}': {}".format("route", message))
        message_json = json.dumps(message)
        try:
            mqtt_connection.publish(
                topic="route",
                payload=message_json,
                qos=mqtt.QoS.AT_LEAST_ONCE)
        except Exception as e:
            print(f"Error while publishing message: {e}")
        time.sleep(1)
    # Wait for all messages to be received.
    # This waits forever if count was set to 0.

    received_all_event.wait()

    # Disconnect

    print("Disconnecting...")
    disarm_motors()
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
