/*Arduino code that runs the 3D scan with 2 IR sensors
 *Author: Hannah Kolano
 *Last updated: 9/17/17
 */

#include <Servo.h>

//set up variables and pins
int ir_value = 0;      //variable for the IR reading
int panpos = 0;        //variable for storing position of the pan servo
String result = "";    //string to send to the computer
const byte IR_PIN = A0; //pin of the IR input
byte cmd_id = 0;
int read1 = 0;
int read2 = 0;
int read3 = 0;
int read4 = 0;
int read5 = 0;

//set up servos 
Servo panservo;       //create servo objects


void setup() {
  panservo.attach(12);    //attaches servo on this pin to the servo object
  pinMode(IR_PIN, INPUT);        //declares the IR as an input
  Serial.begin(9600);

}

void loop() {
  int ir_value = analogRead(IR_PIN);

  if(Serial.available() > 0) {
    cmd_id = Serial.read();
  } else {
    cmd_id = 0;
  }

  switch(cmd_id) {
    case 1:
      scanPan();
      returnPan();
    default:
      delay(15);
  }
}

void scanPan() {
  for (panpos = 45; panpos <= 135; panpos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    panservo.write(panpos);              // tell servo to go to position in variable 'pos'
    delay(200);                       // waits 15ms for the servo to reach the position
    read1 = analogRead(IR_PIN);
    delay(50);
    read2 = analogRead(IR_PIN);
    delay(50);
    read3 = analogRead(IR_PIN);
    delay(50);
    read4 = analogRead(IR_PIN);
    delay(50);
    read5 = analogRead(IR_PIN);
    result = result + panpos + " " + read1 + " " + read2 + " " + read3 + " " + read4 + " " + read5;
    Serial.println(result);
    result = "";
  }
}

void returnPan() {
  for (panpos = 180; panpos >= 0; panpos -= 1) { // goes from 180 degrees to 0 degrees
    panservo.write(panpos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}
