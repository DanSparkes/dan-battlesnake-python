import bottle
import json
import math

def moveRight(taunt):
    return json.dumps({
        'move': 'right',
        'taunt': taunt
    })
def moveDown(taunt):
    return json.dumps({
        'move': 'down',
        'taunt': taunt
    })
def moveUp(taunt):
    return json.dumps({
        'move': 'up',
        'taunt': taunt
    })
def moveLeft(taunt):
    return json.dumps({
        'move': 'left',
        'taunt': taunt
    })

class FoodDistance:
   'Common base class food and it\s distance'

   def __init__(self, food, distance):
      self.food = food
      self.distance = distance

def getSnakeIndex(snakes, name):
    length = len(snakes)
    for x in range(0, length):
        if(snakes[x]['name'] == name):
            return x

def getSnakeHead():
    data = bottle.request.json
    return data["snakes"][getSnakeIndex(data["snakes"], "Dan\'s Snake")]['coords'][0]

def getBoarders(board):
    return {
        'width': len(board),
        'height': len(board[0])
    }

def getClosestFood(snakeHead, food):
    foodList = []
    for x in range(0, len(food)):
        distance = math.sqrt((snakeHead[0] - food[x][0])**2 + (snakeHead[1] - food[x][1])**2)
        fd = FoodDistance(food[x], distance)
        foodList.append(fd)
    foodList.sort(key=lambda x: x.distance, reverse=False)
    return foodList[0].food

def checkIfSafe(snakeHead, direction, board):   
    if(direction == 'right'):
        if(snakeHead[0] + 1 == getBoarders(board)['width']):
            return False
        state = board[snakeHead[0]+1][snakeHead[1]]['state']
        if(state == 'food' or state == 'empty'):
            if(snakeHead[0] + 2 < getBoarders(board)['width']):
                if(board[snakeHead[0]+2][snakeHead[1]]['state'] == 'head'):
                    return False
            if(snakeHead[0] + 1 < (getBoarders(board)['width']) and (snakeHead[1]+1 < (getBoarders(board)['height']))):
                if(board[snakeHead[0]+1][snakeHead[1] + 1]['state'] == 'head'):
                    return False
            if(snakeHead[0] + 1 < (getBoarders(board)['width'])):
                if(board[snakeHead[0]+1][snakeHead[1] - 1]['state'] == 'head'):
                    return False
                else:
                    return True
        else:
            return False
    if(direction == 'left'):
        state = board[snakeHead[0]-1][snakeHead[1]]['state']
        if(state == 'food' or state == 'empty'):
            if(snakeHead[1]+1 < (getBoarders(board)['height'])):
                if(board[snakeHead[0]-1][snakeHead[1] + 1]['state'] == 'head'):
                    return False
            if(board[snakeHead[0]-2][snakeHead[1]]['state'] == 'head' or board[snakeHead[0]-1][snakeHead[1] - 1]['state'] == 'head'):
                return False
            else:
                return True
        else:
            return False
    if(direction == 'up'):
        state = board[snakeHead[0]][snakeHead[1]-1]['state']
        if(state == 'food' or state == 'empty'):
            if(snakeHead[0] + 1 < getBoarders(board)['width']):
                if(board[snakeHead[0] + 1][snakeHead[1]-1]['state'] == 'head'):
                    return False
            if(board[snakeHead[0]][snakeHead[1]-2]['state'] == 'head' or board[snakeHead[0] - 1][snakeHead[1]-1]['state'] == 'head'):
                return False
            else:
                return True
        else:
            return False
    if(direction == 'down'):
        if(snakeHead[1] + 1 == getBoarders(board)['height']):
            return False
        state = board[snakeHead[0]][snakeHead[1]+1]['state']
        if(state == 'food' or state == 'empty'):
            if(snakeHead[1] + 2 < getBoarders(board)['height']):
                if(board[snakeHead[0]][snakeHead[1]+2]['state'] ==  'head'):
                    return False
            if(snakeHead[0] + 1 < (getBoarders(board)['width']) and (snakeHead[1]+1 < (getBoarders(board)['height']))):
                if(board[snakeHead[0] + 1][snakeHead[1]+1]['state'] == 'head'):
                    return False
            if(board[snakeHead[0] - 1][snakeHead[1]+1]['state'] == 'head'):
                return False
            else:
                return True
        else:
            return False

