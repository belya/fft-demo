from time import sleep
import pandas as pd

HARDCODED_SAMPLE_RATE = 256
HARDCODED_CHANNEL_NAMES = ["Channel {}".format(i) for i in range(1, 9)]

SPEED = 1

class Stream:
    prev_chunk = None
    handlers = []
    sample_rate = HARDCODED_SAMPLE_RATE
    channels = HARDCODED_CHANNEL_NAMES

    def __init__(self):
        print("Initialized")

    # TODO add sliding window
    def _load_chunk(self, chunk):
        if self.prev_chunk is not None:
            total_chunk = pd.concat([self.prev_chunk, chunk])
            for i in range(0, self.prev_chunk.shape[0], SPEED):
                sliding_chunk = total_chunk[i:i + chunk.shape[0]]

                for handler in self.handlers:
                    handler.handle(sliding_chunk)

        self.prev_chunk = chunk

    def add_handler(self, handler):
        self.handlers.append(handler)

    def receive(self):
        pass