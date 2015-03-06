import bottle
import json
import math

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


def moveToFood(snakeHead, food):
    if(snakeHead[0] < food[0]):
        return json.dumps({
            'move': 'right',
            'taunt': 'Bollocks'
        })
    elif(snakeHead[0] > food[0]):
        return json.dumps({
            'move': 'left'
        })
    elif(snakeHead[1] < food[1]):
         return json.dumps({
            'move': 'down'
        })
    else:
         return json.dumps({
            'move': 'up'
        })
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
        'head_url': 'http://battlesnake-python.herokuapp.com',
        'taunt': 'ArGG!'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json

    return moveToFood(getSnakeHead(), getClosestFood(getSnakeHead(), data["food"]))
    
    print "x = " + str(getSnakeHead()[0])
    print "y = " + str(getSnakeHead()[1])
    print "board width = " + str(getBoarders(data['board'])['width'])
    print "board height = " + str(getBoarders(data['board'])['height'])
    #return json.dumps({
    #    'move': 'down',
    #    'taunt': data
    #})
    #else:
       # return json.dumps({
        #    'move': 'down',
         #   'taunt': 'ArGG!'
        #})



@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
