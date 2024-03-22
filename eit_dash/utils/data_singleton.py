from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from eitprocessing.sequence import Sequence

# ruff: noqa: D102

_singleton = None
_lock = Lock()


def get_singleton():  # noqa: D103
    with _lock:
        global _singleton

        if _singleton is None:
            _singleton = LoadedData()

        return _singleton


class LoadedData:
    """Loaded data."""

    def __init__(self):
        self._data: list[Sequence] = []
        self._stable_periods: list[Period] = []

    def add_sequence(self, new_sequence: Sequence) -> None:
        self._data.append(new_sequence)

    def clear_data(self) -> None:
        self._data.clear()

    def get_all_sequences(self):
        return self._data

    def get_list_length(self):
        return len(self._data)

    def get_sequence_at(self, index: int):
        if not self.dataset_exists(index):
            msg = f"Index higher than list length {self.get_list_length()}"
            raise ValueError(msg)

        return self._data[index]

    def dataset_exists(self, index) -> bool:
        return index <= self.get_list_length()

    def add_stable_period(self, data: Sequence, dataset_index: int):
        if not self.dataset_exists(dataset_index):
            msg = f"Index higher than list length {self.get_list_length()}"
            raise ValueError(msg)

        self._stable_periods.append(Period(data, dataset_index))

    def remove_stable_period(self, index: int):
        if index > (length := len(self._stable_periods)):
            msg = f"Index higher than list length {length}"
            raise ValueError(msg)

        self._stable_periods.pop(index)

    def get_stable_periods_list_length(self):
        return len(self._stable_periods)

@dataclass
class Period:
    """Stable period."""

    _data: Sequence
    _dataset_index: int
