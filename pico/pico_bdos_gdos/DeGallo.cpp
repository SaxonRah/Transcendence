//DeGallo.cpp
//(Processor)     Pimoroni Pico LiPo 16MB
//(SPI)           Pimoroni Display Pack 2.0 (PIM580)
//(I2C)           Pimoroni Trackball (PIM447)
//(I2C)           Adafruit PCA9546 4-Channel I2C Multiplexer
//(SPI and I2C)   Adafruit PiCowbell Adalogger - MicroSD, RTC

//Arduino IDE with PicoProbe
//Port:           COM9 (PicoProbe)
//Debug Level:    All
//Debug Port:     Serial
//Update Method:  PicoProbe

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "hardwareSerial.h"

#include <SD.h>
#include <SPI.h>
#include <Wire.h>

#include "Adafruit_ST7789.h"

#include "Mouse.h"
#include <pimoroniTrackball.h>

#include "RTClib.h"

// I2C
// Multiplexer - I2C 0x70
#define I2C_MULTIPLEXER 0x70
// PCA Port #0 - I2C 0x68 - Adalogger RTC (SD must be connected to MISO, MOSI, CS, SCK)
#define I2C_RTC 0x68
// PCA Port #1 - I2C 0x0A  - Trackball
#define I2C_TB 0x0A

// Real Time Clock
RTC_PCF8523 rtc;

// Pimoroni Display 2 Screen
#define TFT_DC 16  // Shares SPI 1 Bus
#define TFT_CS 17
#define TFT_SCLK 18  // Shares SPI 1 Bus
#define TFT_MOSI 19  // Shares SPI 1 Bus
#define TFT_RST -1
#define TFT_BL 20
Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST);

// Adalogger SD Card Slot
#define SD_DETECT 15
#define SD_MISO 16  // Shares SPI 1 Bus
#define SD_CS 22
// #define SD_CS 27
#define SD_SCK 18   // Shares SPI 1 Bus
#define SD_MOSI 19  // Shares SPI 1 Bus

File logfile;

// Pimoroni Trackball
uint8_t mouseSpeed = 5;  //Change this to alter the mouse speed
int16_t x = 0;
int16_t y = 0;

bool RTC_INIT = false;
bool SD_INIT = false;
bool TB_INIT = false;
bool SCREEN_INIT = false;

void pca_select(uint8_t i) {
  if (i > 3) return;
  Wire.beginTransmission(I2C_MULTIPLEXER);
  Wire.write(1 << i);
  Wire.endTransmission();
}

void debug_msg(const String& debug_message) {
  
  digitalWrite(SD_CS, HIGH);  // Deactivate SD card CS
  digitalWrite(TFT_CS, LOW);  // Activate Screen CS

  Serial.println(debug_message + String(" "));
  if (SCREEN_INIT) {
    tft.print(debug_message + String(" "));
  }

  digitalWrite(TFT_CS, HIGH);  // Deactivate Screen CS
  digitalWrite(SD_CS, LOW);  // Activate SD card CS
}

void cycleTrackballColors() {
  if (TB_INIT) {
    static float hue = 0;
    hue += 0.5;  // Adjust this value to change the speed of the transition
    if (hue >= 360) {
      hue = 0;
    }

    // Convert HSV to RGB
    float s = 1.0, v = 1.0;
    int i = int(hue / 60) % 6;
    float f = (hue / 60) - i;
    float p = v * (1 - s);
    float q = v * (1 - f * s);
    float t = v * (1 - (1 - f) * s);

    uint8_t r, g, b;
    switch (i) {
      case 0:
        r = v * 255;
        g = t * 255;
        b = p * 255;
        break;
      case 1:
        r = q * 255;
        g = v * 255;
        b = p * 255;
        break;
      case 2:
        r = p * 255;
        g = v * 255;
        b = t * 255;
        break;
      case 3:
        r = p * 255;
        g = q * 255;
        b = v * 255;
        break;
      case 4:
        r = t * 255;
        g = p * 255;
        b = v * 255;
        break;
      case 5:
        r = v * 255;
        g = p * 255;
        b = q * 255;
        break;
    }

    trackball.setRGBW(r, g, b, 255);
    delay(10);  // Adjust delay for speed of color change

  } else {
  }
}

