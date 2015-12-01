__author__ = 'justin'

import numpy as np


c1=.001468
c2=.0002383
c3=.0000001007

analogread=498.0
Rk=10000.0 #ohms

voltage = analogread *5.0/1024.0
Rt = Rk*((5.0/voltage)-1)
logRt = np.log(Rt)
T = (1.0/(c1+c2*logRt+c3*logRt*logRt*logRt))-273.15 #celsius temp
Tf = (T*9.0/5.0)+32.0

voltage2=analogread*5.0/1024.0
Rt2=((1024.0/analogread)-1.0)*Rk
logRt2=np.log(Rt2)
T2= 1/(c1+c2*logRt2+c3*np.power(logRt2,3))-273.15
Tf2=(T2*9.0/5.0)+32

print"Analog read: %f"  %analogread
print"Voltage across known resistor: %f"  %voltage
print "Thermistor Resistance %f ohms" %Rt
print"Measured Temperature (C): %f"  %T
print "Measured Temperature (F): %f"  %Tf


print"Analog read: %f"  %analogread
print"Voltage across known resistor: %f"  %voltage2
print "Thermistor Resistance %f ohms" %Rt2
print"Measured Temperature (C): %f"  %T2
print "Measured Temperature (F): %f"  %Tf2


mT=23.88 #measured temperature in Celsius
mTF=75 #measured temperature in Celsius
Rt3= 10525.29 #expected resistance of thermistor ohms
Vs=5.0
I=Vs/(Rt3+Rk)
Vm=I*Rk
exanalogread=Vm*1024.0/Vs

print "Voltage Source: %f V" %Vs
print "Measured Temperature: %f C" %mT
print "Measured Temperature: %f F" %mTF
print "Expected thermisotr resistance: %f" %Rt3
print "Expected voltage across known resistor: %f" %Vm
print "Expected Analog Read %f" %exanalogread

Vs2=3.3
I2=Vs2/(Rt3+Rk)
Vm2=I2*Rk
exanalogread2=Vm2*1024.0/Vs2

print "Voltage Source: %f V" %Vs2
print "Measured Temperature: %f C" %mT
print "Measured Temperature: %f F" %mTF
print "Expected thermisotr resistance: %f" %Rt3
print "Expected voltage across known resistor: %f" %Vm2
print "Expected Analog Read %f" %exanalogread2