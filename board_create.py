import numpy as np
import numpy.typing as npt
from typing import List, Tuple

class Board:
    """
    Initialize game board
    """
    def __init__(self, x: int, y: int, starting: Tuple[int]):
        # Define board size
        self.x, self.y = x, y
        
        self.starting: Tuple[int] = starting
        self.bombs: npt.ArrayLike = self.bomb_locations()
        
        self.values = self.values()
        

    def bomb_locations(self, threshold:float =0.9) -> np.ndarray:
        """
        Returns np.ndarray of random bomb locations as boolean array
        Paramters: threshold (default 0.8)
        """
        # Flatten arrays to allow for easy iteration
        rand_array = np.random.rand(self.x*self.y)
        bool_array = np.empty([self.x*self.y], dtype=np.bool8)
        for i in range(len(rand_array)):
           bool_array[i] = rand_array[i] > threshold


        new_array = bool_array.reshape(self.x, self.y)
        new_array[self.starting[0]][self.starting[1]] = False

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
                value: int = None
                if elem == True: value = 255 
                elif elem == False:
                    value = 0
                    # range (-1, 2, 1) is equivalent to [-1, 0, 1]
                    for k in range(-1, 2, 1):
                        for n in range(-1, 2, 1):
                            # check if neighbor index exists
                            if (i + k) in range(0, self.x) and (j + n) in range(0, self.y):
                                value += int(self.bombs[i+k][j+n])
                                
                else: 
                    raise TypeError(f"Failed to determine state of Boolean in bomb array at index {[i, j]}");
                    value = 254
                empty_array.append(value)
        
        new_array = np.array(empty_array).reshape(self.x, self.y) 
        return new_array 


class State:
    def __init__(self, x: int, y: int, values: npt.ArrayLike, locations: List[Tuple[int]], flags: List[Tuple[int]]):
        self.locs = locations
        self.values = values
        self.flags = flags
        self.x, self.y = x, y

    def get_print_board(self):
        board = np.full([self.x, self.y], "~")
        self.print_board = board
        for x0, y0 in self.locs:
            if self.values[x0][y0] == 255:
                board[x0][y0] = 'b'
            else: board[x0][y0] = str(self.values[x0][y0])

        for x0, y0 in self.flags:
            board[x0][y0] = 'f'
        return board
        
        
        
if __name__ == '__main__':
    x, y = 10, 10

    np.random.seed(1234567)
    game = Board(x, y)
    print(game.values)
    state = State(x, y, game.values, locations=[(1,1), (3, 2)])
    print(state.get_print_board())
    
    

