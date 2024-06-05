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
#define I2C_MULTIPLEXER 0x70
#define I2C_RTC 0x68
#define I2C_TB 0x0A

// Real Time Clock
RTC_PCF8523 rtc;

// Pimoroni Display 2 Screen
#define TFT_DC 16
#define TFT_CS 17
#define TFT_SCLK 18
#define TFT_MOSI 19
#define TFT_RST -1
#define TFT_BL 20
Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST);

// Adalogger SD Card Slot
#define SD_DETECT 15
#define SD_MISO 16
#define SD_CS 22
#define SD_SCK 18
#define SD_MOSI 19

File logfile;

// Pimoroni Trackball
uint8_t mouseSpeed = 5;
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
  digitalWrite(SD_CS, HIGH);
  digitalWrite(TFT_CS, LOW);

  Serial.println(debug_message + String(" "));
  if (SCREEN_INIT) {
    tft.print(debug_message + String(" "));
  }

  digitalWrite(TFT_CS, HIGH);
  digitalWrite(SD_CS, LOW);
}

void cycleTrackballColors() {
  if (TB_INIT) {
    static float hue = 0;
    hue += 0.5;
    if (hue >= 360) {
      hue = 0;
    }

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
    delay(10);

  } else {
  }
}

void load_and_execute_application(const char* filename) {
  // Ensure SD card is initialized
  if (!SD_INIT) {
    debug_msg("SD card not initialized.");
    return;
  }

  // Open the application file
  File appFile = SD.open(filename);
  if (!appFile) {
    debug_msg("Failed to open application file.");
    return;
  }

  // Get file size
  size_t fileSize = appFile.size();

  // Allocate memory to load the application
  uint8_t* appBuffer = (uint8_t*)malloc(fileSize);
  if (!appBuffer) {
    debug_msg("Memory allocation failed.");
    appFile.close();
    return;
  }

  // Read the application into memory
  appFile.read(appBuffer, fileSize);
  appFile.close();

  // Function pointer to the application entry point
  typedef void (*app_entry_t)();
  app_entry_t appEntry = (app_entry_t)appBuffer;

  // Deactivate peripherals before jumping to the application
  Serial.end();
  tft.fillScreen(ST77XX_BLACK);
  Mouse.end();

  // Jump to the application entry point
  appEntry();

  // Free the memory allocated for the application
  free(appBuffer);

  // Reinitialize peripherals after application execution (if returning)
  Serial.begin(115200);
  tft.init(240, 320);
  tft.setRotation(3);
  tft.fillScreen(ST77XX_BLACK);
  tft.setCursor(0, 0);
  tft.setTextColor(ST77XX_WHITE);
  tft.setTextWrap(true);
  SCREEN_INIT = true;
  debug_msg("Returned from application.");
}

void setup() {
  // Initialize Serial for debugging
  Serial.begin(115200);
  while (!Serial) { ; }
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

  // Initialize I2C
  Wire.begin();
  debug_msg("I2C Initialised.");

  // Ensure the SPI pinout for the SD card is configured properly
  SPI.setRX(SD_MISO);
  SPI.setTX(SD_MOSI);
  SPI.setSCK(SD_SCK);

  pinMode(LED_BUILTIN, OUTPUT);

  // Configure SD card detect pin
  pinMode(SD_DETECT, INPUT_PULLUP);
  pinMode(SD_CS, OUTPUT);

  digitalWrite(SD_CS, LOW);
  digitalWrite(TFT_CS, HIGH);

  // Check if SD card is inserted
  if (digitalRead(SD_DETECT) == LOW) {
    debug_msg("SD card detected.");
    debug_msg("Attempting SD card initialization...");
    digitalWrite(TFT_CS, HIGH);
    digitalWrite(SD_CS, LOW);
    if (!SD.begin(SD_CS)) {
      SD_INIT = false;
      debug_msg("SD initialization failed!");
    } else {
      SD_INIT = true;
      debug_msg("SD initialization done.");
    }
    digitalWrite(SD_CS, HIGH);
    digitalWrite(TFT_CS, LOW);
  } else {
    SD_INIT = false;
    debug_msg("No SD card detected!");
  }

  // Initialize the trackball
  pca_select(1);
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

  // Initialize RTC
  pca_select(0);
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
      rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
      debug_msg("RTC date/time is now set!");
    }
    rtc.start();

    float drift = 43;
    float period_sec = (7 * 86400);
    float deviation_ppm = (drift / period_sec * 1000000);
    float drift_unit = 4.34;
    int offset = round(deviation_ppm / drift_unit);
    debug_msg(String("Offset is ") + String(offset));
  }
}

void loop() {
  if (SD_INIT) {
    load_and_execute_application("app.bin");
  } else {
    debug_msg("SD read/write NOT OK!");
  }

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
