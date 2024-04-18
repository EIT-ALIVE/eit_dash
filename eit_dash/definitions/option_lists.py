from enum import Enum

from eitprocessing.filters.butterworth_filters import FILTER_TYPES


class InputFiletypes(Enum):
    """One hot encoding of input file types (EIT vendors)."""

    Timpel = 0
    Draeger = 1
    Sentec = 2


# create the filters enum, according to what has been defined in the filters module
filters = {value: idx for idx, value in enumerate(FILTER_TYPES) if FILTER_TYPES[value].available_in_gui}

FilterTypes = Enum("FilterTypes", filters)


class SignalSelections(Enum):
    """One hot encoding of selectable signals."""

    raw = 0
    airway_pressure = 1
    flow = 2
    esophageal_pressure = 3
    volume = 4
    CO2 = 5


class PeriodsSelectMethods(Enum):
    """One hot encoding of period selection methods."""

    Manual = 0


class SynchMethods(Enum):
    """One hot encoding of synchronization methods."""

    manual = 0
    algorithm_1 = 1
    algorithm_2 = 2
