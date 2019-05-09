from gameFunctions import *

pygame.init()

dispSz = [1400, 1000]
boardSz = [1000, 1000]
gameAt = [10, 0]

screen = pygame.display.set_mode(dispSz)
pygame.display.set_caption("Ultimate Tic Tac Toe")

gameScreen = pygame.Surface(boardSz)
gameBoard = createBoard(boardSz)

s = True
startMenu = True
clock = pygame.time.Clock()

currPlayer = Color.X

imS = min(dispSz)
explanations = pygame.image.load("images/transparentImageWithExplanations.png").convert_alpha()
explanations = pygame.transform.scale(explanations, (imS, imS))
xPos = dispSz[0] / 2 - imS / 2
yPos = dispSz[1] / 2 - imS / 2
while startMenu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s = False
            startMenu = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                startMenu = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                startMenu = False
    screen.fill((255, 255, 255))

    screen.blit(explanations, (xPos, yPos))

    pygame.display.flip()

while s:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                turn = False
                mosPos = list(pygame.mouse.get_pos())
                for i in range(2):
                    mosPos[i]-=gameAt[i]
                clicked = clickHandler(mosPos, boardSz)
                if clicked:
                    turn = placeTile(gameBoard, clicked, currPlayer)
                if turn:
                    currPlayer = flaging(currPlayer, Color.X, Color.O)
    win = handleGame(gameBoard)
    if win:
        gameBoard = createBoard(boardSz)
    drawGame(gameScreen, gameBoard)
    screen.blit(gameScreen, gameAt)

    pygame.display.flip()

    clock.tick(60)
pygame.quit()
