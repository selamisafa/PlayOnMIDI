from copy import deepcopy
import random

walls = []

bird = [0, 1]

board = {'h': 8, 'l': 8}
currentBoard = []

currentSpeed = [1, 1]
gravity = 1
jumpSpeed = -2

isGameOver = False

def Move(direction):
    global isGameOver  
    if bird[1] >= board['h']:
        isGameOver = True
        print('Game Over')
        return

    currentSpeed[1] += gravity

    if direction == '1':
        currentSpeed[1] += jumpSpeed

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
            
    print("\033[H\033[J", end="")
    print(*currentBoard, sep = "\n")
    print(f"speed: {currentSpeed[1]}")

def CreateWall():
    #First element is X location of the wall
    #Second element is length of top wall
    #Third element is space between the walls
    #Using these we can render everyrhing about the walls.
    #Fill the board with wall after the space

    walls.append([board['l'], random.randint(1, 5), random.randint(1,3)])


def Update():
    global isGameOver
    if isGameOver:
        return

    if len(walls) <= 0:
        CreateWall()

    Move(input('Direction?'))
    Render()
    Update()

Render()
Update()