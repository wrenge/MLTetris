import os

import pygame
import random

from GameAction import GameAction
from Colors import colors, BLACK, WHITE, GRAY
from Tetris import Tetris

# Initialize the game engine
pygame.init()

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 30
game = Tetris(20, 10)
time = clock.get_time()
step_period = 2000
next_step_stamp = time + step_period
played_by_bot = True
bot_moves = []
random.seed(2)

session_number = 0
if not played_by_bot:
    if os.path.isfile('progress.txt'):
        try:
            f = open("progress.txt", "r+")
            session_number = int(f.readline())
            f.close()
            f = open("progress.txt", "w")
            f.write(f"{session_number + 1}")
        finally:
            f.close()
    else:
        f = open("progress.txt", 'w')
        f.write(f"{session_number + 1}")

    in_log = open(f"in_{session_number}.txt", "w")
    out_log = open(f"out_{session_number}.txt", "w")
else:
    bot_moves_file = open(f"out_2.txt", "r")
    lines = bot_moves_file.readlines()
    for i in range(0, len(lines)):
        if (i + 1) % 2 == 0:
            bot_moves.append(GameAction(int(lines[i].strip())))
    bot_moves_file.close()


def get_player_input():
    global done, next_step_stamp
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.record_move(GameAction.ROTATE)
                game.rotate()
            if event.key == pygame.K_DOWN:
                game.record_move(GameAction.DOWN)
                game.go_down()
                next_step_stamp = time + step_period
            if event.key == pygame.K_LEFT:
                game.record_move(GameAction.LEFT)
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.record_move(GameAction.RIGHT)
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.record_move(GameAction.JUMP)
                game.go_space()
                next_step_stamp = time + step_period
            if event.key == pygame.K_ESCAPE and not played_by_bot:
                game.__init__(20, 10)


def get_bot_input(i):
    if i >= len(bot_moves):
        return False

    move = bot_moves[i]

    if move == GameAction.ROTATE:
        game.rotate()
    if move == GameAction.DOWN or move == GameAction.IGNORE:
        game.go_down()
    if move == GameAction.LEFT:
        game.go_side(-1)
    if move == GameAction.RIGHT:
        game.go_side(1)
    if move == GameAction.JUMP:
        game.go_space()

    return True


while not done:
    time += clock.get_time()

    if game.figure is None:
        game.new_figure()

    if not played_by_bot and time > next_step_stamp:
        if game.state == "start":
            game.record_move(GameAction.IGNORE)
            game.go_down()
            next_step_stamp = time + step_period

    if not played_by_bot:
        get_player_input()
    else:
        if not get_bot_input(game.move_count):
            done = True

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        if not played_by_bot:
            game.__init__(20, 10)
        else:
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

if in_log:
    in_log.close()
if out_log:
    out_log.close()
pygame.quit()
