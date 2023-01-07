import random


class Board:
    def __init__(self, sizex, sizey, bombs, first="None"):
        self.sizex = sizex
        self.sizey = sizey
        self.bombs = bombs
        self.first = first
        self.board, self.show = self.new_board()
        self.calc_board()
        self.alive = True
        self.victory = False

    def new_board(self):
        board = []
        for i in range(self.sizey):
            board.append([])
            for j in range(self.sizex):
                board[i].append("Empty")
        show = [[0 for _ in range(self.sizex)] for _ in range(self.sizey)]
        if self.first != "None":
            show[self.first[1]][self.first[0]] = 1
        board_bombs = 0
        if self.bombs >= self.sizex * self.sizey:
            raise Exception("to many bombs")
        while board_bombs < self.bombs:
            y = random.randint(0, self.sizey - 1)
            x = random.randint(0, self.sizex - 1)
            if board[y][x] == "Bomb" or show[y][x] == 1:
                continue
            board[y][x] = "Bomb"
            board_bombs += 1
        return board, show

    def calc_board(self):
        for i in range(self.sizey):
            for j in range(self.sizex):
                if self.board[i][j] == "Bomb":
                    continue
                counting_bombs = 0
                for ii in [i-1, i, i+1]:
                    for jj in [j-1, j, j+1]:
                        if ii < 0 or jj < 0 or ii >= self.sizey or jj >= self.sizex:
                            continue
                        if self.board[ii][jj] == "Bomb":
                            counting_bombs += 1
                self.board[i][j] = counting_bombs

    def click(self, x, y):
        self.show[y][x] = 1
        if self.board[y][x] == "Bomb":
            for i in range(self.sizey):
                for j in range(self.sizex):
                    self.show[i][j] = 1
            self.alive = False
        elif self.board[y][x] == 0:
            for ii in [y - 1, y, y + 1]:
                for jj in [x - 1, x, x + 1]:
                    if ii < 0 or jj < 0 or ii >= self.sizey or jj >= self.sizex:
                        continue
                    if self.show[ii][jj] == 0:
                        self.click(jj, ii)

    def did_i_win(self):
        if not self.alive:
            return self.alive
        for i in range(self.sizey):
            for j in range(self.sizex):
                if self.board[i][j] == "Bomb":
                    continue
                if self.show[i][j] == 1:
                    self.victory = True
                else:
                    self.victory = False
                    return self.alive
        if self.victory:
            self.alive = False
        return self.alive

    def __str__(self):
        a = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nBoard:\n   "
        for j in range(len(self.board[0])):
            a += '|'
            if j < 10:
                a += ' '
            a += '{} '.format(j)
            if j == len(self.board[0]) - 1:
                a += '|\n'
        a += '   '
        for j in range(len(self.board[0])):
            a += '████'
            if j == len(self.board[0]) - 1:
                a += '█'
        for i in range(len(self.board)):
            if i < 10:
                a += '\n{} █|'.format(i)
            else:
                a += '\n{}█|'.format(i)
            for j in range(len(self.board[i])):
                if (self.board[i][j] == "Empty") or (self.show[i][j] == 0):
                    a += '   |'
                elif self.board[i][j] == "Bomb":
                    a += 'XXX|'
                else:
                    a += ' {} |'.format(self.board[i][j])
        if not self.alive:
            if not self.victory:
                a += '\nDead!'
            else:
                a += '\nYou WIN!'
        return a


def game_start():
    user_input = input("Please insert board size- x,y : ")
    x = user_input.split(',')
    rowsize, colsize = int(x[0]), int(x[1])
    size = rowsize*colsize
    bombnum = int(input("How many bombs? 1-{} : ".format(size-1)))
    return rowsize, colsize, bombnum


def game_on():
    rows, cols, bombs = game_start()
    board = Board(rows, cols, bombs)
    print(board)
    alive = True
    first_click = True
    while alive:
        user_input = input("Please pick coordinates- x,y : ")
        x = user_input.split(',')
        x, y = int(x[0]), int(x[1])
        if first_click:
            board = Board(rows, cols, bombs, [x, y])
            first_click = False
        board.click(x, y)
        alive = board.did_i_win()
        print(board)


"""Can get to the recursion limitation while using big boards with small no. of bombs!"""
'''999 recursion is the limit, as long "rows * cols - bombs > 999" supposed to be OK'''

game_on()
