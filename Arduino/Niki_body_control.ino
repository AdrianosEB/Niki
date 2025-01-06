#include <ContinuousServo.h>

boolean  isOK = true;
boolean varSwitchOn = true;
int  varCalibrationDelay = 500;
int  varLoopDelay = 100;
int  varMovementDelay = 500;

String incomingByte ;



// for Scenarios


//  D0  GPIO  16
//  D1  GPIO  5
//  D2  GPIO  4 ,  VO  , pin 22 to Mega 
//  D3  GPIO  0
//  D4  GPIO  2 
//  D5  GPIO  14
//  D6  GPIO  12
//  D7  GPIO  13
//  D8  GPIO  15

//int  inPinStartSpeak = 22;     // INPUT FROM  D2 OF ESP8266 , V1 FROM BLYNK
//int  varForStorePinStartSpeak = 0;      


//int  inPinMovingRightHand = 22;        
//int  inPinMovingLeftHand = 23;         
//int  varForStorePinRightHand = 0;      
//int  varForStorePinLeftHand = 0;      


int  inPinSmallBodyMoving = 22; 
int  varForStorePinSmallBodyMoving  = 0;


//int  inCalibrRightHandClockwise = 24;     
//int  inCalibrRightHandClockwise = 24;     
//int  inCalibrRightHandAntiClockwise = 25; 
//int  inCalibrRightHandBackward = 26;      
//int  inCalibrRightHandForward = 27;       

//int  varCalibrRightHandClockwise = 0;     // variable to store the read value
//int  varCalibrRightHandAntiClockwise = 0; // variable to store the read value
//int  varCalibrRightHandBackward = 0;      // variable to store the read value
//int  varCalibrRightHandForward = 0;       // variable to store the read value


//Right hand *********************************
ContinuousServo RightUpArm(2); // up arm , must  moving slow  till 10 , 1R 
ContinuousServo RightClockwise(3); // clockwise  antiClokwise , 2R
ContinuousServo RightForwardBackward(4); //forward , backward  ,  3R
ContinuousServo RightUpShoulder(5); // up shoulder , 4R


ContinuousServo Waist(6); // up shoulder , 4R

//Left hand *********************************
ContinuousServo LeftUpArm(8); // arm , must  moving slow till 10 , 1L
ContinuousServo LeftClockwise(9); // clockwise antiClokwise , 2L
ContinuousServo LeftForwardBackward(10); // forward , backward  , 3L
ContinuousServo LeftUpShoulder(11); //up shoulder   , 4L



void setup()
{
  Serial.begin(9600);
  pinMode(inPinSmallBodyMoving , INPUT);    // sets the digital pin 22 as input , D2  GPIO  4 ,  VO 
  
 // pinMode(inPinMovingLeftHand, INPUT);    // sets the digital pin 23 as input , V7 

  // for calibration
//  pinMode(inCalibrRightHandClockwise, INPUT);    // sets the digital pin 24 as input , V10
//  pinMode(inCalibrRightHandAntiClockwise, INPUT);    // sets the digital pin 25 as input , V11
//  pinMode(inCalibrRightHandBackward, INPUT);    // sets the digital pin 26 as input , V9
 // pinMode(inCalibrRightHandForward, INPUT);    // sets the digital pin 27 as input  , V8
 
}

void loop()
{

 
 while (Serial.available() > 0 ) // While have something
  {
     incomingByte = Serial.read();
     int n = incomingByte.toInt();
      switch(n)
    { 

      case  '1'   :  
         delay(100);
         RightHandSmallMovement();
         delay(100);
//WaistMoveRight();
         break;
      case  '2'   : 
         delay(100);
          LeftHandSmallMovement();
          delay(100);
         // WaistMoveLeft();
         break;
      default:
         break;

    }
  }

/*
 varForStorePinSmallBodyMoving = digitalRead(inPinSmallBodyMoving); 

   while (varForStorePinSmallBodyMoving == 1  ){
        WaistMoveRight();
         delay(200);
         varForStorePinSmallBodyMoving = digitalRead(inPinSmallBodyMoving);
         delay(2000);
   }

   while (varForStorePinSmallBodyMoving == 2  ){
        WaistMoveLeft();
         delay(200);
         varForStorePinSmallBodyMoving = digitalRead(inPinSmallBodyMoving);
         delay(2000);
   }
*/

}
//##################################################################

void RightHandSmallMovement(){

 
  RightUpShoulder.step(5);
  delay(200);
  RightUpShoulder.step(-6); 
  delay(200);
  RightClockwise.step(5); // right
  delay(200);
  RightClockwise.step(-6); //left
  delay(200);
  RightForwardBackward.step(5);    // backward
  delay(200);
  RightForwardBackward.step(-6);  // forward
  delay(200);

}

void LeftHandSmallMovement(){


   LeftUpShoulder.step(5);
   delay(200);
  LeftUpShoulder.step(-6); 
  delay(200);
  LeftClockwise.step(5); 
  delay(200);
   LeftClockwise.step(-7); 
  delay(200);
  LeftForwardBackward.step(5);
   delay(200);
  LeftForwardBackward.step(-6);
  delay(200);
  
  
}

void WaistMoveRight(){
  delay(35);
  Waist.step(30);

}

void WaistMoveLeft(){
  delay(35);
  Waist.step(-30);

}
