from time import sleep
import numpy as np
import pandas as pd
from streams.mqtt_stream import MQTTStream as Stream
# from streams.file_stream import FileStream as Stream

def _transform_chunk(chunk):
    return pd.DataFrame(
        np.absolute(np.fft.fft(chunk, axis=0))[0:chunk.shape[0] // 2], 
        columns=chunk.columns
    )


def _convert_chunk_to_json(chunk):
    return [
        [channel, chunk[channel].tolist()]
        for channel in chunk.columns
    ]


def _create_fft_chunk_handler(app):
    def wrap(chunk):
        transformed_chunk = _transform_chunk(chunk)
        transformed_chunk_json = _convert_chunk_to_json(transformed_chunk)
        app.emit('bci:fft', transformed_chunk_json)
        app.sleep(0.1)

    return wrap


def handle_fft(app):
    # TODO close stream
    handler = _create_fft_chunk_handler(app)
    stream = Stream(on_chunk=handler)
    stream.receive()