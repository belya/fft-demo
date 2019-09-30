from time import sleep
import pandas as pd

HARDCODED_SAMPLE_RATE = 256
HARDCODED_CHANNEL_NAMES = ["Channel {}".format(i) for i in range(1, 9)]

SPEED = 10

class Stream:
    prev_chunk = None
    handlers = []
    sample_rate = HARDCODED_SAMPLE_RATE
    channels = HARDCODED_CHANNEL_NAMES

    def __init__(self):
        print("Initialized")

    # TODO add sliding window
    def _load_chunk(self, chunk):
        for handler in self.handlers:
            handler.handle(chunk)

    def add_handler(self, handler):
        self.handlers.append(handler)

    def receive(self):
        pass