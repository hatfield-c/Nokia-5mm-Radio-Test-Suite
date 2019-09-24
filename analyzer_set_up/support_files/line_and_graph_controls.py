# NOTE: to use the graph class, initialize the graph class from the top level program
# and pass the graph object to calling functions or modules. It
# does strange things otherwise

import tkinter as tk
from tkinter import messagebox
import time
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Graph():
    def __init__(self,parent_window,size=(6,3),grid_row=3):
        self.fig = plt.figure(figsize=(6, 3))
        plt.ion()
        self.titles = []
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig,parent_window)
        self.canvas.get_tk_widget().grid(column=0,row=3)
        self.parent_window=parent_window
        

    def A_line(self,title,line):
        
        min_x,min_y = line.get_min()
        max_x,max_y = line.get_max()
        params = line.plot_data()
        if title not in self.titles:
            self.titles.append(title)
        leg = plt.legend(loc='best',
                 labels=self.titles,
                 ncol=1,
                 shadow=True,
                 fancybox=True)

        self.ax.set_ylim(min_y-2,max_y+2)
        
        self.ax.plot(params[0],params[1],color=params[3],label=title)
        self.fig.canvas.draw_idle()
        self.fig.canvas.draw()
        return self.fig
        
    def A_point(self,title,x,y,Color='r'):
        if title not in self.titles:
            self.titles.append(title)
        leg = plt.legend(loc='best',
                 labels=self.titles,
                 ncol=1,
                 shadow=True,
                 fancybox=True)

        self.ax.plot(x,y,marker='o',color=Color)
        self.fig.canvas.draw_idle()
        self.fig.canvas.draw()
        return self.fig
       
    def __enter__(self):
        return self

    # ...

    def __exit__(self, exc_type, exc_value, traceback):
        pass
        


class Line():
    
    def __init__(self):
        
        self.color = 'r'
        self.width = 1
        self.xvals = []
        self.yvals = []
        self.line = (self.xvals,self.yvals,self.width,self.color)

    def set_color(self,color):
        self.color=color

    def append(self,x,y):
        self.xvals.append(x)
        self.yvals.append(y)

    def plot_data(self):return (self.xvals,self.yvals,self.width,self.color)

    def xy_data(self):return (self.xvals,self.yvals)

    def get_max(self):
        highest_val = max(self.yvals)
        highest_x = self.xvals[self.yvals.index(highest_val)]
        return highest_x,highest_val

    def find_bw(self,dB=3):
        x,y = self.get_max()
        yindex = self.yvals.index(y)
        edge = y-dB
        for i,val in enumerate (self.yvals[yindex::-1]):
            if val<edge:break
        loEdge = yindex-i
        for i,val in enumerate (self.yvals[yindex:]):
            if val<edge:break
        hiEdge = yindex+i
        xlo=float(((self.xvals[loEdge+1]-self.xvals[loEdge])
                   /(self.yvals[loEdge+1]-self.yvals[loEdge]))
                  *(edge-self.yvals[loEdge])
                  +self.xvals[loEdge])
        
        xhi=float(((self.xvals[hiEdge]-self.xvals[hiEdge-1])
                   /(self.yvals[hiEdge]-self.yvals[hiEdge-1]))
                  *(edge-self.yvals[hiEdge-1])
                  +self.xvals[hiEdge-1])
        return xhi-xlo

        
        
        

    def get_min(self):
        lowest_val = 999
        lowest_x = -360
        for i,val in enumerate(self.yvals):
            if val < lowest_val:lowest_val=val;lowest_x=self.xvals[i]
        return lowest_x,lowest_val
    
    def add_x_offset(self,offset_val):
        temp = self.xvals[:]
        self.xvals = []
        for w in temp:
            self.xvals.append(w-offset_val)
    def add_y_offset(self,offset_val):
        temp = self.yvals[:]
        self.yvals = []
        for w in temp:
            self.yvals.append(w-offset_val)

    def cleanup(self):
        #goes through values and deletes duplicate sequential y values
        y=0
        tempx = self.xvals[:]
        tempy = self.yvals[:]
        self.xvals = []
        self.yvals = []
        for i,val in enumerate(tempy):
            if val != y:
                self.xvals.append(tempx[i])
                self.yvals.append(tempy[i])
                y=val
        return


    def merge(self,new_xdata,new_ydata):
        # takes the line and interleaves passed line into it based on x value
        #ex. line1=[[1,2,3][2,3,4]] line1.merge([1.5,2,3.5],[7,8,9])
        # final line is [[1,1.5,2,3,3.5][2,7,5.5,4,9]]
        # if 2 values are the same it averages them, not duplicate
        
        for i,val in enumerate(new_xdata):          
            for i2,val2 in enumerate(self.xvals):
                if val<=val2:
                    if val == val2:
                        self.yvals[i2] = (self.yvals[i2]+new_ydata[i])/2
                    else:
                        self.xvals.insert(i2,val)
                        self.yvals.insert(i2,new_ydata[i])
                    break
    def __enter__(self):
        return self

    # ...

    def __exit__(self, exc_type, exc_value, traceback):
        pass

if __name__ == '__main__':
    def go(root,line_data,Graph):
            
        def read_data(x,y):
            x +=1
            y+=1
            
            return x,y
        x=0
        y=0
        for x in range(25):
            x,y=read_data(x,y)
            line_data.append(x,y)
            fig=Graph.A_line("rf",line_data)
            x,y=read_data(x,y)
            line2_data.append(x,y)
            fig=Graph.A_line("lev",line2_data)
            time.sleep(.25)
        x=0
        y=0
        for x in range (25):
            x,y=read_data(x,y)
            fig = Graph.A_point('none',x,y,Color='g')
            time.sleep(.25)
        

    root = tk.Tk()
    root.title('software version: {0}'.format('test'))

    main_frame = tk.Frame(root)
    main_frame.grid(row=0,column=0)

    line_data = Line()
    line2_data = Line()
    line2_data.set_color('b')
    Graph = Graph(root,size=(6,3),grid_row=4)

    b=tk.Button(main_frame,text="go",command=lambda:go(root,line_data,Graph))
    b.grid(row=1,column=1)
    root.mainloop