def nextBestMove(snakeHead, prevDirection, board):
    left = 0
    right = 0
    up = 0
    down = 0
    snakex = snakeHead[0]
    snakey = snakeHead[1]
    if(prevDirection != 'left'):
        while snakex >= 0:
            snakex -= 1
            if(board[snakex][snakey]['state'] == 'food' or board[snakex][snakey]['state'] == 'empty'):
                left += 1
            else:
                break
        snakex = snakeHead[0]
    if(prevDirection != 'right'):
        if(snakeHead[0] + 1 != getBoarders(board)['width']):
            while snakex < (getBoarders(board)['width'] - 1):
                snakex += 1
                if(board[snakex][snakey]['state'] == 'food' or board[snakex][snakey]['state'] == 'empty'):
                    right += 1
                else:
                    break
            snakex = snakeHead[0]
    if(prevDirection != 'up'):
        while snakey >= 0:
            snakey -= 1
            if(board[snakex][snakey]['state'] == 'food' or board[snakex][snakey]['state'] == 'empty'):
                up += 1
            else:
                break
        snakey = snakeHead[1]
    if(prevDirection != 'down'):
        if(snakeHead[1] + 1 != getBoarders(board)['height']):
            while snakey < (getBoarders(board)['height'] - 1):
                snakey += 1
                if(board[snakex][snakey]['state'] == 'food' or board[snakex][snakey]['state'] == 'empty'):
                    down += 1
                else:
                    break
    moveList = [left, right, up, down]
    moveList.sort()
    if(moveList[3] == up):
        if(checkIfSafe(snakeHead, 'up', board)):
            return moveUp('Get out the way')
        else:
            return nextBestMove(snakeHead, 'up', board)
    elif(moveList[3] == down):
        if(checkIfSafe(snakeHead, 'down', board)):
            return moveDown('Shift it!')
        else:
            return nextBestMove(snakeHead, 'down', board)
    elif(moveList[3] == right):
        if(checkIfSafe(snakeHead, 'right', board)):
            return moveRight('Move!!')
        else:
            return nextBestMove(snakeHead, 'right', board)
    elif(moveList[3] == left):
        if(checkIfSafe(snakeHead, 'left', board)):
            return moveLeft('You are in the way!')
        else:
            return nextBestMove(snakeHead, 'left', board)
    
    
def moveToFood(snakeHead, food, board):
    if(snakeHead[0] < food[0]):
        if(checkIfSafe(snakeHead, 'right', board)):
            return moveRight('So hungry')
        else:
            return nextBestMove(snakeHead, 'right', board) 
    elif(snakeHead[0] > food[0]):
        if(checkIfSafe(snakeHead, 'left', board)):
            return moveLeft('Must eat soon...')
        else:
            return nextBestMove(snakeHead, 'left', board)
    elif(snakeHead[1] < food[1]):
        if(checkIfSafe(snakeHead, 'down', board)):
            return moveDown('mmmm yellow balls')
        else:
            return nextBestMove(snakeHead, 'down', board)
    else:
        if(checkIfSafe(snakeHead, 'up', board)):
            return moveUp('On my way')
        else:
            return nextBestMove(snakeHead, 'up', board)

@bottle.get('/')
def index():
    return """
        <a href="https://github.com/sendwithus/battlesnake-python">
            battlesnake-python
        </a>
    """


@bottle.post('/start')
def start():
    data = bottle.request.json

    return json.dumps({
        'name': 'Dan\'s Snake',
        'color': '#000000',
        'head_url': 'http://www.spraypaintstencils.com/a-zlistings/bat-thumb.gif',
        'taunt': 'ArGG!'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json
    return moveToFood(getSnakeHead(), getClosestFood(getSnakeHead(), data["food"]), data["board"])
    



@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
