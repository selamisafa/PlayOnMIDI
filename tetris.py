from copy import deepcopy
import random

walls = []

blockPrefabs = [

    [[0,0],[1,0],
    [0,1],[1,1]],
    
    [[0,0],[1,0],[2,0],[3,0]],
    
    [       [1,0],
    [0,1],[1,1],[2,1]],
    
    [[0,0],
    [0,1],
    [0,2],
    [0,3],[1,3]],
    
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
    for blocks in prediction
        blocks[0] += horizontalSpeed
        blocks[1] += gravity
    
    sideways = CanMoveSideways(prediction)
    if CanMoveDown(prediction):
        for blocks in currentBlock
            blocks[1] += horizontalSpeed

def PickBlock():
    global currentBlock
    
    currentBlock = deepcopy(blockPrefabs[random.randrange(len(blockPrefabs))])

def CanMoveDown(prediction):
    for block in prediction:
        if block[1] >= board["h"]:
            return False
        elif block in oldBlocks:
            return False
    return True

def 
def CanMoveDown(prediction):
    for block in prediction:
        if block[1] >= board["h"]:
            return False
        elif block in oldBlocks:
            return False
    return True
    (prediction):
    for block in prediction:
        if block[0] >= board["l"]:
            return False
        elif block in oldBlocks:
            return False
    return True
    
def Render():
    global currentBoard
    global isGameOver

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

Render()
Update()