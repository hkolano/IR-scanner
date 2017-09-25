'''
plotscan.py
Purpose: Graphs input from 2 IR sensors into a 3D plot (PoE Lab 2)
Author: Hannah Kolano
hannah.kolano@students.olin.edu
Last edited 9/24/17
matplotlib tutorial: https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html

make sure the serial port corresponds correctly to the arduino
'''

'''import libraries'''
from serial import Serial, SerialException          # ability to talk to arduino
cxn = Serial('/dev/ttyACM0', baudrate=9600)         # defines communication port
import matplotlib.pyplot as plt                     # plotting tool
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
from numpy.polynomial import Polynomial as P        # math tools
import math as m

'''initialize data sets'''
xvalues = []
yvalues = []
zvalues = []

'''tell arduino when to start'''
cmd_id = int(input("Select '1' to begin"))          #waits for user input
if cmd_id == 1:
    cxn.write([int(cmd_id)])                        #writes input to arduino
else:
    print("That's not the number 1.")

'''main loop: get data from arduino'''
i = 0
'''loops (# pan angles)*(# tilt angles) times'''
while i <= 60*60:
    '''wait for and receive a message from arduino'''
    while cxn.inWaiting() < 1:            # wait for something from the arduino
        pass
    result = cxn.readline()              # read the message
    try:
        result = result.decode('UTF-8') # make the message readable
        pan_angle, hypotenuse_raw, tilt_angle = result.split(' ')
    except UnicodeDecodeError:
        print("unicode error! help!")
        pass
    '''change the raw input into a distance'''
    #ignore readings out of calibration range
    if int(hypotenuse_raw) > 220 and int(hypotenuse_raw) < 550:
        '''change raw input to actual distance'''
        #defines our calibration curve
        new_polynomial = P([807.74 - float(hypotenuse_raw), -18.27, .137])
        roots = new_polynomial.roots()         # finds roots of said polynomial
        raw_distance = roots.item(0)           # takes the relevant one

        '''change the angles so 0 is the center'''
        pan_center = m.radians(int(pan_angle)-90)
        tilt_center = m.radians(int(tilt_angle)-90)

        '''add coordinate to list'''
        xvalues.append(pan_center)
        yvalues.append(tilt_center)
        zvalues.append(raw_distance)
    else:
        pass
    i += 1      # up counter

'''assign colors based on distance away, in segments of 5cm'''
colors = []
for item in zvalues:
    if item <=25:
        new_color = "b"             # closest items are blue
    elif item >25 and item <=30:
        new_color = "c"             #then cyan
    elif item>30 and item <=35:
        new_color = "g"             #then green
    elif item>35 and item <=40:
        new_color = "y"             #then yellow
    elif item>40:
        new_color = "w"             #then white
    colors.append(new_color)

'''create scatterplot'''
ax.scatter(xvalues, yvalues, zvalues, c=colors)

'''make the plot pretty'''
ax.set_xlabel('Pan (radians)')
ax.set_ylabel('Tilt (radians)')
ax.set_zlabel('Distance Away (cm)')

plt.show()
