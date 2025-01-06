#include <Servo.h>

String incomingByte ;


// Arduino Nano , old bootloader ,  PWM : D3 , D5 , D6 , D9 , D10 ,D11
Servo servothumb;   // 3       
Servo servoindex;    //5       
Servo servomiddle;  //6
Servo servoring;   //9
Servo servopinky;  //10

int inPinMovingRightIndex  = 4; //  digital pin D4 
int inPinMovingRightHandOpen  = 2; //  digital pin D2 , V6
int  varForStorePinMovingRightIndex = 0;      // variable to store the read value
int  varForStorePinMovingRightHandOpen = 0;      // variable to store the read value


int pos = 0;    // variable to store the servo position


void setup() {

  // signals comes from Ardino Mega
   pinMode(inPinMovingRightIndex , INPUT);   
   pinMode(inPinMovingRightHandOpen , INPUT);   
   
  Serial.begin(9600);
  servothumb.attach(3); 
   
  servoindex.attach(5); 
  servomiddle.attach(6);
   servoring.attach(9);
  servopinky.attach(10);
    
}


void loop() {
  delay(300);
  CloseFingers();

  while (Serial.available() > 0 ) // While have something
  {
     incomingByte = Serial.read();
     int n = incomingByte.toInt();
      switch(n)
    { 

      case  '1'   :  
         delay(100);
         OpenFingers();
         break;
      case  '2'   : 
         delay(100);
          CloseFingers();
         break;
      default:
         break;

    }
  }

/*
  // Serial.println("close fingers  ");
  

  //delay(3000);
 // OpenFingers();
 
 // Serial.println("open  fingers  ");

 // varForStorePinMovingRightIndex = digitalRead(inPinMovingRightIndex);

 // Serial.println("varForStorePinMovingRightIndex =  ");
 // Serial.println(varForStorePinMovingRightIndex);

//   while (varForStorePinMovingRightIndex == 1  ){
//       Serial.println("inside while varForStorePinMovingRightIndex ");
//        RightHandSayYou();
//        delay(500);
//    varForStorePinMovingRightIndex = digitalRead(inPinMovingRightIndex);
//   }

  delay (300);
  
   varForStorePinMovingRightHandOpen = digitalRead(inPinMovingRightHandOpen);
    Serial.println("varForStorePinMovingRightHandOpen =  ");
  Serial.println(varForStorePinMovingRightHandOpen);

   while (varForStorePinMovingRightHandOpen == 1  ){
      // Serial.println("inside while varForStorePinMovingRightHandOpen ");
        RightHandSayHi();
        delay(500);
    varForStorePinMovingRightHandOpen = digitalRead(inPinMovingRightHandOpen);
   }

   */

  delay(300);
}


void CloseFingers(){
pos = 80; // means close
                       
servopinky.write(pos);
delay(110);
servoring.write(pos);
delay(110);
servomiddle.write(pos);
delay(110);
servoindex.write(pos);
delay(110);
servothumb.write(pos);
delay(110);

  
  }

void OpenFingers(){
pos = 0; // means open
                       
servopinky.write(pos);
delay(110);
servoring.write(pos);
delay(110);
servomiddle.write(pos);
delay(110);
servoindex.write(pos);
delay(110);
servothumb.write(pos);
delay(110);

  
  }

void detachAll(){

                       
servopinky.detach();
delay(110);
servoring.detach();
delay(110);
servomiddle.detach();
delay(110);
servoindex.detach();
delay(110);
servothumb.detach();
delay(110);

  
  }

void RightHandSayYou(){
pos = 80; // means close
                       
servopinky.write(pos);
delay(110);
servoring.write(pos);
delay(110);
servomiddle.write(pos);
delay(110);
servoindex.write(0); // means open
delay(110);
servothumb.write(pos);
delay(110);

  
  }


void RightHandSayHi(){
pos = 0; // means open
  
servopinky.write(pos);
delay(110);
servoring.write(pos);
delay(110);
servomiddle.write(pos);
delay(110);
servoindex.write(pos);
delay(110);
servothumb.write(pos);
delay(110);



}
