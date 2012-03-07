import curses
import time
import Brick
import math

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
    board_height = 15
    level = 1
    score = 0
    game_not_over = True

    # create window
    window = curses.newwin(board_height + 2, 2 * board_width + 2, 0, 0)
    window.nodelay(True)    # getch() is non-blocking (doesn't wait for user input)
    window.keypad(1)        # some keys are interpreted by curses

    # initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_MAGENTA)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_CYAN)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_GREEN)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_YELLOW)

    # create board
    board = board_width * [None]
    for i in range(board_width):
        board[i] = board_height * [False]


    # initialize brick and timer
    current_brick = None
    start_time = time.time()

    # welcome the player
    screen.addstr(board_height / 2 - 5, 0, "Welcome to Terminal Tetris!")

    BUFFER_TIME = 1
    time_difference = time.time() - start_time
    while time_difference < BUFFER_TIME:
        screen.addstr((board_height / 2) - 4, 0, "Starting in..." + str((BUFFER_TIME) - int(time_difference)))
        screen.refresh()
        time_difference = time.time() - start_time

    screen.clear()
    screen.refresh()
    start_time = time.time()

    while game_not_over:
        has_moved = False

        # get a new current_brick
        if current_brick == None:
            current_brick = Brick.Brick()
            current_brick.x = (board_width - current_brick.width) / 2

        # start moving the brick down
        if time.time() - start_time >= (1.0 / level):
            current_brick.y += 1
            has_moved = True
            start_time = time.time()

        # deal with user input
        user_input = window.getch()
        if user_input == curses.KEY_LEFT:
            if current_brick.x > 0:
                # can it move left?
                can_move = True
                for j in range(current_brick.height):
                    if board[current_brick.x - 1][current_brick.y + j] and current_brick.occupies_space(0, j):
                        can_move = False
                if can_move:
                    current_brick.x -= 1
        elif user_input == curses.KEY_RIGHT:
            if current_brick.x < (board_width - current_brick.width):
                # can it move right? 
                can_move = True
                for j in range(current_brick.height):
                    if board[current_brick.x + current_brick.width][current_brick.y + j] and current_brick.occupies_space(current_brick.width - 1, j):
                        can_move = False
                if can_move:
                    current_brick.x += 1
        elif user_input == curses.KEY_UP:
            if current_brick.can_rotate(board):
                current_brick.rotate()
        elif user_input == curses.KEY_DOWN:
            if not has_moved:
                current_brick.y += 1
        elif user_input == curses.KEY_BACKSPACE:
            game_not_over = False
            break

        # is the current_brick hitting something else?
        collision = False
        for i in range(current_brick.width):
            for j in range(current_brick.height):
                if current_brick.occupies_space(i, j):
                    # is the current_brick at the bottom?
                    if current_brick.y + j >= board_height:
                        collision = True
                    # is the current_brick hitting another brick?
                    elif board[current_brick.x + i][current_brick.y + j]:
                        collision = True
        # if there's a collision, need to put the brick onto the board
        if collision:
            # check if the game is over
            for i in range(current_brick.width):
                for j in range(current_brick.height):
                    if current_brick.occupies_space(i, j) and current_brick.y + j <= 0:
                        game_not_over = False

            current_brick.y -= 1    # move the brick back to right before collision
            # update the board
            for i in range(current_brick.width):
                for j in range(current_brick.height):
                    if current_brick.occupies_space(i, j):
                        #board[current_brick.x + i][current_brick.y + j] = True
                        board[current_brick.x + i][current_brick.y + j] = current_brick.color

            # reset the current_brick
            # TODO: next_brick functionality
            current_brick = None

            # check for points
            lines_cleared = 0
            for j in range(board_height):
                full_line = True
                for i in range(board_width):
                    if not board[i][j]:
                        full_line = False
                        break
                if full_line:
                    # full line, time to clear the line
                    for k in range(j, 0, -1):
                        for i in range(board_width):
                            board[i][k] = board[i][k - 1]
                    for i in range(board_width):
                        board[i][0] = False
                    lines_cleared += 1
            # calculate new score
            if lines_cleared > 0:
                score += 2**(lines_cleared - 1) * 100
                valid_screen = False    # score needs to be updated on screen
            # calculate level
            if score > 0:
                level = int(math.floor(math.sqrt(score) / 35) + 1)
            else:
                level = 1

        window.border()     # draw border of window
        # draw board
        for i in range(board_width):
            for j in range(board_height):
                if board[i][j]:
                    window.addstr(j + 1, 2 * i + 1, "  ", curses.color_pair(board[i][j]))
                else:
                    window.addstr(j + 1, 2 * i + 1, "  ")

        # draw current_brick
        if current_brick != None:
            for i in range(current_brick.width):
                for j in range(current_brick.height):
                    if current_brick.occupies_space(i, j) and (current_brick.y + j) >= 0:
                        window.addstr(current_brick.y + j + 1, (2 *
                            current_brick.x) + (2 * i) + 1, "  ", curses.color_pair(current_brick.color))

        # draw current level and score 
        screen.addstr(board_height + 3, 1, "Level: " + str(level))
        screen.addstr(board_height + 2, 1, "Score: " + str(score))

        # refresh
        window.refresh()
        if not valid_screen:
            screen.refresh()
            valid_screen = True

    # game over
    screen.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    curses.endwin()

    print "Game over! Your final score was " + str(score) + "."






if __name__ == "__main__":
    main()







