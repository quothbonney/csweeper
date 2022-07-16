import numpy as np
import numpy.typing as npt
from typing import List, Tuple


class Board:
    """
    Initialize game board
    """

    def __init__(self, x: int, y: int):
        # Define board size
        self.x, self.y = x, y

        self.bombs: npt.ArrayLike = self.bomb_locations()

        self.values = self.values()

    def bomb_locations(self, threshold: float = 0.9) -> np.ndarray:
        """
        Returns np.ndarray of random bomb locations as boolean array
        Parameters: threshold (default 0.8)
        """
        # Flatten arrays to allow for easy iteration
        rand_array = np.random.rand(self.x * self.y)
        bool_array = np.empty([self.x * self.y], dtype=np.bool8)
        for i in range(len(rand_array)):
            bool_array[i] = rand_array[i] > threshold

        new_array = bool_array.reshape(self.x, self.y)

        return new_array

    def values(self) -> np.ndarray:
        """
        Iterate across ndarray self.bombs
        
        Value = true (bomb): It is set as 255
        Value = false (no bomb): 
            Check for existance of each neighbor (in range)
            Sum int(bool) for all neighbors
            return sum

        Parameters: none
        """
        empty_array = []
        for i, row in enumerate(self.bombs):
            for j, elem in enumerate(row):
                value: int = 0
                if elem:
                    value = 255
                elif elem == False:
                    value = 0
                    # range (-1, 2, 1) is equivalent to [-1, 0, 1]
                    for k in range(-1, 2, 1):
                        for n in range(-1, 2, 1):
                            # check if neighbor index exists
                            if (i + k) in range(0, self.x) and (j + n) in range(0, self.y):
                                value += int(self.bombs[i + k][j + n])

                else:
                    raise TypeError(f"Failed to determine state of Boolean in bomb array at index {[i, j]}");
                    value = 254

                empty_array.append(value)

        new_array = np.array(empty_array).reshape(self.x, self.y)
        return new_array

    def character_board(self) -> np.ndarray:
        """
        Convert int array self.values into a character array
        """
        char_board = np.empty([self.x, self.y], dtype=np.str_)
        for i, row in enumerate(self.values):
            for j, elem in enumerate(row):
                if elem == 255:
                    char_board[i][j] = 'b'
                else:
                    char_board[i][j] = str(elem)

        return char_board


class State:
    def __init__(self, board: object, locations: List[Tuple[int]], flags: List[Tuple[int]]):
        self.super = board
        self.master = board.character_board()

        self.flags = flags
        self.locs = locations

    def get_print_board(self):
        game_board = np.full([self.super.x, self.super.y], "~")
        for x0, y0 in self.locs:
            game_board[x0][y0] = self.master[x0][y0]

        for x0, y0 in self.flags:
            game_board[x0][y0] = 'f'
        return game_board


if __name__ == '__main__':
    x, y = 10, 10

    np.random.seed(1234567)
    game = Board(x, y)
    locs = [(1, 1), (2, 3), (5, 5)]
    flags = []
    state = State(game, locs, flags)

    print(game.character_board())
