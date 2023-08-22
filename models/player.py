from enum import Enum

class PlayerType(Enum):
    HUMAN=0
    AI=1

# TODO: think of a proper design for this...
class Player:
    TYPE=PlayerType.HUMAN