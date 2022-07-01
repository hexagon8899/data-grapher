from grapher import Grapher
import random

def randomnum():
    value = random.random()
    return value

g=Grapher(
    randomnum,
    hackermode=True,
    save=True,
    displaymessage = {
    60: 'this is a label',
    61: 'this is another label'
    })
g.start()