from copy import deepcopy
import random

snake = [[3, 3], [4, 3], [4, 4], [4, 5]]
foods = []
board = {'h': 8, 'l': 8, 'Wrap Around': False}
currentBoard = []
lastDirection = 'right'
isGameOver = False

def Move(direction):
    global lastDirection
    global isGameOver

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
    if CanMove(lastPos):
        snake.append(lastPos)
        if lastPos in foods:
            foods.remove(lastPos)
        else:
            snake.pop(0)
            
        Update()
    else:
        isGameOver = True
        print('Game Over')
        return


def CanMove(next):
    if next in snake:
        if snake.index(next) == 0:
            return True
        
        snake.clear()
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
    for l in range(board['l']):
        currentBoard[0].append(' ')

    for h in range(board['h'] - 1):
        currentBoard.append(deepcopy(currentBoard[0]))

    #adding the fucking snake
    for i in snake:
        currentBoard[i[1]][i[0]] = '#'

    for i in foods:
        currentBoard[i[1]][i[0]] = 'O'

    print("\033[H\033[J", end="")
    print(*currentBoard, sep = "\n")

def Update():
    Render()
    if len(foods) <= 0:
        for i in range(2):
            CreateFood()
        Render()

    if not isGameOver:
        Move(input('Direction?'))

Update()