from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st
from ttkthemes import ThemedStyle

class Grapher(Tk):
    def __init__(self, func, interval=200, width=40, height=100, save = False):
        '''
func: the function to get the data from
interval: delay between function calls (ms).
width: width of the graph
height: how many lines of the graph are shown
save: set this to true if you want to save the graph after it is run'''
        super().__init__()
        #just setting it up
        self.style = ThemedStyle(self) 
        self.geometry('1920x1080')
        self.style.theme_use('black')
        self.title = 'Grapher'
        self.frame = ttk.Frame(self)
        self.frame.pack()
        
        self.l = [[0, 'unrecorded'] for i in range(height)]
        self.save = save
        self.func, self.interval, self.width, self.height = func, interval, width, height
        #to save memory, dont save all the recorded data when not saving to file 
        if save:
            self.savebutton = ttk.Button(self.frame, text='save', command=self.savetofile)
            self.savedata = []
            self.savebutton.grid(row=1)
        #text field for the grapher
        self.graphed = st.ScrolledText(self.frame, width=189, height=50)
        self.graphed.grid(row=0)
        self.graphed.insert(1.0,'s')
        self.graph()
        self.attributes('-fullscreen', True)
        self.mainloop()
    
    #the grapher itself
    def graph(self): 
        l = self.l
            
        x = self.func()
        if self.save:
            self.savedata.append(x)
        l.append(x)
        if len(l) > self.height:
            del l[0:len(l)-self.height-1]
        s = ''
        if type(l[0]) != list:
            l = [[i, str(i)] for i in l]
        
        data = [i[0] for i in l]
        low = min(data)
        high = max(data)
        i = 0
        for elem in l:
            i += 1
            
            try: length = int(self.width*(elem[0]-low)/(high-low))
            except ZeroDivisionError: length = self.width//2
            
            line =  '█'*length
            line += ' '*(5+self.width-len(line))
            line += elem[1]
            line += ' '*(30+self.width-len(line))
            line += 'a'
            line += '\n'
            s += line
        s = s[:-1]
        
        self.graphed.replace(1.0, END, s)
        self.l = l
        self.after(self.interval, self.graph)
    
    #save data to a file
    def savetofile(self):
        f = open('data.txt', 'w+', encoding='utf-8')
        s = ''
        data = [i[0] for i in self.savedata]
        low = min(data)
        high = max(data)
        i = 0
        for elem in self.savedata:
            i += 1
            
            try: length = int(self.width*(elem[0]-low)/(high-low))
            except ZeroDivisionError: length = self.width
            
            
            line =  '█'*length
            line += ' '*(5+self.width-len(line))
            line += elem[1]
            line += ' '*(30+self.width-len(line))
            line += 'a'
            line += '\n'
            
            s += line
        f.write(s)


