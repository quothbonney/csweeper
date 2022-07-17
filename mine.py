#!/usr/bin/python3
# Open source software written by Jack D.V. Carson

import sys,os
import curses
import board_create
import numpy as np
import numpy.typing as npt
import os, sys

# Game globals
try:
    game_x, game_y = int(sys.argv[1]), int(sys.argv[2])
except Exception:
    game_x, game_y = 18, 36 
game = board_create.Board(game_x, game_y)


# Color pair dictionary
colordict = {
        '~': 4,
        '0': 8,
        '1': 5,
        '2': 6,
        '3': 7,
        '4': 1,
        '5': 9,
        '6': 9,
        '7': 9,
        '8': 9,
        'b': 2,
        'f': 2,
        }



def draw_menu(stdscr):
    # Keystroke variable
    k = 0
    
    game_still_going = True
    # Cursor start position
    cursor_x = 0
    cursor_y = 0


    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # BOMBS
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK) # EMPTY
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK) # COLOR 1
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK) # COLOR 2
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # COLOR 3
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK) # Invisible
    curses.init_pair(9, curses.COLOR_CYAN, curses.COLOR_BLACK)
    

    # Loop where k is the last character pressed
    locations = []
    flags = []

    # Starg game with board of curlies
    starting_board = np.full([game_x, game_y], "~")

    # Get character board from game global abd send it to the cache
    open_board: npt.ArrayLike = game.character_board()
    cache: npt.ArrayLike = starting_board
    mine_count = np.count_nonzero(open_board == 'b')

    # Function to open adjacent cells to expand zeros
    def open_zeros(x: int, y: int):
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if (x + i) in range(0, game_x) and (y + j) in range(0, game_y): 
                    try: 
                        cache[x + i][y + j] = open_board[x + i][y + j]
                    except Exception: pass


    while (k != ord('q')):
        
        # WASD to move
        # Modulus to prevent going too far
        # Multiplication by 2 to account for y seperation
        if k == ord('s'):
            cursor_y = ((cursor_y + 1) % game_x)
        elif k == ord('w'):
            cursor_y = ((cursor_y - 1) % game_x)
        elif k == ord('d'):
            cursor_x = ((cursor_x + 2) % (game_y * 2))
        elif k == ord('a'):
            cursor_x = ((cursor_x - 2) % (game_y * 2))
        elif k == ord(' '):
            x = int(cursor_x/2)
            if game_still_going and cache[cursor_y][x] != 'f':
                cache[cursor_y][x] = open_board[cursor_y][x]

            if cache[cursor_y][x] == 'b':
                # Render game over message
                game_still_going = False

                # Show all bombs
                for i, row in enumerate(open_board):
                    for j, elem in enumerate(row):
                        if elem == 'b': cache[i][j] = 'b'

        elif k == ord('f'):
            x = int(cursor_x/2)
            if cache[cursor_y][x] == 'f':
                cache[cursor_y][x] = '~' 
                flags.remove((cursor_y, cursor_x))
            else:
                flags.append((cursor_y, cursor_x))
                if cache[cursor_y][x] == '~': cache[cursor_y][x] = 'f'
                else: pass

        elif k == ord('n'):
            os.system(f"python3 ./mine.py {game_x} {game_y}")


        # Initialization
        height, width = stdscr.getmaxyx()

        
        # Board offset given window size
        x_offset = int((width - game_y*2) / 2)
        y_offset = int((height - game_x) / 2)

        stdscr.clear()
        height, width = stdscr.getmaxyx()

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)
        

        statusbarstr = f"Press 'q' to exit | Flags: {len(flags)} | Mines: {mine_count}"


        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.A_BOLD)

        # Print array from cache
        for i, row in enumerate(cache):
            for j, elem in enumerate(row):
                # Get color channel through dictionary
                pair: int = colordict[str(elem)]
                stdscr.attron(curses.color_pair(pair))
                stdscr.addstr(int(i+y_offset), int(x_offset+j*2), elem)
                stdscr.attroff(curses.color_pair(pair))

                if elem == '0': open_zeros(i, j)


        stdscr.move(cursor_y + y_offset, cursor_x + x_offset)
        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()


def main():
    curses.wrapper(draw_menu)



if __name__ == "__main__":
    main()
    
