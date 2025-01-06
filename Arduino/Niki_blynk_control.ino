// Code from the API of arduino connect to Blynk
/board 8266 : LOLIN (WeMos) D1 R1
//D2 = 4  , D6 = 12 ,D7 = 13 , D8 = 15


//D6 = 12 (from 4 Aruino )  , D7 = 13 (from 7 Aruino )   , D2 = 4(from 8 Arduino )

//D5 = 14 ( Head control Left Rigt )

#define BLYNK_TEMPLATE_ID "TMPLoDOYaEx0"
#define BLYNK_TEMPLATE_NAME "Quickstart Template"
#define BLYNK_AUTH_TOKEN "R7BRCZ79VFCyzRwnx4AKvPmVkUEDHKlG"


#define BLYNK_PRINT Serial
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <Servo.h>

#include "ServoEasing.hpp"

//ServoEasing servoLeftRightHead;

#define PinControlBodyLeftHand 14 // 14 means D5 pin of ESP8266 , 23 Arduino  , V7



int varServoMaxPos;

Servo servoNeckLeftRight; //   D3 pin of ESP8266 , V4  




char ssid[] = "VODAFONE_9627";
char pass[] = "XXXXXXXXXX";


void setup()

{

  Serial.begin(9600);

   Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);

  //servoLeftRightHead.attach(14, 90);  //D5 mens 14

  servoNeckLeftRight.attach(14); //  14  means  D5 pin of ESP8266  , V4  
                   
 }

void loop()

{ Blynk.run();}


//#########################################################################
// This function will be called every time Slider Widget
// in Blynk app writes values to the Virtual Pin 4 ,  D3  GPIO  0 ,  V4 , servoNeckLeftRight
BLYNK_WRITE(V4) {  //servoNeckLeftRight
  delay(15);
 
  int pinValue = param.asInt(); // assigning incoming value from pin V4 to a variable
  // You can also use:
  // String i = param.asStr();
  // double d = param.asDouble();
  Serial.print("V4 (servoNeckLeftRight - D3 ) Slider value is: ");
  Serial.println(pinValue);
  delay(50);
  servoNeckLeftRight.write(pinValue);
  //servoLeftRightHead.easeTo(pinValue ,3000);
}
