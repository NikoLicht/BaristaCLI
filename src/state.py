from enum import Enum, auto

class Physical(Enum):
    SOLID= auto()
    LIQUID= auto()
    GAS= auto()
    SAND= auto()
    POWDER = auto()
    MUSH= auto()

class Temperature (Enum):
    COLD = auto()
    TEMPERED = auto()
    HOT = auto()
    

class Extraction(Enum):
    NONE = 0
    UNDER = 1
    MEDIUM = 2
    OVER = 3