import pygame

from Colors import WHITE, colors, GRAY
from Figure import Figure


class Tetris:
    level = 1
    score = 0
    playing = True
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None
    move_count = 0

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.playing = True
        self.move_count = 0
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def reset(self):
        self.__init__(self.height, self.width)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        self.move_count += 1
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.move_count += 1
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.playing = False

    def go_side(self, dx):
        self.move_count += 1
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        self.move_count += 1
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def make_snapshot(self):
        snapshot = []
        for row in self.field:
            snapshot.append(row.copy())

        if self.figure is not None:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.figure.image():
                        snapshot[i + self.figure.y][j + self.figure.x] = -self.figure.color

        return snapshot

    def render(self, screen):
        screen.fill(WHITE)

        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, GRAY, [self.x + self.zoom * j, self.y + self.zoom * i, self.zoom, self.zoom],
                                 1)
                if self.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[self.field[i][j]],
                                     [self.x + self.zoom * j + 1, self.y + self.zoom * i + 1, self.zoom - 2,
                                      self.zoom - 1])

        if self.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.figure.image():
                        pygame.draw.rect(screen, colors[self.figure.color],
                                         [self.x + self.zoom * (j + self.figure.x) + 1,
                                          self.y + self.zoom * (i + self.figure.y) + 1,
                                          self.zoom - 2, self.zoom - 2])
