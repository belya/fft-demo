import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import pandas as pd
from streams.stream import Stream
from time import sleep
import numpy as np

CLIENT_ID = "2aa667b7-35ff-47b1-bebf-4c6df24b18d9-2"

HARDCODED_MQTT_HOST = "akj4408rb7nrj-ats.iot.eu-central-1.amazonaws.com"
HARDCODED_MQTT_PORT = 8883
HARDCODED_MQTT_TOPIC = "test/topic/"
HARDCODED_MQTT_VERSION = 1
HARDCODED_MQTT_CREDENTIALS = ["credentials/root_ca", "credentials/private_key", "credentials/certificate"]


def on_connect(*args, **kwargs):
    print("Connected with result code", str(rc))


def on_message(context, message):
    message_string = message.payload.decode('utf-8')
    message_json = json.loads(message_string)

    # if message_json.get("version", 0) < HARDCODED_MQTT_VERSION:
    #     print("Message skipped, the version is too old")
    #     return

    del message_json["ch"]
    del message_json["freq"]
    del message_json["id"]

    channels = message_json.keys()

    chunk_df = pd.DataFrame(
        np.vstack([message_json[channel] for channel in channels]).T, 
        columns=channels
    )

    context._load_chunk(chunk_df)


class MQTTStream(Stream):
    host = HARDCODED_MQTT_HOST
    port = HARDCODED_MQTT_PORT
    topic = HARDCODED_MQTT_TOPIC
    version = HARDCODED_MQTT_VERSION

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initialize_client()

    def _initialize_client(self):
        self.client = AWSIoTMQTTClient(CLIENT_ID)
        self.client.configureEndpoint(HARDCODED_MQTT_HOST, HARDCODED_MQTT_PORT)
        self.client.configureCredentials(*HARDCODED_MQTT_CREDENTIALS)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.connect()

        on_message_callback = lambda s: lambda a, b, message: on_message(self, message)
        self.client.subscribe(self.topic, 1, on_message_callback(self))

    def receive(self):
        while True:
            sleep(0.01)
