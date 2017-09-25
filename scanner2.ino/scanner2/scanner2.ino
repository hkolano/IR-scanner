/*Arduino code that runs the 3D scan with 2 IR sensors
 *Author: Hannah Kolano
 *Last updated: 9/24/17
 */

#include <Servo.h>

//set up variables and pins
int ir_value = 0;      //variable for the IR reading
int panpos = 0;        //variable for storing position of the pan servo
int tiltpos = 0;       //variable for storing position of the tilt servo
String result = "";    //string to send to the computer
const byte IR_PIN = A0; //pin of the IR input
byte cmd_id = 0;        //a variable to receive from the python code
int readtotal = 0;

//set up servos 
Servo panservo;       //create servo objects
Servo tiltservo;

//code that runs once: set up the pins on the arduino
void setup() {
  panservo.attach(12);        //attaches servo on this pin to the servo object
  tiltservo.attach(13);
  pinMode(IR_PIN, INPUT);     //declares the IR as an input
  Serial.begin(9600);
}

//looping code: waits for the python to be ready and then scans 
void loop() {
  int ir_value = analogRead(IR_PIN);

  //see if cmd_id has changed (from the python code)
  if(Serial.available() > 0) {    
    cmd_id = Serial.read();
  } else {
    cmd_id = 0;
  }

  //decide what to do with cmd_id
  switch(cmd_id) {
    
    //if gets a "1" input from python, runs the scan
    case 1:
      for (tiltpos = 60; tiltpos <= 120; tiltpos +=1) {       //goes from 60 to 120
                                                              //in steps of 1
        tiltservo.write(tiltpos);           //tell servo to go to that position
        scanPan();                          //do a horizontal scan at this altitude
        returnPan();                        //return pan servo to original position
      }
      
    //if nothing has been received, wait
    default:
      delay(15);
  }
}

//moves the scanner in a panning direction, taking measurements along the way
void scanPan() {
  //loops for specified angles
  for (panpos = 60; panpos <= 120; panpos += 1) { //goes from 60-120 in steps of 1 
    panservo.write(panpos);                       //move servo to position 'panpos'
    delay(200);                                   //waits 200ms to get there
    //takes 5 measurements of the sensor
    readtotal += analogRead(IR_PIN);              //takes measurement from IR  
                                                  //and adds it to a total
    delay(50);                                    //gives time for scan to happen
    readtotal += analogRead(IR_PIN);
    delay(50);
    readtotal += analogRead(IR_PIN);
    delay(50);
    readtotal += analogRead(IR_PIN);
    delay(50);
    readtotal += analogRead(IR_PIN);
    readtotal = readtotal/5;                       //takes average of measurements
    
    //combine the positions of the motors and the average reading
    result = result + panpos + " " + readtotal + " " + tiltpos;     
    Serial.println(result);                     //sends this information to python 
    result = "";                                //reset variables
    readtotal = 0;
  }
}

//bring the pan servo back to its original position
void returnPan() {
  for (panpos = 120; panpos >= 60; panpos -= 1) { //go through angles back to start
    panservo.write(panpos);              //move servo through those angles
    delay(15);                       //gives it times to move
  }
}


