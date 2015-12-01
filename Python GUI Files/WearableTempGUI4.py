import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import Tkinter as tk
import ttk
import serial
import sys
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style

MAX_LEN=25
global xList, yList, zList
xList=np.arange(1,MAX_LEN+1)                                      #empty list for X-axis values
yList=np.zeros(MAX_LEN)                                       #empy list for Y-axis values
zList=["black"]*MAX_LEN

SERIAL_PORT=sys.argv[1]
serialConnection = serial.Serial(SERIAL_PORT, timeout=2.0 )

SMALL_FONT = ("Helvetica", 24)
LARGE_FONT = ("Helvetica", 32)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)   #only one chart

tstate='Netural'
pstate = 'Data Recording State'
b='Black'
c='neutralbody.gif'
bccount=0
intcount='red'
skinrec=0

def z(tstate):
            return {
                'Hot' :   'Red',
                'Warm':  'Orange',
                'Neutral': 'Black',
                'Cool':    'Cyan',
                'Cold':    'Blue',
                } [tstate]


class wearabletempGUI(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Wearable Temp Sensor GUI")      #window title
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames= {}

        frame = StartPage(container, self)
        self.frames[StartPage] = frame

        frame.grid(row=0, column= 0, sticky ="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame=self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="Wearable Thermal Comfort System UI", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        #Canvas for Data Display
        global thermalstate, canvas2, bc, skintemp, interr, prototypestate, pstate, h, b, c

        canvas2 = tk.Canvas(master=self, width=800, height=800)
        canvas2.pack(side=tk.LEFT)

        thermalstatelabel = canvas2.create_text(50,150, fill="black", font=LARGE_FONT, anchor=tk.W, text="Thermal State:")
        thermalstate = canvas2.create_text(370,150, fill=b, font=LARGE_FONT, anchor=tk.W, text=tstate)


        prototypestatelabel = canvas2.create_text(50,225, fill="black",font=LARGE_FONT, anchor=tk.W, text="Prototype State:")
        prototypestate = canvas2.create_text(370,225, fill="black",font=LARGE_FONT, anchor=tk.W, text=pstate)

        bclabel = canvas2.create_text(50,300, fill="black", font=LARGE_FONT, anchor=tk.W, text="Button Count:")
        bc = canvas2.create_text(370,300, fill="black", font=LARGE_FONT, anchor=tk.W, text=bccount)

        bc2=canvas2.create_rectangle(390,300, 450,400, fill='white')


        interlabel = canvas2.create_text(50,375, fill="black", font=LARGE_FONT, anchor=tk.W, text="Gesture Input:")
        interr = canvas2.create_oval(350,395, 400,345, fill=intcount)

        skintemplabel = canvas2.create_text(50,450, fill="black", font=LARGE_FONT, anchor=tk.W, text="Skin Temperature:")
        skinF= canvas2.create_text(550,450, fill="black", font=LARGE_FONT, anchor=tk.W, text="F")
        skintemp = canvas2.create_text(420,450, font=LARGE_FONT, anchor=tk.W, fill="black",text=skinrec)

        self.image2=tk.PhotoImage(file=c)
        h=self.image2
        #h=tk.PhotoImage(file=c)
        #imgbody= canvas2.create_image(350,500,image=h)


        #Graphing Data
        canvas=FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  #display canvas of graph

        #tool bar
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

##update plot code
def animate(i):
    pullData=serialConnection.readline().strip()
    global b, tstate, pstate, intcount, bccount, skinrec, xList, yList, c, zList

    if pullData == 'Analyze Mode':                    #display states if text comes out
        pstate = 'Analyze Mode'
    elif pullData == 'Data Recording State':
        pstate= 'Data Recording State'
    elif pullData == 'Button Counting State':
        pstate= 'Button Counting State'
    elif pullData == 'Transition State':
        pstate= 'Transition State'
    elif pullData == 'Thermal Recording State':
        pstate= 'Temp Recording'
    elif pullData[:12] == 'Button Count':
        bccount = int(pullData[14:])
        #print bccount
    elif pullData == 'WiFi Mode':
        pstate='WiFi Mode'
    elif pullData[:9] == 'Intevent:':
        intcount=int(pullData[10:])
        if intcount > 0:
            intcount = 'green'
        else:
            intcount = 'red'
    else:
        data = pullData.split(',')
        # print data                                                               #expected data format  [Time,Int#,BC,SkinTemp,Sensation,GPSloc]
        if(len(data) == 6) :                           #check the size of data -> if words, turn into ...
            #time=data[0]
            bccount=int(data[2])
            skinrec=float(data[3])
            tstate=data[4]
            #GPSloc=data[5]
            zList=zList[:-1]
            linecolor=z(tstate)
            #print linecolor
            zList.insert(0,linecolor)                  #append skinrec as Y-axis list
            #print zList
            yList=yList[:-1]
            yList=np.insert(yList,0,skinrec)                  #append skinrec as Y-axis list
            #print yList
            #print xList
            b=z(tstate)                            #adjust text color of tstate
            c=x(tstate)                            #adjust thermal picture state based on tstate
            #print c
    a.clear()

    index=0
    start=0
    end=0
    for value in zList:
        #print "value is %s" %value
        #print "start value is  %d" %start
        try:
            if (zList[index+1] == zList[index]):  #if the state is the same continue on the list
                index = index+1
            else:
                end=index
                a.plot(xList[start:end+1],yList[start:end+1], color=value, marker='o')
                index=index+1
                start=index

        except IndexError:
            start=start
            end2=index
            #print "start index: %d,  end index: %d"  %(start,end2)
            a.plot(xList[start:end2+1],yList[start:end2+1], color=value, marker='o')

    title = "Skin Temperature Recording (F)"
    a.set_title(title)
    a.set_xlim(0,max(xList))
    a.set_ylim([min(yList)-.5,max(yList)+.5])      # +/- 2F buffer for the graphing
    a.set_ylabel('Skin Temperature F')
    a.set_xlabel('Last %d Recordings' %MAX_LEN)


    canvas2.itemconfig(thermalstate, fill=b, text=tstate)
    canvas2.itemconfig(interr, fill=intcount)
    canvas2.itemconfig(bc, text=bccount)
    canvas2.itemconfig(prototypestate, text=pstate)
    canvas2.itemconfig(skintemp, text=skinrec)
    h=tk.PhotoImage(file=c)
    #imgbody= canvas2.create_image(500,600,image=h)
    #canvas2.itemconfig(h, file=c)

def x(tstate):
            return {
                'Hot' :   'hotbody.gif',
                'Warm':  'warmbody.gif',
                'Neutral': 'neutralbody.gif',
                'Cool':    'coolbody.gif',
                'Cold':    'coldbody.gif',
                } [tstate]



# if run as top-level script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "USAGE:  python WearableTempGUI4.py <COM#>"
        sys.exit(1)
    print sys.argv


app = wearabletempGUI()
anim = animation.FuncAnimation(f, animate, interval=100)
app.mainloop()