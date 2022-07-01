from grapher import Grapher
import random

def randomnum():
    value = random.random()
    return value

g=Grapher(
    randomnum,
    displaymessage = {
    60: 'this is a label',
    61: 'this is another label',
    65: '/-\\-----------------------------------------------/-\\',
    66: '|-|                                               |-|',
    67: '|-|   T H I S   I S   A   L A R G E   L A B E L   |-|',
    68: '|-|                                               |-|',
    69: '\\-/-----------------------------------------------\\-/',
    },
    textcolour='#ffffff')
g.start()