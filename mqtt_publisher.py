## https://pypi.org/project/paho-mqtt/
import paho.mqtt.client as mqtt
import json
import requests
# Define Variables

# Ip Adress of the MQTT Broker
MQTT_HOST = "127.0.0.1"
# Port used by the MQTT Broker
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
# Name of the tpoc where data will be pushed inside the MQTT Broker
MQTT_TOPIC = "sensor-data"

# Get a sample dataset from a Rest API
response = requests.get("https://data.cincinnati-oh.gov/resource/b56d-ydmm.json?$limit=500000&$offset=0&$order=time")
MQTT_DATA = response.json()

# Define on_publish event function
def on_publish(client, userdata, mid):
    print ("Message published with mid", mid)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code :: ", str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe(MQTT_TOPIC)
    for MQTT_MSG in MQTT_DATA:
        client.publish(MQTT_TOPIC, json.dumps(MQTT_MSG))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload) # <- do you mean this payload = {...} ?
    payload = json.loads(msg.payload) # you can use json.loads to convert string to json
    print(payload['asset']) # then you can check the value
    client.disconnect() # Got message then disconnect

# Initiate MQTT Client
mqttc = mqtt.Client()

# Register publish callback function
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# Loop forever
mqttc.loop_forever()