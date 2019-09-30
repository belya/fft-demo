from time import sleep
import numpy as np
import pandas as pd
from handlers.handler import Handler

FREQUENCY = 256

class SeriesHandler(Handler):
    window = pd.DataFrame()
    # TODO use frequency from request
    max_size = 10 * FREQUENCY

    def _add_chunk_to_window(self, chunk):
        self.window = pd.concat([self.window, chunk])
        self.window = self.window.iloc[-self.max_size:]

    def _convert_window_to_json(self):
        return [
            [channel, self.window[channel].tolist()]
            for channel in self.window.columns
        ]

    def handle(self, chunk):
        self._add_chunk_to_window(chunk)

        window_json = self._convert_window_to_json()
        self.app.emit('bci:series', window_json)
        self.app.sleep(0.1)