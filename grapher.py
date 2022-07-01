from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)






class Grapher(Tk):
    def __init__(self, func, interval=200, width=40, height=100, displaymessage = {}, save = False, bgcolour = 'black', textcolour = 'lightgreen'):
        '''
func: the function to get the data from, should return float
interval: delay between function calls (ms).
width: width of the graph
height: how many lines of the graph are shown
save: set this to true if you want to save the graph after it is run
bgcolour: the colour of the background
textcolour: the colour of the text'''

        super().__init__()
        
        #just setting it up
        self.geometry('1920x1080')
        self.title = 'Grapher'
        self.configure(bg='black')
        self.frame = ttk.Frame(self)
        self.frame.pack()
        
        self.l = [0 for i in range(height)]
        self.save = save
        self.displaymessage = displaymessage
        self.func, self.interval, self.width, self.height = func, interval, width, height
        #to save memory, dont save all the recorded data when not saving to file 
        if save:
            self.savebutton = ttk.Button(self.frame, text='save data', command=self.savetofile)
            self.saveData = []
            self.savebutton.grid(row=1)
            
        #text field for the grapher
        self.graphed = st.ScrolledText(self.frame, width=189, height=50)
        self.graphed.configure(bg='black', foreground=('lightgreen'), borderwidth=0)
        self.graphed.grid(row=0)
        self.graphed.insert(1.0,self.all_lines(self.l))
        self.graphed.see(END)
        
        self.colourIn = Entry(self.frame)
        self.graph()
        self.attributes('-fullscreen', True)
    
    #the grapher itself
    def graph(self): 
            
        x = self.func()
        if self.save:
            self.saveData.append(x)
        self.l.append(x)
        if len(self.l) > self.height:
            del self.l[0:len(self.l)-self.height-1]
        
        s = self.all_lines(self.l)
        
        self.graphed.replace(1.0, END, s)
        self.after(self.interval, self.graph)
    
    #save data to a file
    def savetofile(self):
        f = open('data.txt', 'w+', encoding='utf-8')
        s = self.all_lines(self.saveData)
        f.write(s)

    def start(self):
        '''
start the grapher'''
        self.mainloop()
    
    def all_lines(self, l):
        '''
this is the thing that generates all the text.

l: a list including the input date
width: width of the graph'''
        s = ''
        
        low = min(l)
        high = max(l)
        keys = self.displaymessage.keys()
        i = 0
        for elem in l:
            i += 1 
            if i in keys:
                message = self.displaymessage[i]
            else:
                message = ''
            s += self.line(elem, low, high, message)
        s = s[:-1]
        return s
    
    def line(self, data: float, low:float, high:float, label: str):
        '''
generates a single line for the graph

data: the length of the bar
low: lower bound of the bar
high: upper bound of the bar
label: the text to put directly after the bar. e '''
    
        try: length = int(self.width*(data-low)/(high-low))
        except ZeroDivisionError: length = self.width//2
        
        
        line =  '░'*length
        line += ' '*(5+self.width-len(line))
        line += str(data)
        line += ' '*(30+self.width-len(line))
        line += label
        line += '\n'
        return line

