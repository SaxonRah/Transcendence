# (Pico) De Gallo.
De Gallo is a CP/M and DOS inspired Operating System for the Pico.

# Boilerplate for Hardware / Build tools
Hardware for BIOS and GIOS
- Pimoroni Pico with 16mb of Flash
- Pimoroni ST7789 Display 2
- Adafruit RTC with SD card
- Pimoroni trackball
- Arduino
  - USB Host for Keyboard
  - communicates with Pico over RS232 

Obviously this should all be implemented in the BIOS and GIOS and none of this should ever touch the BDOS and GDOS. For now, a simple project which gets all the hardware talking to each other is needed to find and collect all required source files from Adafruit, Pimoroni, and Arduino. Below is some non-working boilerplate code to get started with the simple project. Later this all can be converted into the BIOS and GIOS.

# Build tools
```CMake
cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)

project(my_os_project)

pico_sdk_init()

add_executable(my_os
    main.c
    st7789.c
    rtc_sd.c
    trackball.c
    rs232.c
)

target_link_libraries(my_os pico_stdlib hardware_spi hardware_i2c hardware_uart hardware_rtc fatfs)

pico_add_extra_outputs(my_os)
```

# Hardware
### st7789.h
```st7789
// st7789.h
#ifndef ST7789_H
#define ST7789_H

void st7789_init();
void st7789_clear();

#endif // ST7789_H
```
### st7789.c
```st7789
// st7789.c
#include "hardware/spi.h"
#include "hardware/gpio.h"
#include "st7789.h"

#define ST7789_SPI_PORT spi0
#define ST7789_PIN_CS 17
#define ST7789_PIN_DC 16
#define ST7789_PIN_RST 18

void st7789_init() {
    // Initialize SPI
    spi_init(ST7789_SPI_PORT, 1000 * 1000);
    gpio_set_function(19, GPIO_FUNC_SPI); // SCK
    gpio_set_function(16, GPIO_FUNC_SPI); // TX

    // Initialize control pins
    gpio_init(ST7789_PIN_CS);
    gpio_set_dir(ST7789_PIN_CS, GPIO_OUT);
    gpio_put(ST7789_PIN_CS, 1);

    gpio_init(ST7789_PIN_DC);
    gpio_set_dir(ST7789_PIN_DC, GPIO_OUT);

    gpio_init(ST7789_PIN_RST);
    gpio_set_dir(ST7789_PIN_RST, GPIO_OUT);

    // Reset the display
    gpio_put(ST7789_PIN_RST, 0);
    sleep_ms(50);
    gpio_put(ST7789_PIN_RST, 1);
    sleep_ms(50);

    // Further initialization commands for ST7789
    // (Refer to the ST7789 datasheet for necessary initialization commands)
}

void st7789_clear() {
    // Clear screen implementation
    // (Send commands to clear the screen)
}
```

### rtc_sd.h
```rtc_sd
// rtc_sd.h
#ifndef RTC_SD_H
#define RTC_SD_H

void rtc_init();
void sd_init();

#endif // RTC_SD_H
```
### rtc_sd.c
```rtc_sd
// rtc_sd.c
#include "hardware/i2c.h"
#include "hardware/spi.h"
#include "rtc_sd.h"

#define I2C_PORT i2c0
#define SD_SPI_PORT spi1
#define SD_CS_PIN 5

void rtc_init() {
    // Initialize I2C for RTC
    i2c_init(I2C_PORT, 100 * 1000);
    gpio_set_function(4, GPIO_FUNC_I2C);
    gpio_set_function(5, GPIO_FUNC_I2C);
    gpio_pull_up(4);
    gpio_pull_up(5);

    // Further RTC initialization (if needed)
}

void sd_init() {
    // Initialize SPI for SD card
    spi_init(SD_SPI_PORT, 1000 * 1000);
    gpio_set_function(2, GPIO_FUNC_SPI);
    gpio_set_function(3, GPIO_FUNC_SPI);
    gpio_set_function(4, GPIO_FUNC_SPI);

    gpio_init(SD_CS_PIN);
    gpio_set_dir(SD_CS_PIN, GPIO_OUT);
    gpio_put(SD_CS_PIN, 1);

    // Further SD card initialization (if needed)
}
```

