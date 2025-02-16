from copy import deepcopy
from pygame import time
import random
import launchpad_py

#Launchpad S Setup
lp = launchpad_py.Launchpad()
lp.Open(0)
lp.Reset()

board = {'length': 8, 'height': 8}
blockColors = [[3,0], [0,3], [1,1], [3,3]]
currentBoard = []
allBlocks = []
currentBlockColor = [0,0]
gravity = 1

isGameOver = False

def GenerateAllBoard():
    global allBlocks
    
    for l in range(board['length']):
        allBlocks.append([])

        for h in range(board['height']):
            allBlocks[l].append(deepcopy(blockColors[random.randrange(len(blockColors))]))
 
def MoveDown(pickedBlockX):
    global allBlocks
    
    foundEmpty = False
    foundSomethingToMove = False

    y = board['height'] - 1
    while y >= 0:
        if foundEmpty:
            allBlocks[pickedBlockX][y+1] = deepcopy(allBlocks[pickedBlockX][y])
            foundSomethingToMove = True
            if y == 0:
                allBlocks[pickedBlockX][y] = [0,0]
        elif allBlocks[pickedBlockX][y] == [0,0]:
            foundEmpty = True

        y -= 1
    
    allBlocks[pickedBlockX][0] = deepcopy(blockColors[random.randrange(len(blockColors))])
    Render()

    if foundEmpty and foundSomethingToMove:
        MoveDown(pickedBlockX)

    
def TryBlast(pickedBlockCoordinates):
    global allBlocks
    theChunk = []
    theChunk = CollectConnectedSame(pickedBlockCoordinates, theChunk)
    
    uniqueColumns = []

    if len(theChunk) > 3:
        for block in theChunk:
            allBlocks[block[0]][block[1]] = [0,0]

            if block[0] not in uniqueColumns:
                uniqueColumns.append(block[0])

    for column in uniqueColumns:
        MoveDown(column)
    
def CollectConnectedSame(pickedBlockCoordinates, theChunk):
    global allBlocks

    x = pickedBlockCoordinates[0]
    y = pickedBlockCoordinates[1]

    pickedBlock = allBlocks[x][y]
    theChunk.append(pickedBlockCoordinates)

    #Up
    if y - 1 >= 0:
        if pickedBlock == allBlocks[x][y - 1] and [x, y - 1] not in theChunk:
            theChunk += CollectConnectedSame([x, y - 1], theChunk)

    #Down
    if y + 1 < board['height']:
        if pickedBlock == allBlocks[x][y + 1] and [x, y + 1] not in theChunk:
            theChunk += CollectConnectedSame([x, y + 1], theChunk)

    #Left
    if x - 1 >= 0:
        if pickedBlock == allBlocks[x - 1][y] and [x - 1, y] not in theChunk:
            theChunk += CollectConnectedSame([x - 1, y], theChunk)

    #Right
    if x + 1 < board['length']:
        if pickedBlock == allBlocks[x + 1][y] and [x + 1, y] not in theChunk:
            theChunk += CollectConnectedSame([x + 1, y], theChunk)

    return theChunk

def Render():
    global currentBoard
    global isGameOver
    global allBlocks
    
    currentBoard = []
    emptyList = []
    
    for h in range(board['height']):
        emptyList.append(' ')

    for l in range(board['length']):
        currentBoard.append(deepcopy(emptyList))        

    #adding the fucking blocks
    x = 0
    for column in allBlocks:
        y = 0
        for block in column:
            if allBlocks[x][y] == [3,0]:
                currentBoard[x][y] = "#"
            elif allBlocks[x][y] == [0,3]:
                currentBoard[x][y] = "O"
            elif allBlocks[x][y] == [1,1]:
                currentBoard[x][y] = "X"
            elif allBlocks[x][y] == [3,3]:
                currentBoard[x][y] = "$"
            else:
                currentBoard[x][y] = " "
                
            y+=1
        x+=1
            
    """print("\033[H\033[J", end="")
    print(*currentBoard, sep = "\n")"""
    
    RenderOnLaunchpad()

def RenderOnLaunchpad():
    global allBlocks
    for x in range(board['length']):
        for y in range(board['height']):
            currentBlock = allBlocks[x][y]
            lp.LedCtrlXY(x, y+1, currentBlock[0], currentBlock[1])                

def ButtonChecker():
    global lastButton
    button = deepcopy(lp.ButtonStateXY())
    lp.ButtonFlush()
    
    if len(button) > 0:
        if button[2] == False:
            TryBlast([button[0], button[1] - 1])
            print(button)

def Update():
    global isGameOver

    if isGameOver:
        return

    ButtonChecker()
    Render()
    Update()

GenerateAllBoard()
Render()
Update()