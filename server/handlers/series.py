from time import sleep
import numpy as np
import pandas as pd
from handlers.handler import Handler

class SeriesHandler(Handler):
    def _convert_chunk_to_json(self, chunk):
        return [
            [channel, chunk[channel].tolist()]
            for channel in chunk.columns
        ]

    def handle(self, chunk):
        chunk_json = self._convert_chunk_to_json(chunk)
        self.app.emit('bci:series', chunk_json)
        self.app.sleep(0.1)