void setup() {
  // Initialize Serial for debugging
  Serial.begin(115200);
  while (!Serial) { ; }  // Wait for Serial to be ready
  debug_msg("Serial initialized.");

  // SCREEN BACKLIGHT
  pinMode(TFT_BL, OUTPUT);
  digitalWrite(TFT_BL, HIGH);

  // Screen Setup
  tft.init(240, 320);
  tft.setRotation(3);
  tft.fillScreen(ST77XX_BLACK);
  tft.setCursor(0, 0);
  tft.setTextColor(ST77XX_WHITE);
  tft.setTextWrap(true);
  SCREEN_INIT = true;
  debug_msg("Pico - De Gallo OS - ver 0.0.0");

  //Initialise I2C
  // Wire.begin(I2C_MULTIPLEXER);
  Wire.begin();
  debug_msg("I2C Initialised.");

  // Ensure the SPI pinout the SD card is connected to is configured properly
  SPI.setRX(SD_MISO);
  SPI.setTX(SD_MOSI);
  SPI.setSCK(SD_SCK);

  pinMode(LED_BUILTIN, OUTPUT);

 // Configure SD card detect pin
  pinMode(SD_DETECT, INPUT_PULLUP); 
  // SD card CS pin
  pinMode(SD_CS, OUTPUT);

  digitalWrite(SD_CS, LOW);    // Activate SD card CS
  digitalWrite(TFT_CS, HIGH);  // Deactivate Screen CS
  // digitalWrite(TFT_CS, LOW);  // Activate Screen CS


  // Check if SD card is inserted
  if (digitalRead(SD_DETECT) == LOW) {
    debug_msg("SD card detected.");
    debug_msg("Attempting SD card initialization...");
    digitalWrite(TFT_CS, HIGH);  // Ensure screen CS is high (inactive)
    digitalWrite(SD_CS, LOW);    // Activate SD card CS
    // Attempt to initialize SD card
    if (!SD.begin(SD_CS)) {
      SD_INIT = false;
      debug_msg("SD initialization failed!");
    } else {
      SD_INIT = true;
      debug_msg("SD initialization done.");
    }
    digitalWrite(SD_CS, HIGH);  // Deactivate SD card CS
    digitalWrite(TFT_CS, LOW);  // Activate Screen CS
  } else {
    SD_INIT = false;
    debug_msg("No SD card detected!");
  }

  //Initialise the trackball
  pca_select(1);
  // trackball.begin(I2C_TB);
  trackball.begin();
  if (trackball.isConnected()) {
    TB_INIT = true;
    trackball.setRGBW(255, 255, 255, 255);
    cycleTrackballColors();
    Mouse.begin();
    debug_msg("Trackball initialized.");
  } else {
    TB_INIT = false;
    debug_msg("Trackball initialization failed!");
  }

  // SERIAL ADALOGGER
  // Serial.begin(115200);
  // while (!Serial)
  //   ;
  debug_msg("PiCowbell Adalogger Test");
  pca_select(0);
  // RTC
  if (!rtc.begin()) {
    debug_msg("Can't find RTC!");
    RTC_INIT = false;
    Serial.flush();
    while (1) delay(10);
  } else {
    RTC_INIT = true;
    debug_msg("Found RTC!");
  }

  if (RTC_INIT) {
    if (!rtc.initialized() || rtc.lostPower()) {
      debug_msg("RTC date/time NOT set!");
      // When time needs to be set on a new device, or after a power loss, the
      // following line sets the RTC to the date & time this sketch was compiled
      rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
      debug_msg("RTC date/time is now set!");
      // This line sets the RTC with an explicit date & time, for example to set
      // January 21, 2014 at 3am you would call:
      // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
      //
      // Note: allow 2 seconds after inserting battery or applying external power
      // without battery before calling adjust(). This gives the PCF8523's
      // crystal oscillator time to stabilize. If you call adjust() very quickly
      // after the RTC is powered, lostPower() may still return true.
    }
    // When time needs to be re-set on a previously configured device, the
    // following line sets the RTC to the date & time this sketch was compiled
    // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // This line sets the RTC with an explicit date & time, for example to set
    // January 21, 2014 at 3am you would call:
    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));

    // When the RTC was stopped and stays connected to the battery, it has
    // to be restarted by clearing the STOP bit. Let's do this to ensure
    // the RTC is running.
    rtc.start();

    float drift = 43;                                      // seconds plus or minus over oservation period - set to 0 to cancel previous calibration.
    float period_sec = (7 * 86400);                        // total obsevation period in seconds (86400 = seconds in 1 day:  7 days = (7 * 86400) seconds )
    float deviation_ppm = (drift / period_sec * 1000000);  //  deviation in parts per million (μs)
    float drift_unit = 4.34;                               // use with offset mode PCF8523_TwoHours
    // float drift_unit = 4.069; //For corrections every min the drift_unit is 4.069 ppm (use with offset mode PCF8523_OneMinute)
    int offset = round(deviation_ppm / drift_unit);
    // rtc.calibrate(PCF8523_TwoHours, offset); // Un-comment to perform calibration once drift (seconds) and observation period (seconds) are correct
    // rtc.calibrate(PCF8523_TwoHours, 0); // Un-comment to cancel previous calibration
    debug_msg(String("Offset is ") + String(offset));
  }
}

void loop() {
  if (SD_INIT) {
  } else { debug_msg("SD read/write NOT OK!"); }

  if (TB_INIT) {
    pca_select(1);
    cycleTrackballColors();
    if (trackball.changed()) {
      x = (trackball.right() - trackball.left()) * mouseSpeed;
      y = (trackball.down() - trackball.up()) * mouseSpeed;
      trackball.setRGBW(x + y, x + y, x + y, 128);
      if (x != 0 || y != 0) {
        Mouse.move(x, y, 0);
        tft.setCursor(x, y);
        debug_msg("TB MOVED!");
      }
      if (trackball.click()) {
        Mouse.press(MOUSE_LEFT);
        debug_msg("TB CLICKED!");
        trackball.setRGBW(x + y, x + y, x + y, 128);

      } else if (trackball.release()) {
        if (Mouse.isPressed(MOUSE_LEFT)) {
          Mouse.release(MOUSE_LEFT);
          debug_msg("TB RELEASED!");
          trackball.setRGBW(x + y, x + y, x + y, 128);
        }
      }
    }
  } else {
  }
}
