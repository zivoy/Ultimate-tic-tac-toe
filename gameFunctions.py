import pygame
from enum import Enum


class Color(Enum):
    X = [242, 32, 9]
    O = [51, 214, 42]
    HIGHLIGHT = [209, 232, 62]
    WHITE = [255, 255, 255]
    GRAY = [150, 150, 150]


def getColor(color, alpha=225):
    col = [*color.value, alpha, color.name]
    return col


class board:
    def __init__(self, boardx, boardy, sizex, sizey, parts=3):
        self.boardx = boardx
        self.boardy = boardy
        self.sizex = sizex
        self.sizey = sizey
        self.parts = parts
        self.displayB = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
        self.boardOver = getColor(Color.WHITE, 0)
        self.Board = ticTacToeBoard()

    def bigBoard(self, col=None, alpha=180):
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
        for x in range(self.parts):
            for y in range(self.parts):
                sqc = self.Board[x][y][:4:]
                # sqc[3] = 200
                sqx = x / self.parts * self.sizex
                sqy = y / self.parts * self.sizey

                s = pygame.Surface((self.sizex / self.parts, self.sizey / self.parts), pygame.SRCALPHA)
                s.fill(sqc)
                self.displayB.blit(s, (sqx, sqy))

        s = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
        s.fill(self.boardOver[:4:])
        self.displayB.blit(s, (0, 0))

        drawGrid(self.displayB, 2, self.parts)

        screen.blit(self.displayB, (self.boardx, self.boardy))

    def update(self, screen):
        self.draw(screen)


def drawGrid(display, thickness, amount=3):
    w, h = display.get_size()

    for i in range(amount+1):
        posx = i / amount * w
        posy = i / amount * h

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
            gameB[i][j] = getColor(Color.WHITE, 0)
    return gameB


def createBoard(wh):
    w, h = wh
    gboard = list()
    for i in range(3):
        gboard.append(list())
        for j in range(3):
            x = round(i / 3 * w)
            y = round(j / 3 * h)
            l = round(h / 3)
            s = round(w / 3)
            gboard[i].append(board(x,y, s, l))

    replaceWith(gboard, Color.WHITE, Color.HIGHLIGHT, 80)
    return gboard


def updateBoards(dataTable, display):
    [[j.update(display) for j in i] for i in dataTable]


def handleGame(dataTable):
    masterBoard = list()
    for x, i in enumerate(dataTable):
        masterBoard.append(list())
        for j in i:
            vik = checkVictory(j.Board)
            if vik:
                j.bigBoard(vik)
            masterBoard[x].append(j.bigBoard())
    vik = checkVictory(masterBoard)
    if vik:
        print(getColor(vik)[4] + " Won")
        return vik


def clickHandler(mousePos, wh):

    bB = [0] * 2
    sB = [0] * 2
    for i in range(2):
        if mousePos[i] < 0 or mousePos[i] > wh[i]:
            return False
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
            completed = True
            currBoard.boardSquares(tile[0], tile[1], color)
            replaceWith(dataTable, Color.HIGHLIGHT, Color.WHITE, 0)
            handleGame(dataTable)
            if dataTable[tile[0]][tile[1]].bigBoard()[4] != Color.WHITE.name:
                replaceWith(dataTable, Color.WHITE, Color.HIGHLIGHT, 80)
            else:
                dataTable[tile[0]][tile[1]].bigBoard(Color.HIGHLIGHT, 80)
                replaceWith(dataTable, Color.WHITE, Color.GRAY, 80)
    return completed


def flaging(variable, option1, option2):
    if variable == option1:
        return option2
    else:
        return option1


def replaceWith(dataTable, original, changed, alpha=180):
    for i in dataTable:
        for j in i:
            if j.bigBoard()[4] == original.name:
                j.bigBoard(changed, alpha)


def checkVictory(board):
    for i in [Color.X, Color.O]:
        for x in range(3):
            for y in range(3):
                if board[0][y][4] == board[1][y][4] == board[2][y][4] == getColor(i)[4]:
                    return i
                if board[x][0][4] == board[x][1][4] == board[x][2][4] == getColor(i)[4]:
                    return i
        if board[0][0][4] == board[1][1][4] == board[2][2][4] == getColor(i)[4]:
            return i
        if board[0][2][4] == board[1][1][4] == board[2][0][4] == getColor(i)[4]:
            return i
    return False


def infromationBox(screen, screenSz, curP):
    wBox = pygame.Rect(screenSz[0]*.73, screenSz[1]*.03, screenSz[0]*.26, screenSz[1]*.94)
    pygame.draw.rect(screen, (255, 255, 255), wBox)

    cBox = pygame.Rect(screenSz[0]*.75, screenSz[1]*.06, 100, 100)
    pygame.draw.rect(screen, getColor(curP)[:4:], cBox)
