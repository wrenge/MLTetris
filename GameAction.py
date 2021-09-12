from enum import Enum


class GameAction(Enum):
    IGNORE = -1
    ROTATE = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    JUMP = 4
    RESET = 5
    QUIT = 6
