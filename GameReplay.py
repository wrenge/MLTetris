import os
import random

import pygame

from Game import Game
from GameAction import GameAction


class GameReplay(Game):
    replay_number = 0
    input_path = "PlayerSessions/out_{0}.txt"
    fps = 30
    moves = []
    seed = 0

    def __init__(self):
        super().__init__()

        self.init_moves()
        self.next_session()
        self.size = (400, 500)
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.time = self.clock.get_time()

    def init_moves(self):
        moves_file = open(self.input_path.format(self.replay_number), "r")
        lines = moves_file.readlines()
        moves_file.close()
        for i in range(0, len(lines)):
            if (i + 1) % 2 == 0:
                self.moves.append(GameAction(int(lines[i].strip())))

    def next_session(self):
        random.seed(self.seed)
        self.tetris.reset()
        self.tetris.new_figure()

    def gather_input(self):
        if self.tetris.move_count >= len(self.moves):
            self.input = GameAction.QUIT
            return

        self.input = self.moves[self.tetris.move_count]

    def update(self):

        if self.tetris.figure is None:
            self.tetris.new_figure()

        if self.input == GameAction.QUIT:
            self.done = True

        if self.tetris.playing:
            if self.input == GameAction.ROTATE:
                self.tetris.rotate()
            if self.input == GameAction.DOWN or self.input == GameAction.IGNORE:
                self.tetris.go_down()
            if self.input == GameAction.LEFT:
                self.tetris.go_side(-1)
            if self.input == GameAction.RIGHT:
                self.tetris.go_side(1)
            if self.input == GameAction.JUMP:
                self.tetris.go_space()

        self.tetris.render(self.screen)
        pygame.display.flip()
        self.clock.tick(self.fps)
        self.input = GameAction.IGNORE