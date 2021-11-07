from GameReplay import GameReplay

game = GameReplay()
game.replay_number = 1

while not game.done:
    game.gather_input()
    game.update()
    pass
