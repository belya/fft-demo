import json
import paho.mqtt.client as mqtt
import pandas as pd
from streams.stream import Stream
from time import sleep


HARDCODED_MQTT_HOST = "localhost"
HARDCODED_MQTT_PORT = 1883
HARDCODED_MQTT_TOPIC = "/data"
HARDCODED_MQTT_VERSION = 1


def on_connect(client, userdata, flags, rc):
    print("Connected with result code", str(rc))


def on_message(client, userdata, message):
    message_string = message.payload.decode('utf-8')
    message_json = json.loads(message_string)

    if message_json.get("version", 0) < HARDCODED_MQTT_VERSION:
        print("Message skipped, the version is too old")
        return

    chunk_df = pd.DataFrame(
        message_json["data"], 
        columns=message_json["channels"]
    )

    client.context._load_chunk(chunk_df)


class MQTTStream(Stream):
    host = HARDCODED_MQTT_HOST
    port = HARDCODED_MQTT_PORT
    topic = HARDCODED_MQTT_TOPIC
    version = HARDCODED_MQTT_VERSION

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initialize_client()

    def _initialize_client(self):
        self.client = mqtt.Client()
        self.client.context = self
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(self.host, self.port, 60)
        self.client.subscribe(self.topic)

    def receive(self):
        while True:
            self.client.loop()
            sleep(0.01)
