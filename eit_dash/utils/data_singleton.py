from threading import Lock
from typing import List

from eitprocessing.sequence import Sequence

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

    def add_sequence(self, new_sequence: Sequence) -> None:
        self._data.append(new_sequence)

    def clear_data(self) -> None:
        self._data.clear()

    def get_all_sequences(self):
        return self._data

    def get_list_length(self):
        return len(self._data)

    def get_sequence_at(self, index: int):
        if index > (length := self.get_list_length()):
            msg = f"Index higher than list length {length}"
            raise ValueError(msg)

        return self._data[index]
