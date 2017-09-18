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
cxn = Serial('/dev/ttyACM1', baudrate=9600)
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xvalues = [1, 2, 3]
yvalues = [1, 2, 3]


'''get data from arduino'''
cmd_id = int(input("Select '1' to begin"))
if cmd_id ==1:
    cxn.write([int(cmd_id)])

while(True):
        while cxn.inWaiting() < 1:
            pass
        result = cxn.readline()
        try:
            result = result.decode('UTF-8')
            new_angle, hypotenuse_raw = result.split(' ')
            print("angle", new_angle)
            print("reading", hypotenuse_raw)
        except UnicodeDecodeError:
            print("unicode error! help!")
            pass

        '''do the math'''
        #TODO: insert equation to turn hypotenuse_raw into a distance
        #TODO: insert equation to get real x and y Values
        #TODO: append x and y values to lists

zs = 0
ax.scatter(xvalues, yvalues, zs)


'''make the plot pretty'''
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z label')

plt.show()
