from time import sleep
import numpy as np
import pandas as pd
from handlers.handler import Handler

class FFTHandler(Handler):
    def _transform_chunk(self, chunk):
        return pd.DataFrame(
            np.absolute(np.fft.fft(chunk, axis=0))[0:chunk.shape[0] // 2], 
            columns=chunk.columns
        )


    def _convert_chunk_to_json(self, chunk):
        return [
            [channel, chunk[channel].tolist()]
            for channel in chunk.columns
        ]

    def handle(self, chunk):
        transformed_chunk = self._transform_chunk(chunk)
        transformed_chunk_json = self._convert_chunk_to_json(transformed_chunk)
        self.app.emit('bci:fft', transformed_chunk_json)
        self.app.sleep(0.1)