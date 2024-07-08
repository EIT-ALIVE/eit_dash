from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from eitprocessing.datahandling.sequence import Sequence


_singleton = None
_lock = Lock()


def get_singleton():
    """Initialize singleton."""
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
        """Add a sequence to the singleton.

        Args:
        new_sequence: Sequence object containing the selected dataset
        """
        self._data.append(new_sequence)

    def clear_data(self) -> None:
        """Remove all data from the singleton."""
        self._data.clear()
        self._stable_periods.clear()

    def get_all_sequences(self):
        """Get all the saved sequences."""
        return self._data

    def get_sequence_list_length(self):
        """Get the number of stored sequences."""
        return len(self._data)

    def get_sequence_at(self, index: int):
        """Get the sequence wit ha given index.

        Args:
        index: Index of the sequence to be retrieved
        """
        if not self.dataset_exists(index):
            msg = f"Index higher than list length {self.get_sequence_list_length()}"
            raise ValueError(msg)

        return self._data[index]

    def get_dataset_labels(self) -> list[int]:
        """Get a list of the labels of the datasets currently available."""
        return [dataset.label for dataset in self._data]

    def get_next_dataset_label(self):
        """Determines the label to be assigned to the next dataset."""
        available_labels = self.get_dataset_labels()
        label = f"Dataset {self.get_sequence_list_length()}"

        if label in available_labels:
            for i in range(self.get_sequence_list_length()):
                label = f"Dataset {i}"
                if label not in available_labels:
                    break
        return label

    def dataset_exists(self, index: int) -> bool:
        """Verify that a sequence with the provided index exists.

        Args:
            index: Index of the sequence
        Returns: True if the sequence exists, false otherwise.
        """
        return index <= self.get_sequence_list_length()

    def add_stable_period(
        self,
        data: Sequence,
        dataset_index: int,
        period_index: int | None = None,
    ):
        """Add a stable period to the singleton.

        Args:
            data: Sequence object containing the stable period
            dataset_index: index of the reference dataset where the period has been selected
            period_index: index of the sable period.
        """
        if not self.dataset_exists(dataset_index):
            msg = f"Index higher than list length {self.get_sequence_list_length()}"
            raise ValueError(msg)

        if not period_index:
            period_index = self.get_next_period_index()

        # check that the index doesn't exist
        for period in self._stable_periods:
            if period.get_period_index() == period_index:
                msg = f"Index {period_index} exist already"
                raise ValueError(msg)

        self._stable_periods.append(Period(data, dataset_index, period_index))

    def remove_data(self, label: str):
        """Remove a sequence from data from the singleton.

        Args:
            label: label of the sequence to be removed.
        """
        for sequence in self._data:
            if sequence.label == label:
                self._data.remove(sequence)
                return

        msg = f"Sequence with label {label} not found"
        raise ValueError(msg)

    def remove_stable_period(self, index: int):
        """Remove a stable period from the singleton.

        Args:
            index: index of the sable period to be removed.
        """
        for period in self._stable_periods:
            if period.get_period_index() == index:
                self._stable_periods.remove(period)
                return

        msg = f"Period with index {index} not found"
        raise ValueError(msg)

    def get_stable_periods_list_length(self):
        """Get the number of stored periods."""
        return len(self._stable_periods)

    def get_dataset_stable_periods(self, dataset_index: int) -> list[Sequence]:
        """Retrieve the stable periods saved for a dataset.

        Args:
            dataset_index: index of the dataset
        Returns: A list of Sequences containing the stable periods.
        """
        if not self.dataset_exists(dataset_index):
            msg = f"Index higher than list length {self.get_sequence_list_length()}"
            raise ValueError(msg)

        return [period for period in self._stable_periods if period.get_dataset_index() == dataset_index]

    def get_all_stable_periods(self) -> list[Period]:
        """Retrieve all the saved stable periods.

        Returns: A list of Sequences containing the stable periods.
        """
        return self._stable_periods

    def get_stable_period(self, index: int):
        """Get a stable period from the singleton, using its index.

        Args:
            index: index of the sable period to be retrieved.
        """
        for period in self._stable_periods:
            if period.get_period_index() == index:
                return period

        msg = f"Period with index {index} not found"
        raise ValueError(msg)

    def get_stable_periods_indexes(self) -> list[int]:
        """Get a list of the indexes of the stable periods currently available."""
        return [period.get_period_index() for period in self._stable_periods]

    def get_next_period_index(self):
        """Determines the index to be assigned to the next stable period."""
        available_indexes = self.get_stable_periods_indexes()

        return max(available_indexes) + 1 if available_indexes else 0


@dataclass
class Period:
    """Stable period."""

    _data: Sequence
    _dataset_index: int
    _period_index: int

    def get_data(self) -> Sequence:
        """Get all the Sequence representing the period.

        Returns: The sequence with the period data.
        """
        return self._data

    def get_dataset_index(self) -> int:
        """Get the index of the reference dataset.

        Returns: The index of the reference dataset.
        """
        return self._dataset_index

    def get_period_index(self):
        """Get the index of the period.

        Returns: The index of the period.
        """
        return self._period_index

    def set_data(self, data: Sequence, dataset_index: int, period_index: int):
        """Add a period.

        Args:
            data: The sequence with the period data
            dataset_index: index of the reference dataset
            period_index: index of the period.
        """
        self._data = data
        self._dataset_index = dataset_index
        self._period_index = period_index

    def update_data(self, data: Sequence) -> Sequence:
        """Update the data of a period.

        Args:
            data: The sequence with the updated period data
        """
        self._data = data
