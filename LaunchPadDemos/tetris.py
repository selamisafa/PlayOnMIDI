from copy import deepcopy
from pygame import time
import random
import launchpad_py

#Launchpad S Setup
lp = launchpad_py.Launchpad()
lp.Open(0)
lp.Reset()

walls = []

blockPrefabs = [
    [[0,0],[1,0],[2,0],[3,0]],

    [[0,0],
     [0,1],[1,1],[2,1]],

    [            [2,0],
     [0,1],[1,1],[2,1]],

    [[0,0],[1,0],
     [0,1],[1,1]],

    [      [1,0],[2,0],
     [0,1],[1,1]],

    [      [1,0],
     [0,1],[1,1],[2,1]],
    
    [[0,0],[1,0],
           [1,1],[2,1]],
]

board = {'h': 8, 'l': 8}
currentBoard = []
oldBlocks = []
rowBlockCounts = []
currentBlock =[]
gravity = 1
horizontalSpeed = 0
isGameOver = False
lastButton = ""
gameSpeed = 1300

def Move(direction):
    global isGameOver
    
    if not isGameOver:
        if currentBlock == []:
            PickBlock()
    else:
        GameOverAnimation()
        return
    
    if direction == "left":
        horizontalSpeed = -1
    elif direction == "right":
        horizontalSpeed = 1
    else:
        horizontalSpeed = 0
        
    prediction = deepcopy(currentBlock)
    for block in prediction:
        block[0] += horizontalSpeed
        block[1] += gravity
    
    horizontal = CanMoveSideways(prediction)
    vertical = CanMoveDown(prediction)

    if horizontal and vertical:
        for block in currentBlock:
            block[0] += horizontalSpeed
            block[1] += gravity
    elif horizontal:
        for block in currentBlock:
            block[0] += horizontalSpeed
            SettleBlock()
            return
    elif vertical:
        for block in currentBlock:
            block[1] += gravity
    else:
        SettleBlock()
        return

def MoveOnlyHorizontal(direction):
    global isGameOver
    
    if not isGameOver:
        if currentBlock == []:
            PickBlock()
    else:
        GameOverAnimation()
        return
    
    if direction == "left":
        horizontalSpeed = -1
    elif direction == "right":
        horizontalSpeed = 1
    else:
        horizontalSpeed = 0
        
    prediction = deepcopy(currentBlock)
    for block in prediction:
        block[0] += horizontalSpeed
    
    horizontal = CanMoveSideways(prediction)

    if horizontal:
        for block in currentBlock:
            block[0] += horizontalSpeed

def SettleBlock():
    for block in currentBlock:
        oldBlocks.append(block)
        rowBlockCounts[block[1]] += 1

    CleanRows()
    PickBlock()

def CleanRows():
    #Dont have any idea for now
    global oldBlocks
    global rowBlockCounts

    newOldBlocks = []

    i = 0
    for row in rowBlockCounts:
        if row >= board["l"]:
            row = 0
            rowBlockCounts[i] = 0
            
            for block in oldBlocks:
                if block[1] != i:
                    if block[1] < i:
                        block[1] += 1
                    newOldBlocks.append(block)

            oldBlocks = newOldBlocks
            
        #animation?
        i += 1

    Render()

def PickBlock():
    global currentBlock
    global isGameOver

    currentBlock = deepcopy(blockPrefabs[random.randrange(len(blockPrefabs))])

    for block in currentBlock:
        block[0] += 2
        if block in oldBlocks:
            isGameOver = True
            GameOverAnimation()
            return 
    Render()

def CanMoveDown(prediction):
    for block in prediction:
        if block[1] >= board["h"]:
            return False
        elif block in oldBlocks:
            return False
    return True

def CanMoveSideways(prediction):
    for block in prediction:
        if block[0] >= board["l"]:
            return False
        elif block[0] < 0:
            return False
        elif block in oldBlocks:
            return False
    return True
    
def Render():
    global currentBoard

    currentBoard = [[]]
    for l in range(board['l']):
        currentBoard[0].append(' ')

    for h in range(board['h'] - 1):
        currentBoard.append(deepcopy(currentBoard[0]))

    #adding the fucking blocks
    for block in oldBlocks:
        currentBoard[block[1]][block[0]] = "#"

    for block in currentBlock:
        currentBoard[block[1]][block[0]] = "O"
            
    print("\033[H\033[J", end="")
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

def RotateBlock(block, clockwise):
    pivot = block[0]
    cx, cy = pivot

    rotated_block = []
    for x, y in block:
        if clockwise:
            new_x = cx - (y - cy)  
            new_y = cy + (x - cx)  
        else:  
            new_x = cx + (y - cy)
            new_y = cy - (x - cx)
        
        rotated_block.append([new_x, new_y])
    
    return rotated_block    

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
    else:
        lastButton = ""
    
    lp.ButtonFlush()

def Update():
    global isGameOver
    if isGameOver:
        GameOverAnimation()
        return
    else:
        splitCount = 9
        split = int(gameSpeed/splitCount)
        
        for timeBite in range(splitCount-1):
            time.wait(split)
            ButtonChecker()
            MoveOnlyHorizontal(lastButton)
            Render()

        time.wait(split)
        ButtonChecker()
        Move(lastButton)
        Render()

        Update()

def GameOverAnimation():
    for block in oldBlocks:
        lp.LedCtrlXY(block[0], block[1]+1, 3, 0)
        time.wait(50)
    
    Text_Animation("GAME OVER!")
    
def Text_Animation(text):
    lp.LedCtrlString(text, 3,0, direction = -1, waitms = 100)

for l in range(board['l']):
    rowBlockCounts.append(0)

PickBlock()
Render()
Update()