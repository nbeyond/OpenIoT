#include <FlowMeter.h>

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);

#define NUMFLAKES 10
#define XPOS 0
#define YPOS 1
#define DELTAY 2


#define LOGO16_GLCD_HEIGHT 16
#define LOGO16_GLCD_WIDTH  16
static const unsigned char PROGMEM logo16_glcd_bmp[] =
{ B00000000, B11000000,
  B00000001, B11000000,
  B00000001, B11000000,
  B00000011, B11100000,
  B11110011, B11100000,
  B11111110, B11111000,
  B01111110, B11111111,
  B00110011, B10011111,
  B00011111, B11111100,
  B00001101, B01110000,
  B00011011, B10100000,
  B00111111, B11100000,
  B00111111, B11110000,
  B01111100, B11110000,
  B01110000, B01110000,
  B00000000, B00110000 };


#if (SSD1306_LCDHEIGHT != 32)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif

// connect a flow meter to an interrupt pin (see notes on your Arduino model for pin numbers)
FlowSensorProperties DN50 = {200.0f, 0.234f, {1, 1, 1, 1, 1, 1, 1, 1, 1, 1}};
FlowSensorProperties DN32 = {120.0f, 0.45f, {1, 1, 1, 1, 1, 1, 1, 1, 1, 1}};
FlowMeter Meter1 = FlowMeter(2, DN50);
FlowMeter Meter2 = FlowMeter(3, DN50);
//FlowMeter Meter2 = FlowMeter(3, DN32);

// set the measurement update period to 1s (1000 ms)
const unsigned long period = 1000;

// define an 'interrupt service handler' (ISR) for every interrupt pin you use
void MeterISR1() {
  // let our flow meter count the pulses
  Meter1.count();
}
void MeterISR2() {
  // let our flow meter count the pulses
  Meter2.count();
}

void setup(){
  Serial.begin(115200); //turn on serial monitor

 // enable a call to a helper function on every rising edge
  attachInterrupt(INT0, MeterISR1, RISING);
  attachInterrupt(INT1, MeterISR2, RISING);

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3C (for the 128x32)
  // Clear the buffer.
  display.clearDisplay();
}

void loop() {
   // wait between output updates
  delay(period);

  // process the (possibly) counted ticks
  Meter1.tick(period);
  Meter2.tick(period);

  // output some measurement result
  Serial.print(Meter1.getCurrentFlowrate());
  Serial.print(" , ");
  Serial.print(Meter1.getTotalVolume());
  Serial.print(" , ");
  Serial.print(Meter2.getCurrentFlowrate());
  Serial.print(" , ");
  Serial.println(Meter2.getTotalVolume());

  display.setCursor(0,0);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.println("Open #2");
  display.print("P2: ");
  display.print(Meter1.getCurrentFlowrate());
  display.print(" L/min ");
  display.print(Meter1.getTotalVolume());
  display.println(" L");

  display.print("P3: ");
  display.print(Meter2.getCurrentFlowrate());
  display.print(" L/min ");
  display.print(Meter2.getTotalVolume());
  display.println(" L");

  display.display();
}


