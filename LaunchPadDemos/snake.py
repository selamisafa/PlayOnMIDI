from copy import deepcopy
from pygame import time
import random
import launchpad_py

#Launchpad S Setup
lp = launchpad_py.Launchpad()
lp.Open(0)
lp.Reset()

#Starting Snake
snake = [[3, 3], [4, 3]]

#Board Settings (Change according to your Midi size and preference)
board = {'h': 8, 'l': 8, 'Wrap Around': False}

#First direction that snake moves
lastDirection = 'right'

#Leave these alone pls
isGameOver = False
currentBoard = []
foods = []
lastButton = ""
speed = 400

#I might comment on the rest too but cant promise
def Move(direction):
    global lastDirection
    global isGameOver
    global speed

    if isGameOver:
        return

    length = len(snake)
    lastPos = deepcopy(snake[length - 1])

    if direction == 'right':
        if lastDirection == 'left':
            Move(lastDirection)
            return
        lastPos[0] += 1
        lastPos[0] %= 8
    elif direction == 'left':
        if lastDirection == 'right':
            Move(lastDirection)
            return
        lastPos[0] -= 1
        lastPos[0] %= 8
    elif direction == 'up':
        if lastDirection == 'down':
            Move(lastDirection)
            return
        lastPos[1] -= 1
        lastPos[1] %= 8    
    elif direction == 'down':
        if lastDirection == 'up':
            Move(lastDirection)
            return
        lastPos[1] += 1
        lastPos[1] %= 8
    else:
        Move(lastDirection)

    lastDirection = direction

    if not isGameOver:
        if CanMove(lastPos):
            snake.append(lastPos)
            if lastPos in foods:
                foods.remove(lastPos)
                speed -= 10
            else:
                print("test")
                snake.pop(0)
                
            Update()
        else:
            isGameOver = True
            print('Game Over')
            GameOverAnimation()
            return

def CanMove(next):
    if next in snake:
        if snake.index(next) == 0:
            return True

        print('Friendly Fire!')
        return False
    else:
        if board['Wrap Around']:
            return True
        else:
            if next[0] >= board['l'] or next[0] < 0:
                return False
            elif next[1] >= board['h'] or next[1] < 0:
                return False
            else:
                return True

def CreateFood():
    global currentBoard
    x = random.randint(0, board['h'] - 1)
    y = random.randint(0, board['l'] - 1)

    while currentBoard[x][y] == '#' or [y, x] in foods:
        x = random.randint(0, board['l'] - 1)
        y = random.randint(0, board['h'] - 1)

    foods.append([y, x])

def Render():
    global currentBoard
    currentBoard = [[]]

    if isGameOver:
        print("Game Over")
        GameOverAnimation()
        return

    for l in range(board['l']):
        currentBoard[0].append(' ')

    for h in range(board['h'] - 1):
        currentBoard.append(deepcopy(currentBoard[0]))

    #adding the fucking snake
    for segment in snake:
        currentBoard[segment[1]][segment[0]] = '#'

    for food in foods:
        currentBoard[food[1]][food[0]] = 'O'

    print("\033[H\033[J", end="")
    print(lastButton)
    print(*currentBoard, sep = "\n")

    RenderOnLaunchpad()

def RenderOnLaunchpad():
    for x in range(board['l']):
        for y in range(board['h']):
            if currentBoard[x][y] == '#':
                lp.LedCtrlXY(y, x+1, 0, 3)
            elif currentBoard[x][y] == 'O':
                lp.LedCtrlXY(y, x+1, 3, 3)
            else:
                lp.LedCtrlXY(y, x+1, 0, 0)

def ButtonChecker():
    global lastButton
    button = lp.ButtonStateXY()
    if len(button) > 0:
        button.pop()
        if [0,0] == button:
            lastButton = "up"
        elif [1,0] == button:
            lastButton = "down"
        elif [2,0] == button:
            lastButton = "left"
        elif [3,0] == button:
            lastButton = "right"
        else:
            lastButton = ""

        if lastButton != "":
            lp.ButtonFlush()

def Update():
    Render()
    if len(foods) <= 1:
        for i in range(1):
            CreateFood()
        Render()

    if not isGameOver:
        time.wait(speed)
        ButtonChecker()
        Move(lastButton)

def GameOverAnimation():
    for block in snake:
        lp.LedCtrlXY(block[0], block[1]+1, 3, 0)
        time.wait(150)

    for block in snake:
        lp.LedCtrlXY(block[0], block[1]+1, 0, 0)
        time.wait(150)
    
    for block in foods:
        lp.LedCtrlXY(block[0], block[1]+1, 0, 0)

    Text_Animation("GAME OVER!")
    
def Text_Animation(text):
    lp.LedCtrlString(text, 3,0, direction = -1, waitms = 100)


Update()