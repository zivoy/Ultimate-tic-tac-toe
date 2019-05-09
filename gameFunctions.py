import pygame
from enum import Enum

Buttons = dict()
# dictionary that handles buttons


# miniclass that handles colors
class Color(Enum):
    X = [242, 32, 9]            # red
    O = [51, 214, 42]           # green
    HIGHLIGHT = [209, 232, 62]  # yellow
    WHITE = [255, 255, 255]
    GRAY = [150, 150, 150]
    BLUE = [38, 73, 160]


# class that handles small game boards
class board:
    def __init__(self, boardx, boardy, sizex, sizey, parts=3):
        self.boardx = boardx     # define the board x position
        self.boardy = boardy     # define the board y position
        self.sizex = sizex       # define the board width
        self.sizey = sizey       # define the board height
        self.parts = parts       # define the board number of boards (WIP)
        self.displayB = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)   # make board surface
        self.boardOver = getColor(Color.WHITE, 0)                   # sets default board overlay to transparent white
        self.Board = ticTacToeBoard(getColor(Color.WHITE, 0))       # makes an empty list to hold the board

    # function that changes the color over boards
    def bigBoard(self, col=None, alpha=180):
        if col is not None:
            self.boardOver = getColor(col, alpha)   # checks if a color was given if so set that as the overlay color
        else:
            return self.boardOver                   # else return the overlay color

    # function that changes the color of board tiles
    def boardSquares(self, x, y, col=None):
        if col is not None:
            self.Board[x][y] = getColor(col)        # checks if a color was given if so set that as the tile color
        else:
            return self.Board[x][y]                 # else return the tile color

    # function that draw the board
    def draw(self, screen):
        self.displayB.fill(getColor(Color.WHITE)[:4:])  # fill surface with white

        for x in range(self.parts):
            for y in range(self.parts):
                sqc = self.Board[x][y]                 # set the color
                sqx = x / self.parts * self.sizex      # set the x position
                sqy = y / self.parts * self.sizey      # set the y position

                fillColor(self.displayB, sqc, (self.sizex / self.parts, self.sizey / self.parts), (sqx, sqy))
                # fill tile with color

        fillColor(self.displayB, self.boardOver, (self.sizex, self.sizey))
        # fill board with overlay color

        drawGrid(self.displayB, 2, self.parts)
        # draw a grid

        screen.blit(self.displayB, (self.boardx, self.boardy))
        # put it on the surface

    # function that updates the board
    def update(self, screen):
        self.draw(screen)


# function that gets the color adds alpha and returns it in different format
def getColor(color, alpha=225):
    col = [*color.value, alpha, color.name]
    return col


# draw a grid
def drawGrid(display, thickness, amount=3):
    w, h = display.get_size()       # get width and height

    for i in range(amount + 1):
        posx = i / amount * w       # set up which part of the grid to draw using fractions
        posy = i / amount * h

        pygame.draw.line(display, (0, 0, 0), (0, posy), (h, posy), thickness)
        pygame.draw.line(display, (0, 0, 0), (posx, 0), (posx, h), thickness)
        # draw lines


# draw the whole game board
def drawGame(display, board):
    display.fill((0, 0, 0))         # fill display with black

    updateBoards(board, display)    # update the boards

    drawGrid(display, 3)            # draw a grid over everything


# make a list that makes an empty list and populates it with a item
def ticTacToeBoard(fillWith):
    gameB = list()                      # make list
    for i in range(3):
        gameB.append(list())            # add a list to the list
        for j in range(3):
            gameB[i].append(fillWith)   # put the color list in the list
    return gameB


# function that makes a list that handles the entire game board
def createBoard(wh):
    w, h = wh                           # separate width and height
    gboard = list()                     # make a list
    for i in range(3):
        gboard.append(list())           # add a list to the list
        for j in range(3):
            x = round(i / 3 * w + .5)   # calculate the x position
            y = round(j / 3 * h + .5)   # calculate the y position
            l = round(h / 3 + 1.2)      # calculate the height
            s = round(w / 3 + 1.2)      # calculate the width

            gboard[i].append(board(x, y, s, l))
            # make a board and add it to the list

    replaceWith(gboard, Color.WHITE, Color.HIGHLIGHT, 80)
    # highlight all boards
    return gboard


# dunction that updates all boards
def updateBoards(dataTable, display):
    [[j.update(display) for j in i] for i in dataTable]


# function that handles game logic
def handleGame(dataTable):
    masterBoard = list()    # make a list for the board
    for x, i in enumerate(dataTable):
        masterBoard.append(list())  # add a list to the list
        for j in i:
            vik = checkVictory(j.Board)  # check if board was won
            if vik:
                j.bigBoard(vik)      # if won change the color of the board to color of victor
            masterBoard[x].append(j.bigBoard())  # add the board overlay color to list
    vik = checkVictory(masterBoard)  # check if there's a winner in the entire board
    if vik:
        # print(getColor(vik)[4] + " Won")
        replaceWith(dataTable, Color.GRAY, Color.WHITE, 0)       # if there's a winner replace all the
        replaceWith(dataTable, Color.HIGHLIGHT, Color.WHITE, 0)  # highlight and gray with white
        return vik


