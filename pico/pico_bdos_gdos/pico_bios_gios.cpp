/*
The entire idea of this is that you could rewrite the bios/gios and have Pico BDOS/GDOS work on any hardware.
GIOS of GSX is combined into the BIOS for simplicity.

BIOS (Basic Input/Output System):
    Handles low-level, hardware-specific system operations.
    This includes directly interfacing with the console, disk drives, and other system hardware peripherals.

GIOS (Graphics Input/Output System):
    Handles low-level, hardware-specific graphical operations.
    This includes directly interfacing with the display, plotter, printer and other graphical hardware peripherals.


Nothing in BIOS should ever be called from main.
Nothing in GIOS should ever be called from main.
*/

#include <stdio.h>
#include <string.h>

#include <Adafruit_ST7789.h>
#include <SPI.h>

#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "hardware/uart.h"

#include "ff.h" // FatFs library for file operations

// File System
// SPI pins for SD card
#define SPI_PORT spi0
#define PIN_MISO 16
#define PIN_CS 17
#define PIN_SCK 18
#define PIN_MOSI 19

FATFS file_system;      // Filesystem object
FIL file_object;        // File object
UINT file_read_count;   // File read count
UINT file_write_count;  // File write count
void* dma_address;      // DMA address

// Display
// SPI pins for TFT
#define TFT_DC 16
#define TFT_CS 17
#define TFT_SCLK 18
#define TFT_MOSI 19
#define TFT_RST -1
#define BL_EN 20

Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST);

//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

// Cold boot
void bios_cold_boot() {
    // Initializes the system and loads the CCP and BDOS from disk.
    printf("Cold Boot\n");
}

// Warm boot
void bios_warm_boot() {
    // Typically restarts the CP/M system without reloading BIOS
    printf("Warm Boot\n");
}

// Console status
void bios_console_status() {
    // Returns 0xFF if a character is ready, 0x00 otherwise
    int ready = uart_is_readable(uart0) ? 0xFF : 0x00;
    return ready;
}

// Console input
char bios_console_input() {
    // Waits for a character to be typed on the console
    while (!uart_is_readable(uart0));
    char c = uart_getc(uart0);
    return c;
}

// Console output
int bios_console_output(char c) {
    // Outputs a character to the console
    uart_putc(uart0, c);
    return 0;
}

// List output (typically same as console output)
int bios_list_output(char c) {
    bios_console_output(c);
    return 0;
}

// Punch output (typically not used, here for completeness)
int bios_punch_output(char c) {
    // Could be used to output to a serial port or file
    return 0;
}

// Reader input (typically not used, here for completeness)
int bios_reader_input() {
    // Could be used to input from a serial port or file
    return 0;
}

// Home the disk system
int bios_home_disk() {
    // Resets the disk system, typically setting the current drive to A:
    f_mount(&file_system, "", 0);  // Mount the filesystem
    return 0;
}

int bios_select_disk(int drive) {
    // Select disk drive
    // Selects the specified drive (0 = A:, 1 = B:, etc.)
    return drive;
}

// Set the current track
int bios_set_track(int track) {
    // Sets the current track for disk I/O
    return track;
}

// Set the current sector
int bios_set_sector(int sector) {
    // Sets the current sector for disk I/O
    // Sector setting can be done using the FatFs library's seek functionality
    return sector;
}

// Set the DMA address
int bios_set_dma(void* dma) {
    // Sets the address where disk data will be read/written
    dma_address = dma;
}

// Read a sector from the disk
int bios_read_sector() {
    // Reads the current sector into the DMA address

    // Implement reading a sector using the FatFs library
    // This is simplified and assumes a single sector read
    f_read(&file_object, dma_address, 512, &file_read_count);
    return (file_read_count == 512) ? 0 : -1;
}

// Write a sector to the disk
int bios_write_sector() {
    // Writes the current sector from the DMA address

    // Implement writing a sector using the FatFs library
    // This is simplified and assumes a single sector write
    f_write(&file_object, dma_address, 512, &file_write_count);
    return (bw == 512) ? 0 : -1;
}

// List status
int bios_list_status() {
    // Returns the status of the list device
    // Typically the same as the console status
    return 0;
}

// Sector translate
int bios_sector_translate() {
    // Translates logical to physical sector numbers
    // Typically used for different disk formats
    return 0;
}

// Open File
int bios_open_file(char* filename) {
    FRESULT res = f_open(&file_object, filename, FA_READ | FA_WRITE);
    return (res == FR_OK) ? 0 : -1;
}

// Close File
int bios_close_file(int file_handle) {
    FRESULT res = f_close(&file_object);
    return (res == FR_OK) ? 0 : -1;
}

// Delete File
int bios_delete_file(char* filename) {
    FRESULT res = f_unlink(filename);
    return (res == FR_OK) ? 0 : -1;
}

// Read File
int bios_read_file(int file_handle) {
    FRESULT res = f_read(&file_object, dma_address, 512, &file_read_count);
    return (res == FR_OK) ? file_read_count : -1;
}

// Write File
int bios_write_file(int file_handle) {
    FRESULT res = f_write(&file_object, dma_address, 512, &file_write_count);
    return (res == FR_OK) ? bw : -1;
}

// Make File
int bios_make_file(char* filename) {
    FRESULT res = f_open(&file_object, filename, FA_CREATE_NEW | FA_WRITE);
    return (res == FR_OK) ? 0 : -1;
}

// Rename File
int bios_rename_file(char* old_name, char* new_name) {
    FRESULT res = f_rename(old_name, new_name);
    return (res == FR_OK) ? 0 : -1;
}

//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

void bios_diskio_init() {
    // Initialize SPI for SD card
    spi_init(SPI_PORT, 500 * 1000);
    gpio_set_function(PIN_MISO, GPIO_FUNC_SPI);
    gpio_set_function(PIN_CS, GPIO_FUNC_SPI);
    gpio_set_function(PIN_SCK, GPIO_FUNC_SPI);
    gpio_set_function(PIN_MOSI, GPIO_FUNC_SPI);
    gpio_pull_up(PIN_MISO);
    gpio_pull_up(PIN_CS);
    gpio_pull_up(PIN_SCK);
    gpio_pull_up(PIN_MOSI);

    // Additional SD card initialization here
}

void bios_diskio_read(uint32_t sector, uint8_t* buffer) {
    // Implement sector read from SD card
}

void bios_diskio_write(uint32_t sector, const uint8_t* buffer) {
    // Implement sector write to SD card
}

//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

// Initialize the display
void gios_init_display() {
    pinMode(BL_EN, OUTPUT);
    digitalWrite(BL_EN, HIGH);
    tft.init(240, 320);
    tft.setRotation(3);
    bios_clear_display(ST77XX_BLACK);
    bios_print_text(true, 0, 0, "Display Initialized", ST77XX_WHITE);
}

// Clear the display
void gios_clear_display(uint16_t color) {
  // tft.fillScreen(ST77XX_BLACK);
  tft.fillScreen(color);
}

// Draw a pixel
void gios_draw_pixel(int x, int y, uint16_t color) {
    tft.drawPixel(x, y, color);
}

// Draw a line
void gios_draw_line(int x0, int y0, int x1, int y1, uint16_t color) {
    tft.drawLine(x0, y0, x1, y1, color);
}

// Print text
void gios_print_text(bool text_wrap, int x, int y, const char* text, uint16_t color) {
    tft.setTextWrap(text_wrap);
    tft.setCursor(x, y);
    tft.setTextColor(color);
    tft.print(text);
}