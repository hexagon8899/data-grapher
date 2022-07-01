from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

def line(length, width, label):
    line =  '░'*length
    line += ' '*(5+width-len(line))
    line += label
    line += ' '*(30+width-len(line))
    line += 'a'
    line += '\n'
    return line

def all_lines(l, width):
    s = ''
    l = [i if type(i) == list else [i, str(i)] for i in l]
    
    data = [i[0] for i in l]
    low = min(data)
    high = max(data)
    i = 0
    for elem in l:
        i += 1
        
        try: length = int(width*(elem[0]-low)/(high-low))
        except ZeroDivisionError: length = width//2
        
        s += line(length, width, elem[1])
    s = s[:-1]
    return s

class Grapher(Tk):
    def __init__(self, func, interval=200, width=40, height=100, save = False, hackermode = False):
        '''
func: the function to get the data from
interval: delay between function calls (ms).
width: width of the graph
height: how many lines of the graph are shown
save: set this to true if you want to save the graph after it is run
hackermode: makes you look like a movie hacker'''

        super().__init__()
        
        #just setting it up
        self.geometry('1920x1080')
        self.title = 'Grapher'
        self.configure(bg='black')
        self.frame = ttk.Frame(self)
        self.frame.pack()
        
        self.l = [[0, 'unrecorded'] for i in range(height)]
        self.save = save
        self.func, self.interval, self.width, self.height = func, interval, width, height
        #to save memory, dont save all the recorded data when not saving to file 
        if save:
            self.savebutton = ttk.Button(self.frame, text='save', command=self.savetofile)
            self.saveData = []
            self.savebutton.grid(row=1)
        #text field for the grapher
        self.graphed = st.ScrolledText(self.frame, width=189, height=50)
        self.graphed.configure(bg='black', foreground=('lightgreen' if hackermode else 'white'))
        self.graphed.grid(row=0)
        self.graphed.insert(1.0,all_lines(self.l, self.width))
        self.graphed.see(END)
        self.graph()
        self.attributes('-fullscreen', True)
    
    #the grapher itself
    def graph(self): 
        l = self.l
            
        x = self.func()
        if self.save:
            self.saveData.append(x)
        l.append(x)
        if len(l) > self.height:
            del l[0:len(l)-self.height-1]
        
        s = all_lines(l, self.width)
        
        self.graphed.replace(1.0, END, s)
        self.l = l
        self.after(self.interval, self.graph)
    
    #save data to a file
    def savetofile(self):
        f = open('data.txt', 'w+', encoding='utf-8')
        s = all_lines(self.saveData, self.width)
        f.write(s)

    def start(self):
        self.mainloop()

