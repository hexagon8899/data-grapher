import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) ) #allow imports from outside file
from grapher import Grapher
import random


def randomnum(): #simulating a function that gets data
    value = random.random() #generate random value
    return value #return random value

g=Grapher(
    randomnum, #the function
    interval=50, #time between function calls
    precision=6, #precision for scientific notation
    displaymessage = { #displays a message to the right of the graph.
    60: 'this is a label', #on line 60, display 'this is a label'
    61: 'this is another label', #on line 61, display 'this is another label'
    69: 'this is on line 69! there has also been {amountgraphed} values graphed', #strings get formatted, so the {amountgraphed} will show as a number
    75: 'average: {sci(average, prec)}, total: {sci(total, prec)}' #scientific notation
    },
    textcolour='#6a9955') #sets the text to a green colour 

g.start() #start graphing