### trackball.h
```trackball
// trackball.h
#ifndef TRACKBALL_H
#define TRACKBALL_H

void trackball_init();

#endif // TRACKBALL_H
```
### trackball.c
```trackball
// trackball.c
#include "hardware/i2c.h"
#include "trackball.h"

#define TRACKBALL_I2C_PORT i2c1
#define TRACKBALL_ADDR 0x0A

void trackball_init() {
    // Initialize I2C for trackball
    i2c_init(TRACKBALL_I2C_PORT, 100 * 1000);
    gpio_set_function(6, GPIO_FUNC_I2C);
    gpio_set_function(7, GPIO_FUNC_I2C);
    gpio_pull_up(6);
    gpio_pull_up(7);

    // Further trackball initialization (if needed)
}
```
### rs232.h
```rs232
// rs232.h
#ifndef RS232_H
#define RS232_H

void rs232_init();

#endif // RS232_H
```
### rs232.c
```rs232
// rs232.c
#include "hardware/uart.h"
#include "rs232.h"

#define RS232_UART_ID uart1
#define RS232_BAUD_RATE 9600
#define RS232_TX_PIN 8
#define RS232_RX_PIN 9

void rs232_init() {
    // Initialize UART for RS232
    uart_init(RS232_UART_ID, RS232_BAUD_RATE);
    gpio_set_function(RS232_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(RS232_RX_PIN, GPIO_FUNC_UART);

    // Further UART configuration (if needed)
}
```
### Pico Simple Project main.c
```main
// main.c
#include "pico/stdlib.h"
#include "st7789.h"
#include "rtc_sd.h"
#include "trackball.h"
#include "rs232.h"

int main() {
    stdio_init_all();

    // Initialize peripherals
    st7789_init();
    rtc_init();
    sd_init();
    trackball_init();
    rs232_init();

    // Main loop
    while (true) {
        // Update display, read from trackball, communicate via RS232, etc.
        // Example: Clear the display
        st7789_clear();

        sleep_ms(1000); // Simple delay for demonstration
    }

    return 0;
}
```

### Arduino USB Host main.c
```Arduino USB Host
#include <hidboot.h>
#include <usbhub.h>
#include <SPI.h>

// USB host objects
USB     Usb;
HIDBoot<USB_HID_PROTOCOL_KEYBOARD>    Keyboard(&Usb);

class KbdRptParser : public KeyboardReportParser {
  void PrintKey(uint8_t mod, uint8_t key);

protected:
  void OnKeyDown(uint8_t mod, uint8_t key);
  void OnKeyPressed(uint8_t key);
};

KbdRptParser Prs;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600); // Assuming Serial1 is used for RS232 communication
  while (!Serial); // Wait for serial monitor to open

  if (Usb.Init() == -1) {
    Serial.println("USB Host Shield initialization failed");
    while (1); // Halt
  }
  Serial.println("USB Host Shield initialized");

  Keyboard.SetReportParser(0, (HIDReportParser*)&Prs);
}

void loop() {
  Usb.Task();
}

void KbdRptParser::OnKeyDown(uint8_t mod, uint8_t key) {
  uint8_t c = OemToAscii(mod, key);

  if (c) {
    OnKeyPressed(c);
  }
}

void KbdRptParser::OnKeyPressed(uint8_t key) {
  Serial.print("Key Pressed: ");
  Serial.println((char)key);
  Serial1.write((char)key); // Send key to Pico over RS232
}

void KbdRptParser::PrintKey(uint8_t mod, uint8_t key) {
  MODIFIERKEYS modKeys;
  *((uint8_t*)&modKeys) = mod;
  Serial.print((modKeys.bmLeftCtrl   == 1) ? "C" : " ");
  Serial.print((modKeys.bmLeftShift  == 1) ? "S" : " ");
  Serial.print((modKeys.bmLeftAlt    == 1) ? "A" : " ");
  Serial.print((modKeys.bmLeftGUI    == 1) ? "G" : " ");

  Serial.print(" > ");
  Serial.print(key, DEC);
  Serial.print(" ");
  Serial.print((char)key);
  Serial.println(" ");
}
```
