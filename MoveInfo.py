class MoveInfo:
    def __init__(self, field, figure, move):
        self.field = field
        self.move = move
        self.figure = []
        self.snapshot = []

        for i in range(len(field)):
            new_line = []
            for j in range(len(field[i])):
                new_line.append(0)
            self.figure.append(new_line)

        for i in range(4):
            for j in range(4):
                if i * 4 + j in figure.image():
                    self.figure[i + figure.y][j + figure.x] = figure.color

        for i in range(len(field)):
            new_line = []
            for j in range(len(field[i])):
                if field[i][j] > 0:
                    new_line.append(0.5)
                elif self.figure[i][j] > 0:
                    new_line.append(1)
                else:
                    new_line.append(0)
            self.snapshot.append(new_line)
