# 🥗 (Pico) De Gallo. 🥗
# 🍅🔪 + 🧅🔪 + 🌶️🔪 + 🌿🔪 + 🍋‍🟩🤏 = 🥗  
De Gallo is a CP/M and DOS inspired Operating System for the Pico.  

# Boilerplate for Hardware / Build tools
Hardware for BIOS and GIOS
- Processors
  - Pimoroni Pico with 16mb of Flash
    - Info: Main processor
    - Libreq:
      - PicoSDK, Pimoroni Pico
        - https://github.com/raspberrypi/pico-sdk
        - https://github.com/pimoroni/pimoroni-pico
  - Arduino USB Host for Keyboard / Mouse
    - Info: Secondary processor for input devices that communicates with Primary Pico over RS232
    - Libreq: Arduino USB Host
      - https://github.com/arduino-libraries/USBHost
- External Devices
  - Pimoroni ST7789 Display 2
    - Info: Visual graphical display.
    - Libreq:
      - Adafruit ST7789, Pimoroni Display 2
        - https://github.com/adafruit/Adafruit-ST7735-Library
        - https://github.com/pimoroni/pimoroni-pico
  - Adafruit RTC with SD card
    - Info: Real Time Clock and Secure Digital (SD) card.
    - Libreq:
      - Adafruit RTClib, Adafruit BusIO, Arduino SD
        - https://github.com/adafruit/RTClib
        - https://github.com/adafruit/Adafruit_BusIO
        - https://github.com/arduino-libraries/SD
  - Pimoroni trackball
    - Info: Dedicated mouse device.
    - Libreq:
      - pimoroniTrackball
        - https://github.com/ncmreynolds/pimoroniTrackball

Obviously the hardware code should all be implemented in the BIOS and GIOS and none of this should ever touch the BDOS and GDOS.  
For now, a project which gets all hardware talking to each other is needed to collect all required files from Adafruit, Pimoroni, and Arduino.  
Below is some non-working boilerplate code to get started. Later this all can be converted into the BIOS and GIOS for ease of compliation. 

See [DeGallo.cpp](/pico/pico_bdos_gdos/DeGallo.cpp) for working example.  
NO BIOS/GIOS OR BDOS/GDOS YET!!!

# 🍅🔪 + 🧅🔪 + 🌶️🔪 + 🌿🔪 + 🍋‍🟩🤏 = 🥗  
# 🥔🔪 + 🔥 = 🔻🔺🔻  
# 🔻🔺🔻🥗🔻🔺🔻🥗🔻🔺🔻🥗🔻🔺🔻  
