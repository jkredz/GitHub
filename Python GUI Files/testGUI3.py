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

SERIAL_PORT = "COM8"
MAX_LEN=100

serialConnection = serial.Serial(SERIAL_PORT, timeout=2.0 )

LARGE_FONT = ("Helvetica", 12)
style.use("ggplot")



f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)   #only one chart
tstate='Netural'
pstate = 'Recording'
b='black'
c= 'neturalbody.gif'
bccount=0
intcount='red'
skinrec=0

def z(tstate):
            return {
                'Hot' : 'red',
                'Warm':  'orange',
                'Neutral': 'green',
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
        global thermalstate, canvas2, bc, skintemp, interr, prototypestate, pstate, image2, b

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
        skinF= canvas2.create_text(440,350, fill="black", font =("Helvetica",24), anchor=tk.W, text="F")
        skintemp = canvas2.create_text(380,350, font =("Helvetica",24), anchor=tk.W, fill="black",text=skinrec)

        self.image2=tk.PhotoImage(file="neutralbody.gif")
        imgbody= canvas2.create_image(350,500,image=self.image2)


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
    xList=[0]*MAX_LEN                                     #empty list for X-axis values
    yList=[0]*MAX_LEN                            #empy list for Y-axis values
    global b, tstate, pstate, intcount, bccount, skinrec
    if pullData == 'Analyze Mode':                    #display states if text comes out
        pstate = 'Analyze Mode'
        print pullData
    elif pullData == 'Recording':
        pstate= 'Recording'
        print pullData
    elif pullData == 'Counting':
        pstate= 'Counting'
        print pullData
    elif pullData == 'asdfasd':
        pstate= ' '
        print pullData
    elif pullData == 'Temp Recording':
        pstate= 'Temp Recording'
        print pullData
    else:
        data = pullData.split(',')                  #convert data into float values
        # print data                                  #expected data format  [Time,Int#,BC,SkinTemp,Sensation,GPSloc]
        if(len(data) == 6):                           #check the size of data -> if words, turn into ...
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
            yList=y[1:]
            yList.append(skinrec)                  #append skinrec as Y-axis list
            b=z(tstate)
            c=x(tstate)

    a.clear()
    a.plot(yList)
    title = "Skin Temperature Recording (oF)"
    a.set_title(title)

    canvas2.itemconfig(thermalstate, fill=b, text=tstate)
    canvas2.itemconfig(interr, fill=intcount)
    canvas2.itemconfig(bc, text=bccount)
    canvas2.itemconfig(prototypestate, text=pstate)
    canvas2.itemconfig(skintemp, text=skinrec)
    #canvas2.itemconfig(StartPage.image2, file=c)

def x(tstate):
            return {
                'Hot' : 'hotbody.gif',
                'Warm':  'warmbody.gif',
                'Neutral': 'neutralbody.gif',
                'Cool': 'coolbody.gif',
                'Cold': 'coldbody.gif',
                } [tstate]



app = wearabletempGUI()
anim = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()

