import unittest
from handlers.fft import _iterate_openbci, _transform_chunk, _convert_chunk_to_json
import numpy as np
import pandas as pd


class FFTHandlerTests(unittest.TestCase):
    def test_read(self):
        iterator = _iterate_openbci("./data/blinks.txt")
        for chunk, index in zip(iterator, range(10)):
            assert len(chunk.columns) == 8
            for column in chunk.columns:
                assert chunk[column].dtype == np.float64
            assert chunk.shape[0] == 256

    def test_transform(self):
        chunk = pd.DataFrame(np.random.randn(250, 8))
        transformed_chunk = _transform_chunk(chunk)

        assert len(transformed_chunk.columns) == 8
        for column in transformed_chunk.columns:
            assert transformed_chunk[column].dtype == np.float64
        assert transformed_chunk.shape[0] == 250

    def test_convert_to_json(self):
        chunk = pd.DataFrame(np.random.randn(250, 8))
        json = _convert_chunk_to_json(chunk)
        assert len(json) == 8
        assert len(json[0][1]) == 250