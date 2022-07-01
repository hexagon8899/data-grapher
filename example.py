from grapher import Grapher
import random

def randomnum():
    value = random.random()
    return value

g=Grapher(randomnum, hackermode=True)
g.start()