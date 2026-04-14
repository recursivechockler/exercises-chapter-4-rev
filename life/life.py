"""Game of Life."""

import numpy as np
from matplotlib import pyplot
from scipy.signal import convolve2d

glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])

blinker = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])

glider_gun = np.array(
    [
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0],
    ]
)


class Game:
    """Game of life class."""

    def __init__(self, size):
        """Initalise the game of life."""
        self.board = np.zeros((size, size))

    def play(self):
        """Play game of life."""
        print("Playing life. Press ctrl + c to stop.")
        pyplot.ion()
        while True:
            self.move()
            self.show()
            pyplot.pause(0.0000005)

    def move(self):
        """Move in game of life."""
        stencil = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        neighbour_count = convolve2d(self.board, stencil, mode="same")

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                self.board[i, j] = (
                    1
                    if (
                        neighbour_count[i, j] == 3
                        or (neighbour_count[i, j] == 2 and self.board[i, j])
                    )
                    else 0
                )

    def __setitem__(self, key, value):
        """Set an item."""
        self.board[key] = value

    def show(self):
        """Show game."""
        pyplot.clf()
        pyplot.matshow(self.board, fignum=0, cmap="binary")
        pyplot.show()

    def insert(self, pat, loc):
        """Insert pattern centred at location."""
        r, c = loc
        h, w = pat.grid.shape
        r0 = r - h // 2
        c0 = c - w // 2
        self.board[r0 : r0 + h, c0 : c0 + w] = pat.grid


class Pattern:
    """Class for GoL Pattern."""

    def __init__(self, grid):
        """Initialise the pattern."""
        self.grid = grid

    def flip_vertical(self):
        """Flip pattern vertically."""
        return Pattern(self.grid[::-1])

    def flip_horizontal(self):
        """Flip pattern horizontally."""
        return Pattern(self.grid[:, ::-1])

    def flip_diag(self):
        """Flip pattern diagonally."""
        h = len(self.grid)
        w = len(self.grid[1])
        transpose = np.zeros(shape=(w, h))

        for i in range(w):
            for j in range(h):
                transpose[i][j] = self.grid[j][i]

        return Pattern(grid=transpose)

    def rotate(self, n):
        """Rotate pattern by n right angles."""
        if n % 4 == 0:
            return self

        if n % 4 == 3:
            rotated = self.flip_diag()
            rotated = rotated.flip_horizontal()
            return rotated

        elif n % 4 == 2:
            rotated = self.flip_horizontal()
            rotated = rotated.flip_vertical()
            return rotated

        elif n % 4 == 1:
            rotated = self.flip_diag()
            rotated = rotated.flip_vertical()
            return rotated
