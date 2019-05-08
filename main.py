import pygame
from enum import Enum

class Color(Enum):
    RED = [242, 32, 9]
    GREEN = [51, 214, 42]
    YELLOW = [209, 232, 62]
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]


def getColor(color, alpha=225):
    return [*color.value, alpha]


class board:
    def __init__(self, boardx, boardy, sizex, sizey, display):
        self.boardx = boardx
        self.boardy = boardy
        self.sizex = sizex
        self.sizey = sizey
        self.display = display
        self.boardOver = getColor(Color.WHITE, 0)
        self.Board = list()
        self.createBoard()

    def createBoard(self):
        gameB = list()
        for i in range(3):
            gameB.append(list())
            for j in range(3):
                gameB[i].append(list())
                gameB[i][j] = getColor(Color.WHITE)
        self.Board = gameB

    def bigBoard(self, col=None, alpha=0):
        if col is not None:
            self.boardOver = getColor(col, alpha)
        else:
            return self.boardOver

    def boardSquares(self, x, y, col=None):
        if col is not None:
            self.Board[x][y] = getColor(col)
        else:
            return self.Board[x][y]
            
    def draw(self):
        self.display.fill((255, 255, 255))  # (0, 0, 0))
        w, h = self.display.get_size()

        for i in range(3):
            for j in range(3):
                #self.boardOver[3] = 80 #128
                for x in range(3):
                    for y in range(3):
                        sqc = self.Board[x][y]
                        # sqc[3] = 200
                        sqx = x / 2 * w
                        sqy = y / 2 * h

                        s = pygame.Surface((w/3, h/3), pygame.SRCALPHA)
                        s.fill(sqc)
                        self.display.blit(s, (sqx, sqy))

                s = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
                s.fill(self.boardOver)
                self.display.blit(s, (0, 0))

    def update(self, screen):
        self.draw()
        screen.blit(self.display, (self.boardx, self.boardy))


def drawGame(display, board):
    w, h = display.get_size()

    updateBoards(board, display)

    for i in range(10):
        posx = i / 9 * w
        posy = i / 9 * h
        if i % 3 == 0:
            pygame.draw.line(display, (0, 0, 0), (0, posy), (h, posy), 7)
            pygame.draw.line(display, (0, 0, 0), (posx, 0), (posx, h), 7)


def createBoard(wh, display):
    w, h = wh
    gboard = list()
    for i in range(3):
        gboard.append(list())
        for j in range(3):
            gboard[i].append(board(i/3*w, j/3*h, w/3, h/3, display))

    return gboard


def updateBoards(dataTable, display):
    [[j.update(display) for j in i] for i in dataTable]


pygame.init()

dispSz = [1000, 1000]

screen = pygame.display.set_mode(dispSz)

gameBoard = createBoard(dispSz, screen)


gameBoard[1][0].bigBoard(Color.GREEN, 90)
gameBoard[1][2].bigBoard(Color.GREEN)
gameBoard[2][2].bigBoard(Color.RED)
gameBoard[2][1].bigBoard(Color.YELLOW, 21)

gameBoard[2][2].boardSquares(2, 1, Color.GREEN)
gameBoard[1][2].boardSquares(1, 1, Color.RED)
gameBoard[2][0].boardSquares(1, 2, Color.RED)
gameBoard[0][0].boardSquares(2, 2, Color.GREEN)
gameBoard[0][0].boardSquares(0, 0, Color.RED)
gameBoard[2][2].boardSquares(2, 2, Color.GREEN)

for a in gameBoard:
    print(a)

drawGame(screen, gameBoard)

print(gameBoard[1][2].boardSquares(2, 1))
print(gameBoard[2][2].bigBoard())
print(Color.RED)


s = True
while s:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s = False
    drawGame(screen, gameBoard)
    pygame.display.flip()

pygame.quit()
