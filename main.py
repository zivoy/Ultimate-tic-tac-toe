import pygame


def drawGame(display, board):
    display.fill((255, 255, 255))  # (0, 0, 0))
    w, h = pygame.display.get_surface().get_size()

    sx = 1 / 7 * w * .8
    sy = 1 / 7 * h * .8
    v = .3435

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
                    sqx = posX + x * sx
                    sqy = posY + y * sx

                    s = pygame.Surface((sx, sx), pygame.SRCALPHA)
                    s.fill(sqc)
                    display.blit(s, (sqx, sqy))

            s = pygame.Surface((w * v, h * v), pygame.SRCALPHA)
            s.fill(color)
            display.blit(s, (posX, posY))

    for i in range(8):
        posx = i / 7 * w * .8 + sx
        posy = i / 7 * h * .8 + sy
        pygame.draw.line(display, (0, 0, 0), (0, posy), (h, posy), 2)
        pygame.draw.line(display, (0, 0, 0), (posx, 0), (posx, h), 2)
    for j in range(2):
        posx = j * w * v + w * v
        posy = j * h * v + h * v
        pygame.draw.line(display, (0, 0, 0), (0, posy), (h, posy), 7)
        pygame.draw.line(display, (0, 0, 0), (posx, 0), (posx, h), 7)


def createBoard():
    board = list()
    for i in range(3):
        board.append(list())
        for j in range(3):
            board[i].append([list(), list()])
            bigBoard(board, i, j, colors["white"])
            for x in range(3):
                board[i][j][1].append(list())
                for y in range(3):
                    board[i][j][1][x].append(list())
                    smallBoard(board, i, j, x, y, colors["white"])
    return board


def bigBoard(board, x, y, col=None, alpha=None):
    if alpha is None:
        alpha = 80
    if col is not None:
        board[x][y][0] = col.copy()
        board[x][y][0][3] = alpha
    else:
        return board[x][y][0]


def smallBoard(board, bx, by, x, y, col=None):
    if col is not None:
        board[bx][by][1][x][y] = col.copy()
    else:
        return board[bx][by][1][x][y]


colors = {"white": [255, 255, 255, 255],
          "red": [242, 32, 9, 255],
          "green": [51, 214, 42, 255]}

gameBoard = createBoard()

bigBoard(gameBoard, 1, 0, colors["green"], 90)
bigBoard(gameBoard, 1, 2, colors["green"])
bigBoard(gameBoard, 2, 2, colors["red"])
bigBoard(gameBoard, 2, 1, [209, 232, 62, 128])

smallBoard(gameBoard, 2, 2, 2, 1, colors["green"])
smallBoard(gameBoard, 1, 2, 1, 1, colors["red"])
smallBoard(gameBoard, 2, 0, 1, 2, colors["red"])
smallBoard(gameBoard, 0, 0, 2, 2, colors["green"])
smallBoard(gameBoard, 0, 0, 0, 0, colors["red"])
smallBoard(gameBoard, 2, 2, 2, 2, colors["green"])

pygame.init()

dispSz = [900, 900]

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
