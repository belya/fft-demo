import pandas as pd
from streams.stream import Stream


HARDCODED_FILE_NAME = "./data/blinks.txt"


class FileStream(Stream):
    file_name = HARDCODED_FILE_NAME

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.df = pd.read_csv(
            self.file_name, 
            skiprows=6, 
            usecols=list(range(1, 9)),
            names=self.channels,
            chunksize=self.sample_rate
        )

    def receive(self):
        for chunk_df in self.df:
            self._load_chunk(chunk_df)