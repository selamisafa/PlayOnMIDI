from copy import deepcopy
import random

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
     [0,1],[1,1]]

    [      [1,0],
     [0,1],[1,1],[2,1]],
    
    [[0,0],[1,0],
           [1,1],[2,1]],
]

board = {'h': 8, 'l': 8}
currentBoard = []
oldBlocks = []
currentBlock =[]
gravity = 1
horizontalSpeed = 0
isGameOver = False

def Move(direction):
    global isGameOver
    
    if not isGameOver:
        if currentBlock == []:
            PickBlock()
    
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

def SettleBlock():
    for block in currentBlock:
        oldBlocks.append(block)

    CleanRows()
    PickBlock()

def CleanRows():
    #Dont have any idea for now
    Render()

def RotateBlocks():
    #Dont have any idea for now
    print("Ratet")

def PickBlock():
    global currentBlock
    global isGameOver

    currentBlock = deepcopy(blockPrefabs[random.randrange(len(blockPrefabs))])

    for block in currentBlock:
        block[0] += 2
        if block in oldBlocks:
            isGameOver = True
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
    
def Update():
    global isGameOver
    if isGameOver:
        return

    Move(input('Direction?'))
    Render()
    Update()

PickBlock()
Render()
Update()