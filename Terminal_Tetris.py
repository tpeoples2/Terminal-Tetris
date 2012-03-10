#!/usr/bin/python

#TODO(tpeoples): Change level calculator
#TODO(tpeoples): Change quit to "q"
#TODO(tpeoples): Implement space to drop the current_brick
#TODO(tpeoples): Implement shadow_brick to show where the brick would fall
    # DONE, TOO FEW COLORS THOUGH

import Brick, curses, time, math, copy

BOARD_WIDTH = 10
BOARD_HEIGHT = 19
BUFFER_TIME = 3

def init_screen():
    """Initialize the screen"""
    screen = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    return screen

def init_main_window():
    """Create the main window that shows the actual tetris board"""
    main_window = curses.newwin(BOARD_HEIGHT + 2, 2 * BOARD_WIDTH + 2, 1, 5)
    main_window.nodelay(True)
    main_window.keypad(1)
    return main_window

def init_side_window(level, score, next_brick):
    """Initalize side_window that shows the current level, score, and next brick"""
    side_window = curses.newwin(BOARD_HEIGHT / 2, int(1.5 * BOARD_WIDTH), 1, 28)
    side_window.border()
    side_window.addstr(1, 2, "Level: " + str(level))
    side_window.addstr(2, 2, "Score: " + str(score))
    side_window.addstr(4, 2, "Next: ")
    draw_panel_brick(side_window, next_brick, 6, -4)
    side_window.refresh()
    return side_window

def init_hold_window(hold_brick):
    """Initialize hold window that shows the brick being held"""
    hold_window = curses.newwin(BOARD_HEIGHT / 2 - 1, int(1.5 * BOARD_WIDTH), 10, 28)
    hold_window.border()
    hold_window.addstr(1, 2, "Holding: ")
    draw_panel_brick(hold_window, hold_brick, 3, -4)
    hold_window.refresh()
    return hold_window

def init_help_window():
    """Initialize help window that shows the controls"""
    help_window = curses.newwin(BOARD_HEIGHT / 2 + 1, 3 * BOARD_WIDTH + 2,
            1, 44)
    help_window.border()
    help_window.addstr(1, 2, "Controls:")
    help_window.addstr(3, 2, "Move Brick   - L/R/D arrow")
    help_window.addstr(4, 2, "Rotate Brick - U arrow")
    help_window.addstr(5, 2, "Drop Brick   - Spacebar")
    help_window.addstr(6, 2, "Swap Brick   - x")
    help_window.addstr(7, 2, "Pause        - p")
    help_window.addstr(8, 2, "Quit         - q")
    help_window.refresh()
    return help_window


def init_board():
    """Initialize the board that holds where all static pieces are"""
    board = BOARD_WIDTH * [None]
    for i in range(BOARD_WIDTH):
        board[i] = BOARD_HEIGHT * [False]
    return board

def draw_panel_brick(window, brick, yBuff, xBuff):
    """Draw the brick in the side/hold window"""
    if brick != None:
        for i in range(brick.width):
            for j in range(brick.height):
                if brick.occupies_space(i, j):
                    window.addstr(brick.y + j + yBuff, (2 * brick.x) + (2 * i)
                            + xBuff, "  ", curses.color_pair(brick.color))

def init_colors():
    """Initialize colors"""
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_MAGENTA)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_CYAN)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_GREEN)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_YELLOW)

def welcome_player(screen):
    """Welcome the player to the game with a countdown to start"""
    screen.addstr(BOARD_HEIGHT / 2 - 5, 3, "Welcome to Terminal Tetris!")
    start_time = time.time()
    time_difference = time.time() - start_time
    while time_difference < BUFFER_TIME:
        screen.addstr(BOARD_HEIGHT / 2 - 4, 4, "Starting in..." + str(BUFFER_TIME - int(time_difference)))
        screen.refresh()
        time_difference = time.time() - start_time

