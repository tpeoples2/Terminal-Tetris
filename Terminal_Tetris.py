import curses
import random

curses.initscr()    # initialize the library, returns a WindowObject
curses.curs_set(0)  # set the cursor to invisible
window = curses.new(36, 36, 0, 0)   # nlines, ncols, begin_y, begin_x
window.keypad(1)    # if yes is 1, escape sequences are interpreted by curses
window.nodelay()    # getch will be non-blocking (program continues to run
                    # without response from getch

def collision_occured():


def show_figure():


def move_figure():


def check_lines():


def main():


