import pygame
from enum import Enum

class Color(Enum):
    RED = [242, 32, 9]
    GREEN = [51, 214, 42]
    YELLOW = [209, 232, 62]
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]


def getColor(color, alpha=225):
    return color.value, alpha


class board:
    def __init__(self, boardx, boardy, sizex, sizey):
        self.boardx = boardx
        self.boardy = boardy
        self.sizex = sizex
        self.sizey = sizey

    def createBoard(self):
        gameB = list()
        for i in range(3):
            gameB.append(list())
            for j in range(3):
                gameB[i].append(list())
                gameB[i][j] = getColor(Color.WHITE)
        self.boardOver = getColor(Color.WHITE, 0)
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
            
    def draw(self, screen):
        display.fill((255, 255, 255))  # (0, 0, 0))
        w, h = pygame.display.get_surface().get_size()
        v=.343
        for i in range(3):
            for j in range(3):
                color = boardOver
                #color[3] = 80 #128
                posX = i * w * v
                posY = j * h * v

                for x in range(3):
                    for y in range(3):
                        sqc = self.Board[x][y]
                        # sqc[3] = 200
                        sqx =  x / 2 * w
                        sqy =  y / 2 * h

                        s = pygame.Surface((10, 10), pygame.SRCALPHA)
                        s.fill(sqc)
                        display.blit(s, (sqx, sqy))

                s = pygame.Surface((w * v, h * v), pygame.SRCALPHA)
                s.fill(color)
                display.blit(s, (posX, posY))




def drawGame(display, board):
    display.fill((255, 255, 255))  # (0, 0, 0))
    w, h = pygame.display.get_surface().get_size()
    v=.343
    for i in range(3):
        for j in range(3):
            color = board[i][j][0]
            #color[3] = 80 #128
            posX = i * w * v
            posY = j * h * v

            for x in range(3):
                for y in range(3):
                    sqc = board[i][j][1][x][y]
                    # sqc[3] = 200
                    sqx =  x / 2 * w
                    sqy =  y / 2 * h

                    s = pygame.Surface((10, 10), pygame.SRCALPHA)
                    s.fill(sqc)
                    display.blit(s, (sqx, sqy))

            s = pygame.Surface((w * v, h * v), pygame.SRCALPHA)
            s.fill(color)
            display.blit(s, (posX, posY))

    for i in range(10):
        posx = i / 9 * w
        posy = i / 9 * h
        if i % 3 == 0:
            pygame.draw.line(display, (0, 0, 0), (0, posy), (h, posy), 7)
            pygame.draw.line(display, (0, 0, 0), (posx, 0), (posx, h), 7)
        else:
            pygame.draw.line(display, (0, 0, 0), (0, posy), (h, posy), 2)
            pygame.draw.line(display, (0, 0, 0), (posx, 0), (posx, h), 2)


def createBoard(w, h):
    gboard = list()
    for i in range(3):
        gboard.append(list())
        for j in range(3):
            gboard[i].append(board(i/3*w, j/3*h, w/3, h/3))

    return gboard


def updateBoards(dataTable):
    list(map(lambda x:x.update(), dataTable))


gameBoard = createBoard()

bigBoard(gameBoard, 1, 0, Color.GREEN, 90)
bigBoard(gameBoard, 1, 2, Color.GREEN)
bigBoard(gameBoard, 2, 2, Color.RED)
bigBoard(gameBoard, 2, 1, Color.YELLOW.alpha(21))

smallBoard(gameBoard, 2, 2, 2, 1, colors["green"])
smallBoard(gameBoard, 1, 2, 1, 1, colors["red"])
smallBoard(gameBoard, 2, 0, 1, 2, colors["red"])
smallBoard(gameBoard, 0, 0, 2, 2, colors["green"])
smallBoard(gameBoard, 0, 0, 0, 0, colors["red"])
smallBoard(gameBoard, 2, 2, 2, 2, colors["green"])

pygame.init()

dispSz = [1000, 1000]

screen = pygame.display.set_mode(dispSz)

drawGame(screen, gameBoard)

print(smallBoard(gameBoard, 1, 2, 2, 1))
print(bigBoard(gameBoard, 2, 2))
print(colors["red"])
'''for a in gameBoard:
    print(a)'''

s = True
while s:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s = False
    drawGame(screen, gameBoard)
    pygame.display.flip()

pygame.quit()
