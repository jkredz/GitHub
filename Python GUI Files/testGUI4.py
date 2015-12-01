import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import datetime
import Tkinter as tk
import ttk
import serial


MAX_LEN=20
global xList, yList
xList=[0]*MAX_LEN                                       #empty list for X-axis values
yList=[0]*MAX_LEN                                       #empy list for Y-axis values

serialConnection = serial.Serial(SERIAL_PORT, timeout=2.0 )

LARGE_FONT = ("Helvetica", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)   #only one chart
tstate='Netural'
pstate = 'Data Recording State'
b='black'
c='neutralbody.gif'
bccount=0
intcount='red'
skinrec=0

def z(tstate):
            return {
                'Hot' : 'red',
                'Warm':  'orange',
                'Neutral': 'black',
                'Cool': 'blue',
                'Cold': 'purple',
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
        label = ttk.Label(self, text="start page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        #Canvas for Data Display
        global thermalstate, canvas2, bc, skintemp, interr, prototypestate, pstate, h, b, c

        canvas2 = tk.Canvas(master=self, width=800, height=800)
        canvas2.pack(side=tk.LEFT)

        thermalstatelabel = canvas2.create_text(100,150, fill="black", font =("Helvetica",24), anchor=tk.W, text="Thermal State:")
        thermalstate = canvas2.create_text(350,150, fill=b, font =("Helvetica",24), anchor=tk.W, text=tstate)


        prototypestatelabel = canvas2.create_text(100,200, fill="black",font =("Helvetica",24), anchor=tk.W, text="Prototype State:")
        prototypestate = canvas2.create_text(350,200, fill="black",font =("Helvetica",24), anchor=tk.W, text=pstate)

        bclabel = canvas2.create_text(100,250, fill="black", font =("Helvetica",24), anchor=tk.W, text="Button Count:")
        bc = canvas2.create_text(350,250, fill="black", font =("Helvetica",24), anchor=tk.W, text=bccount)


        interlabel = canvas2.create_text(100,300, fill="black", font =("Helvetica",24), anchor=tk.W, text="Gesture Input:")
        interr = canvas2.create_oval(330,275, 380,325, fill=intcount)

        skintemplabel = canvas2.create_text(100,350, fill="black", font =("Helvetica",24), anchor=tk.W, text="Skin Temperature:")
        skinF= canvas2.create_text(460,350, fill="black", font =("Helvetica",24), anchor=tk.W, text="F")
        skintemp = canvas2.create_text(380,350, font =("Helvetica",24), anchor=tk.W, fill="black",text=skinrec)

        #self.image2=tk.PhotoImage(file=c)
        #h=self.image2
        h=tk.PhotoImage(file=c)
        imgbody= canvas2.create_image(350,500,image=h)


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
    print pullData

    global b, tstate, pstate, intcount, bccount, skinrec, xList, yList, c

    if pullData == 'Analyze Mode':                    #display states if text comes out
        pstate = 'Analyze Mode'
    elif pullData == 'Data Recording State':
        pstate= 'Data Recording State'
    elif pullData == 'Button Counting State':
        pstate= 'Button Counting State'
    elif pullData == 'Transition State':
        pstate= 'Transition State'
    elif pullData == 'Temp Recording':
        pstate= 'Temp Recording'
    else:
        data = pullData.split(',')
        # print data                                                               #expected data format  [Time,Int#,BC,SkinTemp,Sensation,GPSloc]
        if(len(data) == 6) :                           #check the size of data -> if words, turn into ...
            time=data[0]
            intcount=int(data[1])


            if intcount > 0:
                intcount = 'green'
            else:
                intcount = 'red'
            bccount=int(data[2])
            skinrec=float(data[3])
            tstate=data[4]
            GPSloc=data[5]
            xList.append(time)                   #append time as X-axis list
            yList=yList[:-1]
            yList.insert(0,skinrec)                  #append skinrec as Y-axis list
            b=z(tstate)                            #adjust text color of tstate
            c=x(tstate)                            #adjust thermal picture state based on tstate
            print c
    a.clear()
    a.plot(yList)
    title = "Skin Temperature Recording (F)"
    a.set_title(title)
    a.set_ylabel('Skin Temperature F')
    a.set_xlabel('Last 20 Recordings')

    canvas2.itemconfig(thermalstate, fill=b, text=tstate)
    canvas2.itemconfig(interr, fill=intcount)
    canvas2.itemconfig(bc, text=bccount)
    canvas2.itemconfig(prototypestate, text=pstate)
    canvas2.itemconfig(skintemp, text=skinrec)
    h=tk.PhotoImage(file=c)
    imgbody= canvas2.create_image(500,600,image=h)
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
if __name__ == “__main__”:
    if len(sys.argv) != 3:
      print "USAGE:  python combineData_REALDISP.py <input_filename> <output_filename>"
      sys.exit(1)
    print sys.argv
    SERIAL_PORT=sys.argv[1]

    try:
    app = wearabletempGUI()
    anim = animation.FuncAnimation(f, animate, interval=500)
    app.mainloop()

