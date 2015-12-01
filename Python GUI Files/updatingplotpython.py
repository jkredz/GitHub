"""
ldr.py

Display analog data from Arduino using Python (matplotlib)

Author: Mahesh Venkitachalam
Website: electronut.in
"""
 
import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque
 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
 
    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, maxLen):
      # open serial port
      self.ser = serial.Serial(strPort, 9600)

      #create a double ended list of x and y values of desired size
      self.ax = deque([0.0]*maxLen)
      self.ay = deque([0.0]*maxLen)
      self.maxLen = maxLen
 
  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:                        #if deque is < max length append to deque
          buf.append(val)                               #append serial read value to the end of the deque list
      else:
          buf.pop()                                    #if deque is > max, then delete last value and append new value
          buf.appendleft(val)
 
  # add data (x,y) values
  def add(self, data):
      assert(len(data) == 2)
      self.addToBuf(self.ax, data[0])
      self.addToBuf(self.ay, data[1])
 
  # update plot
  def update(self, frameNum, a0, a1):
      try:
          line = self.ser.readline()                   #read serial to parse data
          data = [float(val) for val in line.split()]   #convert data into float values
          # print data
          if(len(data) == 2):                           #check the size of data -> if words, turn into ...
              self.add(data)
              a0.set_data(range(self.maxLen), self.ax)
              a1.set_data(range(self.maxLen), self.ay)
      except KeyboardInterrupt:
          print('exiting')
      
      return a0, 
 
  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()    

# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)
 
  # parse args
  args = parser.parse_args()
  
  #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort = args.port
 
  print('reading from serial port %s...' % strPort)
 
  # plot parameters
  analogPlot = AnalogPlot(strPort, 100)  #define strPOrt and max length of data
 
  print('plotting data...')
 
  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 100), ylim=(0, 1023))   #set maximum and minimum of the graph
  a0, = ax.plot([], [])
  a1, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=(a0, a1), 
                                 interval=50)
 
  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()
 
  print('exiting.')
  
 
# call main
if __name__ == '__main__':
  main()