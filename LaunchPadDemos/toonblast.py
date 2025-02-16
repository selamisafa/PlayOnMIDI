from copy import deepcopy
from pygame import time
import random
import launchpad_py

#Launchpad S Setup
lp = launchpad_py.Launchpad()
lp.Open(0)
lp.Reset()

board = {'h': 8, 'l': 8}
blockColors = [[3,0], [0,3], [1,1], [3,3]]
currentBoard = []
allBlocks = []
currentBlockColor = [0,0]
gravity = 1

pickedX = -1
pickedY = -1

isGameOver = False

def GenerateAllBoard():
    global allblocks

    for h in range(board['h']):
        allBlocks.append([])
        for l in range(board['l']):
            allBlocks[h].append(deepcopy(blockColors[random.randrange(len(blockColors))]))
 
def MoveDown(pickedBlockCoordinates):
    global allBlocks
    
    x = pickedBlockCoordinates[0]
    foundEmpty = False
    foundSomethingToMove = False

    i = board['h'] - 1
    while i >= 0:
        if foundEmpty:
            allBlocks[i+1][x] = deepcopy(allBlocks[i][x])
            foundSomethingToMove = True
            if i == 0:
                allBlocks[i][x] = [0,0]
        elif allBlocks[i][x] == [0,0]:
            foundEmpty = True

        i -= 1
    
    allBlocks[0][x] = deepcopy(blockColors[random.randrange(len(blockColors))])

    if foundEmpty and foundSomethingToMove:
        MoveDown(pickedBlockCoordinates)

    
def TryBlast(pickedBlockCoordinates):
    global allBlocks

    allBlocks[pickedBlockCoordinates[1]][pickedBlockCoordinates[0]] = [0,0]
    MoveDown(pickedBlockCoordinates)
    print(pickedBlockCoordinates)
    print(allBlocks[pickedBlockCoordinates[1]][pickedBlockCoordinates[0]])
    print(currentBoard[pickedBlockCoordinates[1]][pickedBlockCoordinates[0]])
    
def CollectConnectedSame(pickedBlockCoordinates):
    x = pickedBlockCoordinates[0]
    y = pickedBlockCoordinates[1]
    
    pickedBlock = allBlocks[y][x]
    
    #Up
    

def CanMoveDown(prediction):
    for block in prediction:
        if block[1] >= board["h"]:
            return False
    return True
    
def Render():
    global currentBoard
    global isGameOver
    global allBlocks
    
    currentBoard = [[]]
    for l in range(board['l']):
        currentBoard[0].append(' ')

    for h in range(board['h'] - 1):
        currentBoard.append(deepcopy(currentBoard[0]))

    #adding the fucking blocks
    y = 0
    for row in allBlocks:
        x = 0
        for column in row:
            if allBlocks[y][x] == [3,0]:
                currentBoard[y][x] = "#"
            elif allBlocks[y][x] == [0,3]:
                currentBoard[y][x] = "O"
            elif allBlocks[y][x] == [1,1]:
                currentBoard[y][x] = "X"
            elif allBlocks[y][x] == [3,3]:
                currentBoard[y][x] = "$"
            else:
                currentBoard[y][x] = " "
                
            x+=1
        y+=1
            
    #print("\033[H\033[J", end="")
    print(*currentBoard, sep = "\n")
    
    RenderOnLaunchpad()

def RenderOnLaunchpad():
    global allBlocks
    for x in range(board['l']):
        for y in range(board['h']):
            currentBlock = allBlocks[y][x]
            lp.LedCtrlXY(y, x+1, currentBlock[0], currentBlock[1])                

def ButtonChecker():
    global lastButton
    button = lp.ButtonStateXY()
    if len(button) > 0:
        if button[2] == False:
            TryBlast([button[1] - 1, button[0]])
        
    lp.ButtonFlush()

def Update():
    global isGameOver
    global pickedX
    global pickedY
    if isGameOver:
        return

    ButtonChecker()
    Render()
    Update()

GenerateAllBoard()
Render()
Update()