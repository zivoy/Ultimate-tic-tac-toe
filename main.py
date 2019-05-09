from gameFunctions import *
# import all the functions we will be using

pygame.init()
pygame.mixer.init(22050, 16, 2, 1024)
# initialise pygame and the sound module

sz = 800
# set the board size

boardSz = [sz, sz]
dispSz = [round(sz * 1.4), round(sz * 1.02)]
gameAt = [round(sz * .01), round(sz * .01)]
# calculate the screen size and offset for the board from the board size

screen = pygame.display.set_mode(boardSz)
pygame.display.set_caption("Ultimate Tic Tac Toe")
# make the screen and set the title

gameScreen = pygame.Surface(boardSz)
gameBoard, currPlayer, playerSound = initBoard(boardSz)
# make the game board and set starting player

hitSounds = list()
for i in range(1, 4):
    sound = pygame.mixer.Sound("sounds/hit{0}.wav".format(i))
    hitSounds.append(sound)
# load hit sounds

pygame.mixer.music.load('sounds/elevator.wav')
# load music

s = True
startMenu = True
clock = pygame.time.Clock()
# start clock and game loop variables

explanations = pygame.image.load("images/Instructions.png").convert_alpha()
scl = sz / max(explanations.get_rect().size)
explanations = pygame.transform.rotozoom(explanations, 0, scl)
xPos = sz / 2 - sz / 2
yPos = sz / 2 - sz / 2
# load the instructions and calculate the position
while startMenu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s = False
            startMenu = False
        # close window if closed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                startMenu = False
                pygame.mixer.Sound.play(hitSounds[1])
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                startMenu = False
                pygame.mixer.Sound.play(hitSounds[1])
        # start the game if space escape or left click were clicked
    screen.fill((255, 255, 255))
    # fill screen with white

    screen.blit(explanations, (xPos, yPos))
    # put the image on the screen

    pygame.display.flip()
    # update screen

screen = pygame.display.set_mode(dispSz)
playing = True
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.2)
# change screen size and start music

while s:
    screen.fill((170, 96, 0))
    # fill screen with this color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s = False
        # close if closed

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                turn = False
                mosPos = list(pygame.mouse.get_pos())
                # get mouse pos

                if Buttons['reset'].collidepoint(mosPos):
                    gameBoard, currPlayer, playerSound = initBoard(boardSz)
                    playing = True
                    pygame.mixer.Sound.play(hitSounds[1])
                # if reset button was pressed reset

                if playing:
                    for i in range(2):
                        mosPos[i] -= gameAt[i]
                    # offset the mouse pos with the board offset
                    clicked = clickHandler(mosPos, boardSz)
                    # get on what board and square the mouse pressed
                    if clicked:
                        turn = placeTile(gameBoard, clicked, currPlayer, hitSounds[playerSound])
                    # place tile on clicked spot
                    if turn:
                        currPlayer = flaging(currPlayer, Color.X, Color.O)
                        playerSound = flaging(playerSound, 0, 2)
                    # if turn was fulfilled switch player

    drawGame(gameScreen, gameBoard)
    # draw game board

    win = handleGame(gameBoard)
    if win:
        playing = False
        fillColor(gameScreen, getColor(win, 128), boardSz)
    # check if game was won if so stop the player and highlight board

    screen.blit(gameScreen, gameAt)
    # put the game on the screen

    infromationBox(screen, dispSz, currPlayer)
    # put the info box on screen

    pygame.display.flip()
    # update screen

    clock.tick(60)
    # keep fps

pygame.mixer.quit()
pygame.quit()
# quit sound module and pygame
