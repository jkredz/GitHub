#!/usr/bin/env python
import matplotlib
matplotlib.use('TkAgg')

from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)   #only one chart

def animate(i):
    pullData=open("sampleData2.txt","r").read()
    dataList = pullData.split('\n')
    xList=[]
    yList=[]
    for eachline in dataList:
        if len(eachLine) > 1:
            x,y= eachLine.spit(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear
    a.plot(xList,yList)




import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

def destroy(e): sys.exit()


#Initialize Serial Communication
 # create parser
#parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
#parser.add_argument('--port', dest='port', required=True)

  # parse args
#args = parser.parse_args()

  #strPort = '/dev/tty.usbserial-A7006Yqh'
#strPort = args.port

#print('reading from serial port %s...' % strPort)

##serial read data for new data to parse
"""
try:
    line = ser.readline()                   #read serial to parse data

    if line == 'asdfasf':
        pstate = 'asfdas'
    elif line == 'asdfasd':
        pstate= ' '
    elif line == 'asdfasd':
        pstate= ' '
    elif line == 'asdfasd':
        pstate= ' '
    elif line == 'asdfasd':
        pstate= ' '
    else:
        data = [val in line.split()]   #convert data into float values
        # print data                                  #expected data format  [Time,Int#,BC,SkinTemp,Sensation,GPSloc]
        if(len(data) == 6):                           #check the size of data -> if words, turn into ...
            time=data[0]
            intcount=int(data[1])
            bccount=int(data[2])
            skinrec=float(data[3])
            tstate=data[4]
            GPSloc=data[5]
            add(skinrec)
            a0.set_data(range(self.maxLen), self.ax)
        else:                                         #if data isnt data recording then ignore
    return a0,

analogPlot = AnalogPlot(strPort, 100)  #define strPort and max length of data
"""

print('plotting data...')
root = Tk.Tk()
# Name of title
root.wm_title("Skin Temperature Recording")
#root.bind("<Destroy>", destroy)


##axis?
#animation
#a0, = ax.plot([], [])

# a tk.DrawingArea
canvas=FigureCanvasTkAgg(f,master=root)
canvas.show()
canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=TRUE)  #display canvas of graph

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=TRUE)

anim = animation.FuncAnimation(f, animate, interval=1000)

#Canvas for Data Display
canvas2 = Canvas(root, width=800, height=800)
canvas2.pack(side=LEFT)

tstate='hot"'

def f(tstate):
    return {
        'hot' : 'red',
        'warm':  'orange',
        'neutral': 'green',
        'cool': 'blue',
        'cold': 'purple',
        } [tstate]
b=f(tstate)

thermalstatelabel = canvas2.create_text(0,150, fill="black", text="Thermal State:")
thermalstate = canvas2.create_text(50,150, fill=b, text=tstate)


prototypestatelabel = canvas2.create_text(0,170, fill="blue",text="Prototype State:")
prototypestate = canvas2.create_text(50,170, fill="black",text="Recording")

bclabel = canvas2.create_text(0,190, fill="blue",text="Gesture Input:")
bc = canvas2.create_text(50,190, fill="black",text="0")


interlabel = canvas2.create_text(0,210, fill="blue",text="Button Count:")
interr = canvas2.create_oval(50,210, 100,100, fill="black")

skintemplabel = canvas2.create_text(0,230, fill="blue", anchor=W, text="Skin Temp:")
skintemp = canvas2.create_text(50,230, fill="black",text="90")

#image2=PhotoImage(file="neutralbody.png")
#imgbody= canvas2.create_image(400,400,image=image2)

#Optional Matlib Plot Toolbar
#toolbar = NavigationToolbar2TkAgg( canvas, root )
#toolbar.update()

canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


#Quit Button
button = Tk.Button(master=root, text='Quit', command=sys.exit)
button.pack(side=Tk.BOTTOM)

#Continuously Run Graphing Loop
Tk.mainloop()

class AnalogPlot:
  # constr
    def __init__(self, strPort, maxLen):
        # open serial port
        self.ser = serial.Serial(strPort, 9600)

        #create a double ended list of x and y values of desired size
        self.ax = deque([0.0]*maxLen)
        self.maxLen = maxLen

    def add(self, data):
        assert(len(data) == 1)
        self.addToBuf(self.ax, data[0])

    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:                        #if deque is < max length append to deque
            buf.append(val)                               #append serial read value to the end of the deque list
        else:
            buf.pop()                                    #if deque is > max, then delete last value and append new value
            buf.appendleft(val)
    # clean up
    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()
          # update plot

    '''
    def update(self, frameNum, a0):
        try:
            line = ser.readline()                   #read serial to parse data
            if line == 'asdfasf':
                pstate = 'asfdas'
            elif line == 'asdfasd':
                pstate= ' '
            elif line == 'asdfasd':
                pstate= ' '
            elif line == 'asdfasd':
                pstate= ' '
            elif line == 'asdfasd':
                pstate= ' '
            else:
                data = [float(val) for val in line.split()]   #convert data into float values
                # print data                                  #expected data format  [Time,Int#,BC,SkinTemp,Sensation,GPSloc]
                if(len(data) == 6):                           #check the size of data -> if words, turn into ...
                    time=str(data[0])
                    intcount=int(data[1])
                    bccount=int(data[2])
                    skinrec=data[3]
                    tstate=str(data[4])
                    GPSloc=str(data[5])
                    add(skinrec)
                    a0.set_data(range(self.maxLen), self.ax)
       '''