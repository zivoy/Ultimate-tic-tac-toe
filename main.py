from gameFunctions import *

pygame.init()

sz = 800

boardSz = [sz, sz]
dispSz = [int(sz * 1.4), int(sz * 1.02)]
gameAt = [int(sz * .01), int(sz * .01)]

screen = pygame.display.set_mode(boardSz)
pygame.display.set_caption("Ultimate Tic Tac Toe")

gameScreen = pygame.Surface(boardSz)
gameBoard = createBoard(boardSz)

s = True
startMenu = True
clock = pygame.time.Clock()

currPlayer = Color.X

explanations = pygame.image.load("images/transparentImageWithExplanations.png").convert_alpha()
explanations = pygame.transform.scale(explanations, boardSz)
xPos = sz / 2 - sz / 2
yPos = sz / 2 - sz / 2
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


screen = pygame.display.set_mode(dispSz)


while s:
    screen.fill((170, 96, 0))
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

    infromationBox(screen, dispSz, currPlayer)

    pygame.display.flip()

    clock.tick(60)
pygame.quit()
