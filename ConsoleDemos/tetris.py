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
        rowBlockCounts[block[1]] += 1

    CleanRows()
    PickBlock()

def CleanRows():
    #Dont have any idea for now
    global oldBlocks
    global rowBlockCounts

    i = 0
    for row in rowBlockCounts:
        if row >= board["l"]:
            row = 0
            
            newOldBlocks = []
            for block in oldBlocks:
                if block[1] != i:
                    if block[1] < i:
                        block[1] += 1
                    newOldBlocks.append(block)

            oldBlocks = newOldBlocks
            
        #animation?
        i += 1

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
    print(*RotateBlock(currentBlock, True))

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
    
def Update():
    global isGameOver
    if isGameOver:
        return

    Move(input('Direction?'))
    Render()
    Update()


for l in range(board['l']):
    rowBlockCounts.append(0)

PickBlock()
Render()
Update()