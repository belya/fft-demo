from time import sleep


HARDCODED_SAMPLE_RATE = 256
HARDCODED_CHANNEL_NAMES = ["Channel {}".format(i) for i in range(1, 9)]


class Stream:
    chunks = []
    sample_rate = HARDCODED_SAMPLE_RATE
    channels = HARDCODED_CHANNEL_NAMES

    def __init__(self, on_chunk):
        print("Initialized")
        self.on_chunk = on_chunk

    # TODO add sliding window
    def _load_chunk(self, chunk):
        self.on_chunk(chunk)

    def receive():
        pass