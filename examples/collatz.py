import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from grapher import Grapher

#lets do a real example, the lengths of the collatz iteration series between 1000000 and 1001000
x = 1000001
def collatz():
    global x
    if x <= 1001000:
        n = x
        x += 1
        length = 0
        while n > 1:
            length += 1
            if n%2 == 0: #if even
                n //= 2 #halve it
            else: #if odd
                n *= 3 #multiply by 3
                n += 1 #add 1
        return length
    return None #returning None means the graph does not update

def save(s): #save it to collatzdata.txt, inside the examples folder
    f = open(f'{path.dirname(path.abspath(__file__))}/collatzdata.txt', 'w', encoding='utf-8')
    f.write(s)

g=Grapher(
    collatz,
    width=100,
    height=1000, #setting height to 1000 so nothing is lost
    interval=1, #interval is low just so we dont need to wait
    displaymessage={
        975: 'average: {sci(average, prec)}',
        976: 'highest: {highest} ({highestindex+1000000})',
        977: 'amount left: {1000-amountgraphed}',
        978: 'runtime: {sci(runtime, prec)}s',
        979: 'time between function calls: {sci(dt, prec)}s'
    },
    savefunc=save, #makes the grapher call our save function when we press the save button
    gapchar=' ',
    linemessage='{sci(dt, prec)}s') 

g.start()