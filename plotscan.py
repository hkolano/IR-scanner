'''
plotscan.py
Purpose: Graphs input from 2 IR sensors into a 3D plot (PoE Lab 2)
Author: Hannah Kolano
hannah.kolano@students.olin.edu
Last edited 9/17/17
matplotlib tutorial: https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
'''

'''import libraries'''
from serial import Serial, SerialException
cxn = Serial('/dev/ttyACM0', baudrate=9600)
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
from numpy.polynomial import Polynomial as P
import math as m

xvalues = []
yvalues = []


'''get data from arduino'''
cmd_id = int(input("Select '1' to begin"))
if cmd_id == 1:
    cxn.write([int(cmd_id)])
else:
    print("That's not the number 1. Learn to read.")

i = 0
while i <= 90:
        while cxn.inWaiting() < 1:
            pass
        result = cxn.readline()
        try:
            result = result.decode('UTF-8')
            new_angle, read1, read2, read3, read4, read5 = result.split(' ')
            hypotenuse_raw = (int(read1)+int(read2)+int(read3)+int(read4)+int(read5))/5
            print("hypotenuse", hypotenuse_raw)
        except UnicodeDecodeError:
            print("unicode error! help!")
            pass
        if hypotenuse_raw > 220 and hypotenuse_raw < 500:
            '''change raw input to actual distance'''
            new_polynomial = P([807.74 - float(hypotenuse_raw), -18.27, .137])      # defines polynomial from calibration
            roots = new_polynomial.roots()                                          # finds roots of said polynomial
            raw_distance = roots.item(0)                                            # takes the relevant one
            print("roots", roots)

            '''take polar coordinates and change to cartesian'''
            angle_from_center = m.radians(int(new_angle)-90)
            y_value = raw_distance*m.cos(angle_from_center)
            x_value = -raw_distance*m.sin(angle_from_center)
            # print("distance from sensor", y_value)
            # print("distance from center", x_value)
            xvalues.append(x_value)
            yvalues.append(y_value)
        else:
            pass

        i += 1

zs = 0
ax.scatter(xvalues, yvalues, zs)


'''make the plot pretty'''
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z label')

plt.show()
