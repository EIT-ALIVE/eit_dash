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