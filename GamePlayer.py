import os
import random

import numpy as np
import pygame

from Game import Game
from GameAction import GameAction
from MoveInfo import MoveInfo
from PIL import Image


class GamePlayer(Game):
    time = 0
    fps = 30
    step_period = 2000
    next_step_stamp = time + step_period
    out_log = None
    in_log = None
    seed = 0
    session = 1
    moves = []

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
            self.end_session()
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
        if key == GameAction.IGNORE:
            return

        snapshot = self.tetris.make_snapshot()
        self.moves.append(MoveInfo(snapshot, self.tetris.figure, key))

    def quit(self):
        pass

    def end_session(self):
        self.save_progress()
        self.save_moves()

    def save_progress(self):
        if os.path.isfile('./PlayerSessions/progress.txt'):
            f = open("./PlayerSessions/progress.txt", "w")
            f.write(f"{self.session}")
            f.close()
        else:
            if not os.path.isdir("./PlayerSessions"):
                os.mkdir("./PlayerSessions")
            f = open("./PlayerSessions/progress.txt", 'w+')
            f.write(f"{self.session}")
            f.close()

    def save_moves(self):
        session_path = f"./PlayerSessions/{self.session}/"
        if not os.path.isdir(session_path):
            os.mkdir(session_path)

        for i in range(len(self.moves)):
            img = Image.fromarray(np.uint8(np.array(self.moves[i].snapshot) * 255))
            img.save(session_path + f"{i}_{self.moves[i].move.value}.bmp")
