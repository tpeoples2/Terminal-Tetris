import curses
import random
import time



def main():
    # initialize the screen
    screen = curses.initscr()   # initialize the library, returns a WindowObject
    valid_screen = False
    curses.start_color()        # initializes eight basic colors to use
    curses.noecho()             # each character is not repeated after entered
    curses.cbreak()             # characters are read one by one
    curses.curs_set(0)          # cursor is invisible

    # initialize the game
    board_width = 10
    board_height = 20
    level = 1
    score = 0
    game_over = False
    game_lost = False

    # create window
    window = curses.newwin(board_height + 2, 2 * board_width + 2, 0, 0)
    window.nodelay(True)    # getch() is non-blocking (doesn't wait for user input)
    window.keypad(1)        # some keys are interpreted by curses

    # initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLUE)

    # create board
    board = board_width * [None]
    for i in range(board_width):
        board[i] = board_height * [False]

    # initialize brick and timer
    current_brick = None
    start_time = time.time()

    # welcome the player
    screen.addstr(board_height / 2 - 5, 0, "Welcome to Terminal Tetris!")
    
    BUFFER_TIME = 5
    time_difference = time.time() - start_time
    while time_difference < BUFFER_TIME:
        screen.addstr((board_height / 2) - 4, 0, "Starting in..." + str((BUFFER_TIME - 1) - time_difference))
        screen.refresh()
        time_difference = time.time() - start_time

    screen.clear()
    screen.refresh()
    start_time = time.time()