def collision_occured(board, current_brick):
    """Returns true if a collision occured, false otherwise."""
    for i in range(current_brick.width):
        for j in range(current_brick.height):
            if current_brick.occupies_space(i, j):
                # is the current_brick at the bottom?
                if current_brick.y + j >= BOARD_HEIGHT:
                    return True
                # is the current_brick hitting another brick?
                elif board[current_brick.x + i][current_brick.y + j]:
                    return True
    return False

def is_game_over(board, current_brick):
    """Return true if the game is over, false otherwise"""
    for i in range(current_brick.width):
        for j in range(current_brick.height):
            if current_brick.occupies_space(i, j) and current_brick.y + j <= 0:
                return True
    return False

def check_lines(board):
    """Return the number of lines that are 'full' on the board to clear them"""
    lines_cleared = 0
    for j in range(BOARD_HEIGHT):
        full_line = True
        for i in range(BOARD_WIDTH):
            if not board[i][j]:
                full_line = False
                break
        if full_line:
            # full line, time to clear the line
            for k in range(j, 0, -1):
                for i in range(BOARD_WIDTH):
                    board[i][k] = board[i][k - 1]
            for i in range(BOARD_WIDTH):
                board[i][0] = False
            lines_cleared += 1
    return lines_cleared

def draw_board(main_window, board):
    """Draw the bricks on the board that are stationary"""
    main_window.border()
    for i in range(BOARD_WIDTH):
        for j in range(BOARD_HEIGHT):
            if board[i][j]:
                main_window.addstr(j + 1, 2 * i + 1, "  ", curses.color_pair(board[i][j]))
            else:
                main_window.addstr(j + 1, 2 * i + 1, "  ")

def draw_current_brick(main_window, current_brick):
    """Draw the current brick on the actual game board"""
    if current_brick != None:
        for i in range(current_brick.width):
            for j in range(current_brick.height):
                if current_brick.occupies_space(i, j) and (current_brick.y + j) >= 0:
                    main_window.addstr(current_brick.y + j + 1, (2 * current_brick.x) + (2 * i) + 1, "  ", curses.color_pair(current_brick.color))


def draw_shadow_brick(main_window, board, current_brick):
    """Draw the shadow brick to show where the piece will fall"""
    shadow_brick = copy.deepcopy(current_brick)
    if shadow_brick != None:
        while not collision_occured(board, shadow_brick):
            shadow_brick.y += 1
        shadow_brick.y -= 1     # move it back up
        for i in range(shadow_brick.width):
            for j in range(shadow_brick.height):
                if shadow_brick.occupies_space(i, j) and shadow_brick.y + j >= 0:
                    main_window.addstr(shadow_brick.y + j + 1, (2 * shadow_brick.x) + (2 * i) + 1, "  ", curses.color_pair(8))

