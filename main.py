from gameFunctions import *

pygame.init()

dispSz = [1000, 1000]

screen = pygame.display.set_mode(dispSz)
pygame.display.set_caption("Ultimate Tic Tac Toe")

gameBoard = createBoard(dispSz)

'''
gameBoard[1][0].bigBoard(Color.GREEN, 90)
gameBoard[1][2].bigBoard(Color.GREEN, 80)
gameBoard[2][2].bigBoard(Color.RED, 80)
gameBoard[2][1].bigBoard(Color.YELLOW, 188)

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
print(Color.RED.value)
print(getColor(Color.GREEN, 13))'''

highlightAvaiable(gameBoard)

gameBoard[2][1].bigBoard(Color.WHITE)

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mosPos = pygame.mouse.get_pos()
                clicked = clickHandler(mosPos, dispSz)
                turn = placeTile(gameBoard, clicked, currPlayer)
                if turn:
                    currPlayer = flaging(currPlayer, Color.X, Color.O)

    drawGame(screen, gameBoard)
    pygame.display.flip()

    clock.tick(60)
pygame.quit()
