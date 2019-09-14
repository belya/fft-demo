import paho.mqtt.client as mqtt
import pandas as pd
from time import sleep
import json
from tqdm import tqdm

HARDCODED_SAMPLE_RATE = 256
HARDCODED_CHANNEL_NAMES = ["Channel {}".format(i) for i in range(1, 9)]
HARDCODED_FILE_NAME = "./data/blinks.txt"
HARDCODED_DATA_TOPIC = "/data"
HARDCODED_VERSION = 1
HOST = "127.0.0.1"
PORT = 1883
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
    return json.dumps({
        "channels": HARDCODED_CHANNEL_NAMES,
        "version": HARDCODED_VERSION,
        "data": chunk.values.tolist()
    })

def send_messages(client):
    for chunk in tqdm(read_chunks(), desc="Chunks sended", unit=" chunks"):
        sleep(DELAY)
        message = create_message(chunk)
        client.publish(HARDCODED_DATA_TOPIC, message)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", str(rc))

def initialize_client():
    client = mqtt.Client("data-publisher")
    client.on_connect = on_connect
    client.connect(HOST, PORT)
    return client

if (__name__ == "__main__"):
    client = initialize_client()
    send_messages(client)

