from copy import deepcopy
from pygame import time
import random
import launchpad_py

#Launchpad S Setup
lp = launchpad_py.Launchpad()
lp.Open(0)
lp.Reset()

walls = []

bird = [0, 1]

board = {'h': 8, 'l': 8}
currentBoard = []

currentSpeed = [1, 1]
gravity = 1
jumpSpeed = -2
gameSpeed = 400

isGameOver = False

def Move(direction):
    global isGameOver  
    if bird[1] >= board['h']:
        isGameOver = True
        print('Game Over')
        GameOverAnimation()
        return

    currentSpeed[1] += gravity

    if direction != '':
        currentSpeed[1] += jumpSpeed

    #Balance
    if currentSpeed[1] > 1:
        currentSpeed[1] = 1
    
    if currentSpeed[1] < -1:
        currentSpeed[1] = -1

    bird[1] += currentSpeed[1]

    if bird[1] < 0:
        bird[1] = 0

    for wall in walls:
        wall[0] -= currentSpeed[0]
        if wall[0] < 0:
            walls.remove(wall)
        
def Render():
    global currentBoard
    global isGameOver

    currentBoard = [[]]
    for l in range(board['l']):
        currentBoard[0].append(' ')

    for h in range(board['h'] - 1):
        currentBoard.append(deepcopy(currentBoard[0]))

    #adding the fucking bird
    if len(currentBoard) > bird[1]:
        currentBoard[bird[1]][bird[0]] = 'O'
    else:
        isGameOver = True
        GameOverAnimation()

    for wall in walls:
        x = wall[0]
        currentIndex = 0
        for p in range(wall[1]):
            currentBoard[currentIndex][x] = '#'
            currentIndex += 1
        
        currentIndex += wall[2]

        for p in range(currentIndex, board['h']):
            currentBoard[p][x] = '#'    
        
    if bird[1] < board['h']:        
        if currentBoard[bird[1]][bird[0]] == "#":
            isGameOver = True
            print('Game Over')
            GameOverAnimation()
            
    print("\033[H\033[J", end="")
    print(*currentBoard, sep = "\n")
    print(f"speed: {currentSpeed[1]}")

    RenderOnLauncpad()

def RenderOnLauncpad():
    for x in range(board['l']):
        for y in range(board['h']):
            if currentBoard[x][y] == '#':
                lp.LedCtrlXY(y, x+1, 3, 0)
            elif currentBoard[x][y] == 'O':
                lp.LedCtrlXY(y, x+1, 0, 3)
            else:
                lp.LedCtrlXY(y, x+1, 0, 0)

def CreateWall():
    #First element is X location of the wall
    #Second element is length of top wall
    #Third element is space between the walls
    #Using these we can render everyrhing about the walls.
    #Fill the board with wall after the space

    walls.append([board['l'], random.randint(1, 4), random.randint(2,4)])

def ButtonChecker():
    global lastButton
    button = lp.ButtonStateXY()
    if len(button) > 0:
        lastButton = "up"
    else:
        lastButton = ""
    
    lp.ButtonFlush()


def Update():
    global isGameOver
    if isGameOver:
        return

    if len(walls) <= 0:
        CreateWall()

    time.wait(gameSpeed)
    ButtonChecker()
    Move(lastButton)
    
    Render()
    Update()

def GameOverAnimation():
    lp.LedCtrlXY(0, bird[1]+1, 1, 3)
    time.wait(300)
    lp.LedCtrlXY(0, bird[1]+1, 2, 2)
    time.wait(300)
    lp.LedCtrlXY(0, bird[1]+1, 3, 0)
    time.wait(300)

    Text_Animation("GAME OVER!")
    
def Text_Animation(text):
    lp.LedCtrlString(text, 3,0, direction = -1, waitms = 100)

Render()
Update()