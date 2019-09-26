import pandas as pd
from time import sleep
import json
from tqdm import tqdm
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


HARDCODED_SAMPLE_RATE = 256
HARDCODED_CHANNEL_NAMES = ["Channel {}".format(i) for i in range(1, 9)]
HARDCODED_FILE_NAME = "./data/blinks.txt"
CLIENT_ID = "2aa667b7-35ff-47b1-bebf-4c6df24b18d9-3"

HARDCODED_MQTT_HOST = "akj4408rb7nrj-ats.iot.eu-central-1.amazonaws.com"
HARDCODED_MQTT_PORT = 8883
HARDCODED_MQTT_TOPIC = "test/topic/"
HARDCODED_MQTT_VERSION = 1
HARDCODED_MQTT_CREDENTIALS = ["../server/credentials/root_ca", "../server/credentials/private_key", "../server/credentials/certificate"]

DELAY = 0.1

def read_chunks():
    iterator = pd.read_csv(
        HARDCODED_FILE_NAME, 
        skiprows=6, 
        usecols=list(range(1, 9)),
        names=HARDCODED_CHANNEL_NAMES,
        chunksize=HARDCODED_SAMPLE_RATE
    )
    return iterator

def create_message(chunk):
    message_json = {
        "id": 1,
        "ch": 6,
        "freq": "1000",
    }

    for column in chunk.columns:
        message_json[column] = chunk[column].tolist()

    return json.dumps(message_json)

def send_messages(client):
    for chunk in tqdm(read_chunks(), desc="Chunks sended", unit=" chunks"):
        sleep(DELAY)
        message = create_message(chunk)
        client.publish(HARDCODED_MQTT_TOPIC, message, 1)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", str(rc))

def initialize_client():
    myMQTTClient = AWSIoTMQTTClient(CLIENT_ID)

    myMQTTClient.configureEndpoint(HARDCODED_MQTT_HOST, HARDCODED_MQTT_PORT)
    myMQTTClient.configureCredentials(*HARDCODED_MQTT_CREDENTIALS)
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    myMQTTClient.connect()

    return myMQTTClient

if (__name__ == "__main__"):
    client = initialize_client()
    while True:
        send_messages(client)

