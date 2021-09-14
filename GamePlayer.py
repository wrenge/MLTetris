import os
import random

import pygame

from Game import Game
from GameAction import GameAction


class GamePlayer(Game):
    time = 0
    fps = 30
    step_period = 2000
    next_step_stamp = time + step_period
    session = 0
    out_log = None
    in_log = None
    seed = 0

    def __init__(self):
        super().__init__()

        self.next_session()

        self.size = (400, 500)
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.time = self.clock.get_time()
        self.reset_cd()

    def next_session(self):

        if os.path.isfile('./PlayerSessions/progress.txt'):
            f = open("./PlayerSessions/progress.txt", "r")
            self.session = int(f.readline()) + 1
            f.close()
            f = open("./PlayerSessions/progress.txt", "w")
            f.write(f"{self.session}")
            f.close()
        else:
            if not os.path.isdir("./PlayerSessions"):
                os.mkdir("./PlayerSessions")
            f = open("./PlayerSessions/progress.txt", 'w+')
            f.write(f"{self.session}")

        if self.in_log:
            self.in_log.close()
        if self.out_log:
            self.out_log.close()

        self.in_log = open(f"./PlayerSessions/in_{self.session}.txt", "w")
        self.out_log = open(f"./PlayerSessions/out_{self.session}.txt", "w")
        self.seed = self.session
        random.seed(self.seed)
        self.tetris.reset()
        self.tetris.new_figure()

    def gather_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.input = GameAction.ROTATE
                if event.key == pygame.K_DOWN:
                    self.input = GameAction.DOWN
                if event.key == pygame.K_LEFT:
                    self.input = GameAction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.input = GameAction.RIGHT
                if event.key == pygame.K_SPACE:
                    self.input = GameAction.JUMP
                if event.key == pygame.K_ESCAPE:
                    self.input = GameAction.RESET

    def update(self):
        self.time += self.clock.get_time()

        if self.tetris.figure is None:
            self.tetris.new_figure()

        if self.input == GameAction.QUIT:
            self.done = True
        if self.input == GameAction.RESET:
            self.next_session()

        if self.tetris.playing:
            if self.input != GameAction.IGNORE:
                self.record_move(self.input)

            if self.input == GameAction.ROTATE:
                self.tetris.rotate()
            if self.input == GameAction.DOWN:
                self.tetris.go_down()
                self.reset_cd()
            if self.input == GameAction.LEFT:
                self.tetris.go_side(-1)
            if self.input == GameAction.RIGHT:
                self.tetris.go_side(1)
            if self.input == GameAction.JUMP:
                self.tetris.go_space()
                self.reset_cd()

            if self.time > self.next_step_stamp:
                self.record_move(GameAction.IGNORE)
                self.tetris.go_down()
                self.reset_cd()

        self.tetris.render(self.screen)
        pygame.display.flip()
        self.clock.tick(self.fps)
        self.input = GameAction.IGNORE

    def reset_cd(self):
        self.next_step_stamp = self.time + self.step_period

    def record_move(self, key):
        self.in_log.write(f"{self.tetris.move_count}\n")
        self.out_log.write(f"{self.tetris.move_count}\n")
        self.out_log.write(f"{key.value}\n")

        snapshot = self.tetris.make_snapshot()
        for i in snapshot:
            count = len(i)
            for j in range(0, count):
                self.in_log.write(f"{i[j]}")
                self.in_log.write('\n' if j + 1 == count else ' ')

    def quit(self):
        if self.in_log:
            self.in_log.close()
        if self.out_log:
            self.out_log.close()
