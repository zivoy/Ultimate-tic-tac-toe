import pygame
from enum import Enum


class Color(Enum):
    X = [242, 32, 9]
    O = [51, 214, 42]
    HIGHLIGHT = [209, 232, 62]
    WHITE = [255, 255, 255]


def getColor(color, alpha=225):
    col = [*color.value, alpha, color.name]
    return col


class board:
    def __init__(self, boardx, boardy, sizex, sizey):
        self.boardx = boardx
        self.boardy = boardy
        self.sizex = sizex
        self.sizey = sizey
        self.displayB = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
        self.boardOver = getColor(Color.WHITE, 0)
        self.Board = ticTacToeBoard()

    def bigBoard(self, col=None, alpha=80):
        if col is not None:
            self.boardOver = getColor(col, alpha)
        else:
            return self.boardOver

    def boardSquares(self, x, y, col=None):
        if col is not None:
            self.Board[x][y] = getColor(col)
        else:
            return self.Board[x][y]

    def draw(self, screen):
        self.displayB.fill((255, 255, 255))  # (0, 0, 0))

        # self.boardOver[3] = 80 #128
        for x in range(3):
            for y in range(3):
                sqc = self.Board[x][y][:4:]
                # sqc[3] = 200
                sqx = x / 3 * self.sizex
                sqy = y / 3 * self.sizey

                s = pygame.Surface((self.sizex / 3, self.sizey / 3), pygame.SRCALPHA)
                s.fill(sqc)
                self.displayB.blit(s, (sqx, sqy))

        s = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
        s.fill(self.boardOver[:4:])
        self.displayB.blit(s, (0, 0))

        drawGrid(self.displayB, 2)

        screen.blit(self.displayB, (self.boardx, self.boardy))

    def update(self, screen):
        self.draw(screen)


def drawGrid(display, thickness):
    w, h = display.get_size()

    for i in range(4):
        posx = i / 3 * w
        posy = i / 3 * h

        pygame.draw.line(display, (0, 0, 0), (0, posy), (h, posy), thickness)
        pygame.draw.line(display, (0, 0, 0), (posx, 0), (posx, h), thickness)


def drawGame(display, board):
    display.fill((0, 0, 0))

    updateBoards(board, display)

    drawGrid(display, 5)


def ticTacToeBoard():
    gameB = list()
    for i in range(3):
        gameB.append(list())
        for j in range(3):
            gameB[i].append(list())
            gameB[i][j] = getColor(Color.WHITE)
    return gameB


def createBoard(wh):
    w, h = wh
    gboard = list()
    for i in range(3):
        gboard.append(list())
        for j in range(3):
            gboard[i].append(board(i / 3 * w, j / 3 * h, w / 3, h / 3))

    return gboard


def updateBoards(dataTable, display):
    [[j.update(display) for j in i] for i in dataTable]


def handleGame(dataTable):
    for i in dataTable:
        for j in dataTable:
            a = j.Board
            b = j.bigBoard()


def clickHandler(mousePos, wh):
    bB = [0] * 2
    sB = [0] * 2
    for i in range(2):
        brd = mousePos[i] / wh[i] * 9
        bB[i] = int(brd / 3)
        sB[i] = int(brd) % 3

    return bB, sB


def placeTile(dataTable, clickTile, color):
    completed = False
    board = clickTile[0]
    tile = clickTile[1]
    currBoard = dataTable[board[0]][board[1]]
    if currBoard.bigBoard()[4] == Color.HIGHLIGHT.name:
        if currBoard.boardSquares(tile[0], tile[1])[4] == Color.WHITE.name:
            currBoard.boardSquares(tile[0], tile[1], color)
            completed = True
            replaceWith(dataTable, Color.HIGHLIGHT, Color.WHITE)
            dataTable[tile[0]][tile[1]].bigBoard(Color.HIGHLIGHT)
    return completed


def flaging(variable, option1, option2):
    if variable == option1:
        return option2
    else:
        return option1


def replaceWith(dataTable, original, changed):
    for i in dataTable:
        for j in i:
            if j.bigBoard()[4] == original.name:
                j.bigBoard(changed)

