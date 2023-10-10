from enum import Enum


class InputFiletypes(Enum):
    Timpel = 0
    Draeger = 1
    Sentec = 2
    Biopac = 3
    Poly5 = 4


class SignalSelections(Enum):
    airway_pressure = 0
    flow = 1
    esophageal_pressure = 2
    ignored = 3


class PeriodsSelectMethods(Enum):
    Manual = 0
    AutomatedStablePeriods = 1
    AutomatedPEEP = 2


class SynchMethods(Enum):
    manual = 0
    algorithm_1 = 1
    algorithm_2 = 2