# functions that calculates what board and tile was pressed
def clickHandler(mousePos, wh):
    bB = [0] * 2  # make empty lists
    sB = [0] * 2
    for i in range(2):  # iterate through the x and y pos of the mouse
        if mousePos[i] < 0 or mousePos[i] > wh[i]:
            return False  # if mouse outside of play area return false
        brd = mousePos[i] / wh[i] * 9   # split board up into 9 parts
        bB[i] = min(int(brd / 3), 2)    # divide by 3 to effectively split to 3 parts and find which board was clicked
        sB[i] = min(int(brd) % 3, 2)    # modulo of three to make it repeat to 0 when reached 3

    return bB, sB  # return board clicked and tile clicked


# functions that places a tile and handles colors
def placeTile(dataTable, clickTile, color, sound):
    completed = False    # variable for if the turn was completed
    game = clickTile[0]  # split board and tile clicks
    tile = clickTile[1]
    currBoard = dataTable[game[0]][game[1]]  # load board clicked

    if currBoard.bigBoard()[4] == Color.HIGHLIGHT.name:
        # check if the board that was clicked is highlighted
        if currBoard.boardSquares(tile[0], tile[1])[4] == Color.WHITE.name:
            # check if the tile that was clicked is white

            pygame.mixer.Sound.play(sound)        # play hit sound

            completed = True                      # turn was competed successfully

            currBoard.boardSquares(tile[0], tile[1], color)  # change the color of clicked tile

            replaceWith(dataTable, Color.HIGHLIGHT, Color.WHITE, 0)  # turn all highlighted bord tiles white
            replaceWith(dataTable, Color.GRAY, Color.WHITE, 0)       # turn all gray bord tiles white

            handleGame(dataTable)               # handle gam logic

            if dataTable[tile[0]][tile[1]].bigBoard()[4] != Color.WHITE.name:
                replaceWith(dataTable, Color.WHITE, Color.HIGHLIGHT, 80)
                # if the tile that was clicked is not white set all tiles to tiles to bo highlighted
            else:
                dataTable[tile[0]][tile[1]].bigBoard(Color.HIGHLIGHT, 80)  # else set the clicked tile to be highlighted
                replaceWith(dataTable, Color.WHITE, Color.GRAY, 60)        # and the rest to be gray

    return completed


# made to make flag variables easier
def flaging(variable, option1, option2):
    if variable == option1:
        return option2  # return option 2 if the variable is the same as option 1
    else:
        return option1  # else return option 1


# replaces all board colors with certain color
def replaceWith(dataTable, original, changed, alpha=180):
    for i in dataTable:  # iterate through table
        for j in i:
            if j.bigBoard()[4] == original.name:
                j.bigBoard(changed, alpha)  # if the color is the origin color replace it with the new color


# checks if board was won
def checkVictory(board):
    for i in [Color.X, Color.O]:  # iterate through player 1 and 2
        for x in range(3):  # iterate through all possible board combinations
            for y in range(3):
                if board[0][y][4] == board[1][y][4] == board[2][y][4] == getColor(i)[4]:  # vertical lines
                    return i
                if board[x][0][4] == board[x][1][4] == board[x][2][4] == getColor(i)[4]:  # horizontal lines
                    return i
        if board[0][0][4] == board[1][1][4] == board[2][2][4] == getColor(i)[4]:          # diagonal
            return i
        if board[0][2][4] == board[1][1][4] == board[2][0][4] == getColor(i)[4]:          # other diagonal
            return i
    return False


# makes the information panel
def infromationBox(screen, screenSz, curP):
    global Buttons  # access the button dictionary

    wBox = pygame.Rect(screenSz[0] * .73, screenSz[1] * .03, screenSz[0] * .26, screenSz[1] * .94)
    # box for panel
    reset = pygame.Rect(screenSz[0] * .75, screenSz[1] * .85, screenSz[0] * .22, screenSz[1] * .1)
    # box for reset button
    cBox = pygame.Rect(screenSz[0] * .75, screenSz[1] * .06, screenSz[1] * .1, screenSz[1] * .1)
    # box for current player square

    Buttons["reset"] = reset
    # add reset button to buttons dict for collision checking

    pygame.draw.rect(screen, Color.WHITE.value, wBox)
    pygame.draw.rect(screen, Color.BLUE.value, reset)
    pygame.draw.rect(screen, getColor(curP)[:4:], cBox)
    # draw on screen


# initialise all variables for start of game
def initBoard(sz, p=0):  # p decides who goes first by default its player 1
    gBoard = createBoard(sz)  # create the game board
    startP = Color.X if not p else Color.O  # set player
    startS = 2 if not p else 0  # set hitsound

    return gBoard, startP, startS


# fills entire area with color supports opacity
def fillColor(display, color, sz, pos=(0, 0)):
    s = pygame.Surface(sz, pygame.SRCALPHA)  # make a surface
    s.fill(color[:4:])          # fill it with color
    display.blit(s, pos)        # put it on display
