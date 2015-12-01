#!/usr/bin/env python
'''
Color parts of a line based on its properties, e.g., slope.
'''


import numpy as np
'''
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

x = np.array((1, 2, 3, 4, 5, 6, 7))
y = np.array((2, 4, 5, 6, 7, 8, 9))
'''
z = np.array((0, 0, 0, 1, 0, 0, 0))  # first derivative
'''
# Create a colormap for red, green and blue and a norm to color
# f' < -0.5 red, f' > 0.5 blue, and the rest green
cmap = ListedColormap(['r', 'g', 'b'])
norm = BoundaryNorm([-1, -0.5, 0.5, 1], cmap.N)

# Create a set of line segments so that we can color them individually
# This creates the points as a N x 1 x 2 array so that we can stack points
# together easily to get the segments. The segments array for line collection
# needs to be numlines x points per line x 2 (x and y)
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Create the line collection object, setting the colormapping parameters.
# Have to set the actual values used for colormapping separately.
lc = LineCollection(segments, cmap=cmap, norm=norm)
lc.set_array(z)
lc.set_linewidth(3)

fig1 = plt.figure()
a1=fig1.add_subplot(2,1,1)
plt.gca().add_collection(lc)
plt.xlim(x.min(), x.max())
plt.ylim(-10, 10)


a2 = fig1.add_subplot(2,1,2)   #only one chart

print x[:1]
print y[:1]
#plt.plot(x[2:3],y[2:3],'b')
#plt.plot(x[4:6],y[4:6],'b')
plt.plot(x[:1],y[:1],'b')


title = "Skin Temperature Recording (F)"
a2.set_title(title)
a2.set_ylim([min(y)-.5,max(y)+.5])      # +/- 2F buffer for the graphing
a2.set_ylabel('Skin Temperature F')
a2.set_xlabel('Last 20 Recordings')

plt.show()
'''

print z
index=0
start=0
for value in z:
        print "value is %d" %value
        print "start value is  %d" %start
        try:
            if (z[index+1] == z[index]):  #if the state is the same continue on the list

                index = index+1
            else:
                end=index
                print "start index: %d,  end index: %d"  %(start,end)
                print z[start:end+1]

                index=index+1
                start=index

        except IndexError:
            start=start
            end2=index
            print "start index: %d,  end index: %d"  %(start,end2)
            print z[start:end2+1]