def main():
    # initialize the screen 
    screen = init_screen()
    init_colors()

    # initialize the game variables
    level = 1
    score = 0
    game_over = False
    pauses_left = 3
    tabs_left = 1
    board = init_board()
    current_brick = None
    next_brick = Brick.Brick()
    next_brick.x = (BOARD_WIDTH - next_brick.width) / 2
    hold_brick = None

    # initialize windows
    main_window = init_main_window()
    side_window = init_side_window(level, score, next_brick)
    hold_window = init_hold_window(hold_brick)
    valid_side_window = False
    valid_hold_window = False

    # welcome the player
    welcome_player(screen)

    screen.clear()
    screen.refresh()
    help_window = init_help_window()
    start_time = time.time()

    # play the game
    while not game_over:
        computer_moved = False

        # get a new current_brick
        if current_brick == None:
            current_brick = next_brick
            next_brick = Brick.Brick()
            next_brick.x = (BOARD_WIDTH - next_brick.width) / 2
            valid_side_window = False
            tabs_left = 1

        # start moving the brick down
        if time.time() - start_time >= (1.0 / level):
            current_brick.y += 1
            computer_moved = True
            start_time = time.time()

        # deal with user input
        user_input = main_window.getch()
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
            if current_brick.x < (BOARD_WIDTH - current_brick.width):
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
            if not computer_moved:
                current_brick.y += 1
        elif user_input == ord(" "):
            while not collision_occured(board, current_brick):
                current_brick.y += 1
            #current_brick.y -= 1    # move it back to before collision
        elif user_input == ord("p"):     # 112 is the int value for "p"
            if pauses_left > 0:
                pauses_left -= 1
                screen.addstr(22, 2, "PAUSED, press p to continue.")
                main_window.nodelay(False)
                exit = screen.getch()
                while exit != ord("p"):
                    exit = screen.getch()
                main_window.nodelay(True)
                screen.clear()
                screen.refresh()
                # reinstate the side_window
                side_window = init_side_window(level, score, next_brick)
                # reinstate the hold_window
                hold_window = init_hold_window(hold_brick)
                # reinstate the help_window
                help_window = init_help_window()
            else:
                screen.addstr(22, 2, "No more pauses left!")
                screen.refresh()
                for i in range(3500000): # time to pause, hack...
                    i = i
                screen.clear()
                screen.refresh()
                # reinstate the side_window
                side_window = init_side_window(level, score, next_brick)
                # reinstate the hold_window
                hold_window = init_hold_window(hold_brick)
                # reinstate the help_window
                help_window = init_help_window()
        elif user_input == ord("x"):
            if tabs_left > 0:
                valid_side_window = False
                valid_hold_window = False
                if hold_brick != None:
                    hold_brick.x = (BOARD_WIDTH - hold_brick.width) / 2
                    hold_brick.y = 0
                    current_brick.x = (BOARD_WIDTH - current_brick.width) / 2
                    current_brick.y = 0
                    hold_brick, current_brick = current_brick, hold_brick
                elif hold_brick == None:
                    current_brick.x = (BOARD_WIDTH - current_brick.width) / 2
                    current_brick.y = 0
                    hold_brick, current_brick = current_brick, hold_brick
                    continue
                tabs_left -= 1
        # use backspace to end a game for debugging purposes
        elif user_input == ord("q"):
            game_over = True
            break

        collision = collision_occured(board, current_brick)
        # if there's a collision, need to put the brick onto the board
        if collision:
            # check if the game is over
            game_over = is_game_over(board, current_brick)

            # move the brick back to right before collision
            current_brick.y -= 1

            # update the board
            for i in range(current_brick.width):
                for j in range(current_brick.height):
                    if current_brick.occupies_space(i, j):
                        board[current_brick.x + i][current_brick.y + j] = current_brick.color

            # reset the current_brick
            current_brick = None

            # check for points
            lines_cleared = check_lines(board)
            # calculate new score
            if lines_cleared > 0:
                score += 2**(lines_cleared - 1) * 100
                valid_side_window = False    # score needs to be updated on screen
                curses.beep()
            # calculate level
            if score > 0:
                level = int(math.floor(math.sqrt(score) / 35) + 1)
            else:
                level = 1

        draw_board(main_window, board)
        draw_shadow_brick(main_window, board, current_brick)
        draw_current_brick(main_window, current_brick)
        main_window.refresh()

        # update and refresh all windows as needed
        if not valid_side_window:
            side_window.clear()
            side_window = init_side_window(level, score, next_brick)
            valid_side_window = True
        if not valid_hold_window:
            hold_window.clear()
            hold_window = init_hold_window(hold_brick)
            valid_hold_window = True

    # game over 
    screen.addstr(22, 2, "Game over! You made it to level " + str(level) + " and your final score was " + str(score) + ".")
    screen.addstr(23, 2, "Press q to exit.")
    exit = screen.getch()
    while exit != ord("q"):
        exit = screen.getch()

    screen.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    curses.endwin()


if __name__ == "__main__":
    main()


















