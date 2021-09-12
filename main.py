from GamePlayer import GamePlayer
from GameReplay import GameReplay

# game = GamePlayer()
game = GameReplay()

while not game.done:
    game.gather_input()
    game.update()
    pass
