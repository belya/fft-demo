from time import sleep
import numpy as np
import pandas as pd

# TODO use sample rate from file
HARDCODED_SAMPLE_RATE = 256
HARDCODED_CHANNEL_NAMES = ["Channel {}".format(i) for i in range(1, 9)]
HARDCODED_FILE_NAME = "./data/blinks.txt"


def _iterate_openbci(path):
    speed = HARDCODED_SAMPLE_RATE // 16
    df = pd.read_csv(
        path, 
        skiprows=6, 
        usecols=list(range(1, 9)),
        names=HARDCODED_CHANNEL_NAMES
    )
    for i in range(0, df.shape[0], speed):
        yield df.iloc[i:i + HARDCODED_SAMPLE_RATE]


def _transform_chunk(chunk):
    return pd.DataFrame(
        np.absolute(np.fft.fft(chunk, axis=0))[0:HARDCODED_SAMPLE_RATE // 2], 
        columns=HARDCODED_CHANNEL_NAMES
    )


def _convert_chunk_to_json(chunk):
    return [
        [channel, chunk[channel].tolist()]
        for channel in chunk.columns
    ]


def handle_fft(app):
    while True:
        for chunk in _iterate_openbci(HARDCODED_FILE_NAME):
            transformed_chunk = _transform_chunk(chunk)
            transformed_chunk_json = _convert_chunk_to_json(transformed_chunk)
            app.emit('bci:fft', transformed_chunk_json)
            app.sleep(0.1)