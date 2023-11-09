from threading import Lock
from typing import List

from eitprocessing.binreader.sequence import Sequence


_singleton = None
_lock = Lock()


def get_singleton():
    with _lock:
        global _singleton

        if _singleton is None:
            _singleton = LoadedData()

        return _singleton


class LoadedData:

    def __init__(self):
        self._data: List[Sequence] = []

    def get_all_sequences(self):
        return self._data

    def add_sequence(self, new_sequence: Sequence):
        self._data.append(new_sequence)

    def clear_data(self):
        self._data.clear()
