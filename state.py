from enum import Enum

class Physical(Enum):
    SOLID= 1
    LIQUID= 2
    GAS= 3
    SAND= 4
    MUSH= 5

class Verbs (Enum):
    NORMAL= 1
    HOT= 2
    CONTAMINATED= 3
