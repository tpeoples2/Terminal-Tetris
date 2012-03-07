# TODO(tpeoples): implement color for different brick types

import random
#import color

class Brick:
    # constants
    BRICK_L = 0
    BRICK_J = 1
    BRICK_T = 2
    BRICK_I = 3
    BRICK_Z = 4
    BRICK_S = 5
    BRICK_O = 6

    def __init__(self):
        # (x, y) is current location on the board
        self.x = 0
        self.y = 0
        self.rotation = 0 # rotation 0 = 0 degrees, 1 = 90 degrees, 2 = 180 degrees, etc.

        # randomly choose which type of Brick
        type = random.randint(0, 6)
        if type == Brick.BRICK_L:
            #self.color = ORANGE
            self.width =  3
            self.height = 2
            self.shape = [[False, False, True], [True, True, True]]
        elif type == Brick.BRICK_J:
            #self.color = BLUE
            self.width = 3
            self.height = 2
            self.shape = [[True, False, False], [True, True, True]]
        elif type == Brick.BRICK_T:
            #self.color = PURPLE
            self.width = 3
            self.height = 2
            self.shape = [[False, True, False], [True, True, True]]
        elif type == Brick.BRICK_I:
            #self.color = CYAN
            self.width = 4
            self.height = 1
            self.shape = [[True, True, True, True]]
        elif type == Brick.BRICK_Z:
            #self.color = RED
            self.width = 3
            self.height = 2
            self.shape = [[True, True, False], [False, True, True]]
        elif type == Brick.BRICK_S:
            #self.color = GREEN
            self.width = 3
            self.height = 2
            self.shape = [[False, True, True], [True, True, False]]
        elif type == Brick.BRICK_O:
            #self.color = YELLOW
            self.width = 2
            self.height = 2
            self.shape = [[True, True], [True, True]]

    def rotate(self):
        self.rotation += 1
        self.width = self.height
        self.height = self.width

        if self.rotation >= 4:
            self.rotation = 0

    def can_rotate(self, board):
        self.rotate()
        can_rotate = True

        for i in range(self.width):
            for j in range(self.height):
                if i + self.x >= len(board) or i + self.x < 0:  
                    # hits the right wall or the left wall respectively
                    can_rotate = False
                if j + self.y >= len(board[0]) or j + self.y < 0: 
                    # hits the bottom or hits the top 
                    can_rotate = False
                if self.occupies_space(i, j) and board[i + self.x][j + self.y]: 
                    # occupies_space(i, j) returns data[row][col]
                    # board[i + self.x][j + self.y] = True (there exists a brick in the location)
                    can_rotate = False

        # rotate back
        self.rotate()
        self.rotate()
        self.rotate()

        return can_rotate


    def occupies_space(self, i, j):
        if self.rotation == 0:
            col = i
            row = j
        elif self.rotation == 1:
            col = j
            row = self.width - i - 1
        elif self.rotation == 2:
            col = self.width - i - 1
            row = self.height - j - 1
        elif self.rotation == 4:
            col = self.height - j - 1
            row = i

        return self.data[row][col]







