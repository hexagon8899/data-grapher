from tkinter import *
from tkinter import ttk
from os import path
import tkinter.scrolledtext as st
import timeit
from ctypes import windll

from numpy import average
windll.shcore.SetProcessDpiAwareness(1) #this lets the program know it is scaled up so it has less blurry text





class Grapher(Tk):
    def __init__(self, func, interval=200, width=40, height=100, displaymessage = {}, linemessage = '', precision = 4, savefunc = None, fullscreen = True, gapchar = ' ', bgcolour = 'black', textcolour = 'lightgreen'):
        '''
func: the function to get the data from, should return float
interval: delay between function calls (ms).
width: width of the graph
height: how many lines of the graph are shown
displaymessage: labels to the right of the graph
savefunc: what to do with the data when you press save. 
bgcolour: the colour of the background
textcolour: the colour of the text'''
        super().__init__()
        self.geometry('1920x1080') #set dimentions to the dimentions of the screen
        self.title('Grapher')
        self.iconbitmap('icon.ico')
        self.configure(bg=bgcolour)
        self.frame = ttk.Frame(self)
        self.frame.pack()
        self.l = [0 for i in range(height)] #default data is all zeros
        self.linemessage = linemessage
        self.linemesssages = ['' for i in range(height)]
        self.startingtime = 0
        self.precision = precision
        self.runtime = 0
        self.dt = 0
        self.gapchar, self.displaymessage, self.func, self.interval, self.width, self.height, self.savefunc = gapchar[0], displaymessage, func, interval, width, height, savefunc
        self.savebutton = ttk.Button(self.frame, text='save data', command=self.save)
        self.savebutton.grid(row=1)
        self.amountgraphed, self.average, self.total, self.highest, self.lowest, self.highestindex, self.lowestindex = 0, 0, 0, 0, 0, 0, 0
        self.graphed = st.ScrolledText(self.frame, width=189, height=50) #text field for the grapher
        self.graphed.configure(bg=bgcolour, foreground=(textcolour), borderwidth=0, wrap=NONE)
        self.graphed.grid(row=0)
        self.graphed.insert(1.0,self.all_lines(self.l))
        self.graphed.see(END) #scroll to bottom
        self.attributes('-fullscreen', fullscreen) #set to fullscreen
    
    def graph(self, data): #the grapher itself
        '''
data: data input, set to None if you do not want the data graphed this call'''
        if data != None:
            self.amountgraphed += 1
            self.total += data
            self.average = self.total/self.amountgraphed
            if data > self.highest:
                self.highest = data
                self.highestindex = self.amountgraphed
            if data < self.lowest:
                self.lowest = data
                self.lowestindex = self.amountgraphed
            self.l.append(data)
            if len(self.l) > self.height:
                del self.l[0:len(self.l)-self.height-1]
            
            s = self.all_lines(self.l)
            self.graphed.replace(1.0, END, s)
        self.after(self.interval, lambda: self.graph(self.func()))
    
    def save(self): #ran when we press save
        s = self.all_lines(self.l)
        if self.savefunc == None:
            open('data.txt', 'w+', encoding='utf-8').write(s)
        else:
            self.savefunc(s)

    def start(self): #call when you start
        '''
start the grapher'''
        self.startingtime = timeit.default_timer()
        self.graph(None) #start to graph
        self.mainloop()
    
    def all_lines(self, l): #returns the graph
        '''
this is the thing that generates all the text.

l: a list including the input date
width: width of the graph'''
        s = ''
        
        low = min(l)
        high = max(l)
        keys = self.displaymessage.keys()
        i = 0
        
        self.dt = timeit.default_timer()-self.runtime-self.startingtime
        self.runtime = timeit.default_timer()-self.startingtime
        linemessage = self.formatmessage(self.linemessage)
        self.linemesssages.append(linemessage)
        if len(self.linemesssages) > self.height:
            del self.linemesssages[0:len(self.linemesssages)-self.height-1]
        
        for elem in l:
            i += 1 
            if i in keys:
                message = self.displaymessage[i]
                message = self.formatmessage(message)
            else:
                message = ''
            s += self.line(elem, low, high, message, self.linemesssages[i-1])
        s = s[:-1]
        return s
    
    def line(self, data: float, low:float, high:float, label: str, linemessage: str): #returns a single line of the graph
        '''
generates a single line for the graph

data: the length of the bar
low: lower bound of the bar
high: upper bound of the bar
label: the text to put directly after the bar. e '''
    
        try: length = int(self.width*(data-low)/(high-low))
        except ZeroDivisionError: length = self.width//2
        
        gapchar = self.gapchar
        line = f'{data:.{self.precision}e}' #the numbers
        line += gapchar*(6-len(line))
        line += ' | '
        line += '░'*length #the bar
        line += gapchar*(9+self.precision+self.width-len(line)) #the gap between the graph and the labels
        line += ' | '
        line += label #the label
        line += gapchar*(188-len(line)-len(linemessage))
        line += linemessage
        line += '\n' #newline
        return line
    
    def sci(self, n, prec):
        return f'{n:.{prec}e}'
    
    def formatmessage(self, s):
        return eval(f"f'{s}'", {
                'highest': self.highest,
                'highestindex': self.highestindex,
                'lowest': self.lowest,
                'lowestindex': self.lowestindex,
                'range': self.highest-self.lowest,
                'total': self.total,
                'average': self.average,
                'runtime': self.runtime,
                'amountgraphed': self.amountgraphed,
                'dt': self.dt,
                'prec': self.precision,
                'sci': self.sci})

