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
        'name': 'battlesnake-python',
        'color': '#000000',
        'head_url': 'http://battlesnake-python.herokuapp.com',
        'taunt': 'ArGG!'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json

    return json.dumps({
        'move': 'right',
        'taunt': 'ArGG!'
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
