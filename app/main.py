import bottle
import json


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
    
    if(getSnakeHead()[0] < data["board"][0]):
        return json.dumps({
            'move': 'right',
            'taunt': 'ArGG!'
        })
    else:
        return json.dumps({
            'move': 'right',
            'taunt': 'ArGG!'
        })

def getSnakeIndex(snakes, name):
    len = snakes.length
    for x in range(0, len):
        if(snake[x].name == name):
            return x

def getSnakeHead():
    return data["snakes"][getSnakeIndex(data["snakes"], "Dan\'s Snake")][0]

@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
