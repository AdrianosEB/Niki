#include <Servo.h>
//COM12
// PWM IN NANO D3 , D5 , D6 , D9 , D10 , D11
int incomingByte = 0;
//String incomingByte ;
char val;
Servo myservo;
const int led = 5;
String inString = "";

void setup() {
  Serial.begin(9600);
  myservo.attach(3);
  myservo.write(0);
}

void loop() {
  delay(500);
  while (Serial.available() > 0 ) // While have something
  {

   incomingByte = Serial.read();
  Serial.println("incomingByte ");
  Serial.println(incomingByte);
 
  switch(incomingByte)
    { 
      case  '1'   :
         delay(100);
         myservo.write(0);
         break;
      case  '2' : 
         delay(100);
         myservo.write(10);
         break;
      case  '3' :
          delay(100);
         myservo.write(15);
         break;
      case  '4' :
          delay(100);
         myservo.write(20);
         break;
      case  '5' :
         delay(100);
         myservo.write(25);
         break;
      case  '6' :
          delay(100);
         myservo.write(30);
         break;
      case  '7' :
          delay(100);
         myservo.write(35);
         break;
      case  '8' :
          delay(100);
         myservo.write(40);
         break;
      case  '9' :
          delay(100);
         myservo.write(45);
         break;
      case  '10' :
          delay(100);
         myservo.write(50);
         break;
      case  '11' :
          delay(100);
         myservo.write(55);
         break;
      case  '12' :
          delay(100);
         myservo.write(60);
         break;
      case  '13' :
          delay(100);
         myservo.write(65);
         break;
      case  '14' :
          delay(100);
         myservo.write(70);
         break;
      default:
         myservo.write(0);
         break;
  }

}
}
