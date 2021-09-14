from GameAction import GameAction
from Tetris import Tetris


class Game:
    tetris = None
    done = False
    input = GameAction.IGNORE
    seed = 0

    def __init__(self):
        self.tetris = Tetris(20, 10)

    def gather_input(self):
        pass

    def quit(self):
        pass
