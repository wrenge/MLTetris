from GamePlayer import GamePlayer

game = GamePlayer()

while not game.done:
    game.gather_input()
    game.update()
    pass
