#include <SPI.h> 
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

int incomingByte = 0;
int current_state = 1;
// PWM IN NANO D3 , D5 , D6 , D9 , D10 , D11

// SCL    --> GREEN , A5   ,  yellow
// SDA    --> ORANGE , A4  ,  white
// GROUND --> BROWN        ,  black
// Vcc    --> RED          ,  red

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
// The pins for I2C are defined by the Wire-library. 
// On an arduino UNO:       A4(SDA), A5(SCL)  
// On an arduino MEGA 2560: 20(SDA), 21(SCL)
// On an arduino LEONARDO:   2(SDA),  3(SCL), ...
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


void drawCircleRight(void) {
  for (int16_t i=10; i<display.height()-32; i+=2) {
    //display.drawCircle((display.width()/2)+50, display.height()/2, i, SSD1306_WHITE);
    display.drawCircle((display.width()/2)+50, display.height()/3, i, SSD1306_WHITE);
    display.display();
    delay(10);

  }
  }

  void drawCircleLeft(void) {
  for (int16_t i=10; i<display.height()-32; i+=2) {
    //display.drawCircle((display.width()/2)-50, display.height()/2, i, SSD1306_WHITE);
    display.drawCircle((display.width()/2)-50, display.height()/3, i, SSD1306_WHITE);
    display.display();
    delay(10);

  }
  }


void drawCircle(void) {
  for (int16_t i=10; i<display.height()-32; i+=2) {
    display.drawCircle((display.width()/2), display.height()/2, i, SSD1306_WHITE);
    display.display();
    delay(10);

   
  }
 

 
}


void setup() {
  Serial.begin(9600);

  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    //Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
  
  display.display();
  delay(1000);
  display.clearDisplay();

  display.display();

  // display.flipScreenVertically();

  //display.setContrast(255);

 

  drawCircle();
  delay(1000);
  display.clearDisplay();

 
}

void loop() {

  while (Serial.available() > 0 )
   {
    
    //incomingByte = Serial.read();
    
    incomingByte = Serial.parseInt();
   Serial.println(" incomingByte = ");
   Serial.println(incomingByte );
    switch(incomingByte)
    {
       case 1:
        current_state = 1; //IDLE
        break;
      case 2:
        current_state = 2; //LISTENING
        break;
      case 3:
        current_state = 3; //PROCESSING
        break;
      case 4:
        current_state = 4; //TALKING
        break;
      default:
        break;
    }
  }

display.clearDisplay();

Serial.println(current_state);

  switch(current_state)
    { 
      case 1: //IDLE
        //display.drawCircle((display.width()/2), display.height()/2, 10, SSD1306_WHITE);
        drawCircle();
        delay(1000);
        break;
      case 2: //LISTENING
        //display.fillCircle((display.width()/2), display.height()/2, 20, SSD1306_WHITE);
        drawCircleLeft();
        delay(1000);
        break;
      case 3: //PROCESSING
      drawCircleRight();
      delay(1000);
       // Set text size
       // display.setTextSize(2);
        // Set text color to white
       // display.setTextColor(SSD1306_WHITE);
        // Set cursor position
       // display.setCursor(0, 0);
        // Print the text "..."
       // display.print("...");
        break;
      case 4: //TALKING
       // display.drawCircle((display.width()/2), display.height()/2, 5, SSD1306_WHITE);
       drawCircle();
       delay(1000);
        break;
      default: //IDLE
        break;
    }

    display.display();

  }
