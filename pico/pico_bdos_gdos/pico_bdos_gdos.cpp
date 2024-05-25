/*
The entire idea of this is that you don't need to rewrite Pico BDOS to have Pico BDOS work on any hardware.
GDOS of GSX is combined into the BDOS for simplicity.

BDOS (Basic Disk Operating System):
    Provides higher-level, system-wide services.
    For example file management, console I/O, and system calls that applications use.
GDOS (Graphics Device Operating System):
    Provides higher-level, system-wide services.
    For example graphical management and graphical calls that applications use.


BDOS should call hardware BIOS functions. Main will call BDOS functions.
GDOS should call hardware GIOS functions. Main will call GDOS functions.
*/
#include "pico_bios_gios.cpp"

//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

// Cold boot
void bdos_cold_boot() {
    bios_cold_boot()
}

// Warm Boot
void bdos_warm_boot() {
    bios_warm_boot()
}

// Console Status
int bdos_console_status() {
    return bios_console_status();
}

// Console Input
char bdos_console_input() {
    return bios_console_input();
}

// Console Output
int bdos_console_output(char c) {
    return bios_console_output(c);
}

// Console List Output
int bdos_list_output(char c) {
    return bios_list_output(c);
}

// Punch output
int bdos_punch_output(char c) {
    return bios_punch_output(c);
}

// Reader input
int bdos_reader_input() {
    return bios_reader_input()
}

// Home Disk
int bdos_home_disk() {
    return bios_home_disk();
}

// Select Disk
int bdos_select_disk(int drive) {
    // Support multiple drives by initializing the filesystem for each drive
    // Assume a single drive is always selected for now.
    return bios_select_disk(drive);
}

// Set Track
int bdos_set_track(int track) {
    // Track setting is not typically needed in modern SD card interfaces
    // but can be implemented if using a more complex disk system and disk image format.
    return bios_set_track(track);
}

// Set Sector
int bdos_set_sector(int sector) {
   return bios_set_sector(sector);
}

// Set DMA Address
int bdos_set_dma(void* dma) {
    return bios_set_dma(dma);
}

// Read Sector
int bdos_read_sector() {
    return bios_read_sector();
}

// Write Sector
int bdos_write_sector() {
    return bios_write_sector();
}

// List status
int bdos_list_status() {
    return bios_list_status();
}

// Sector translate
int bdos_sector_translate() {
    return bios_sector_translate();
}

// Open File
int bdos_open_file(char* filename) {
    return bios_open_file(filename);
}

// Close File
int bdos_close_file(int file_handle) {
    return bios_close_file(file_handle);
}

// Delete File
int bdos_delete_file(char* filename) {
    return bios_delete_file(filename);
}

// Read File
int bdos_read_file(int file_handle) {
    return bios_read_file(file_handle);
}

// Write File
int bdos_write_file(int file_handle) {
    return bios_write_file(file_handle);
}

// Make File
int bdos_make_file(char* filename) {
    return bios_make_file(file_handle);
}

// Rename File
int bdos_rename_file(char* old_name, char* new_name) {
    return bios_rename_file(old_name, new_name);
}

void bdos_diskio_init() {
    bios_diskio_init();
}

void bdos_diskio_read(uint32_t sector, uint8_t* buffer) {
    bios_diskio_read(sector, buffer);
}

void bdos_diskio_write(uint32_t sector, const uint8_t* buffer) {
    bios_diskio_write(sector, buffer);
}

//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

// Initialize the display
void gdos_init_display() {
    gios_init_display();
}

// Clear the display
void gdos_clear_display() {
    gios_clear_display();
}

// Draw a pixel
void gdos_draw_pixel(int x, int y, int color) {
    gios_draw_pixel(x, y, (uint16_t)color);
}

// Draw a line
void gdos_draw_line(int x0, int y0, int x1, int y1, int color) {
    gios_draw_line(x0, y0, x1, y1, (uint16_t)color);
}

// Print text
void gdos_print_text(int x, int y, const char* text, int color) {
    gios_print_text(x, y, text, (uint16_t)color);
}

//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

int fetch_system_call() {
    // Fetch the system call number
    // This is a placeholder and needs to be implemented according to your system
    return 0;
}

int fetch_system_call_argument() {
    // Fetch the system call argument
    // This is a placeholder and needs to be implemented according to your system
    return 0;
}

int fetch_next_arg() {
    // Fetch the next argument for multi-argument system calls
    // This is a placeholder and needs to be implemented according to your system
    return 0;
}

int bdos_gdos(int function, int arg) {
    switch (function) {
        case 1: // Console Input
            return bdos_console_input();

        case 2: // Console Output
            bdos_console_output(arg);
            break;

        case 6: // Direct Console I/O
            return (arg == 0xFF) ? bdos_console_status() : bdos_console_output(arg);

        case 12: // Return Version Number
            // CP/M version 2.2
            return 0x22;

        case 13: // Reset Disk System
            return bdos_home_disk();

        case 14: // Select Disk
            return bdos_select_disk(arg);

        case 15: // Open File
            return bdos_open_file((char*)dma_address);

        case 16: // Close File
            return bdos_close_file(arg);

        case 19: // Delete File
            return bdos_delete_file((char*)dma_address);

        case 20: // Read Sequential
            return bdos_read_file(arg);

        case 21: // Write Sequential
            return bdos_write_file(arg);

        case 22: // Make File
            return bdos_make_file((char*)dma_address);

        case 23: // Rename File
            return bdos_rename_file((char*)dma_address, (char*)dma_address + 11);

        case 24: // Initialize Display
            gdos_init_display();
            break;

        case 25: // Clear Display
            int color = fetch_next_arg();
            gdos_clear_display(color);
            break;

        case 26: // Draw Pixel
            {
                int x = (arg >> 16) & 0xFFFF;
                int y = arg & 0xFFFF;
                int color = fetch_next_arg();
                gdos_draw_pixel(x, y, color);
            }
            break;

        case 27: // Draw Line
            {
                int x0 = (arg >> 16) & 0xFFFF;
                int y0 = arg & 0xFFFF;
                int x1 = fetch_next_arg();
                int y1 = fetch_next_arg();
                int color = fetch_next_arg();
                gdos_draw_line(x0, y0, x1, y1, color);
            }
            break;

        case 28: // Print Text
            {
                int x = (arg >> 16) & 0xFFFF;
                int y = arg & 0xFFFF;
                char* text = (char*)fetch_next_arg();
                int color = fetch_next_arg();
                bool text_wrap = fetch_next_arg();
                gdos_print_text(x, y, text, color, text_wrap);
            }
            break;

        default:
            printf("Unknown BDOS/GDOS function: %d\n", function);
            break;
    }
    return 0;
}

//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------

// CP/M and DOS Main Entry
// BIOS <- BDOS <- Main
// Main will use BDOS. BDOS will use BIOS.
// GIOS <- GDOS <- Main
// Main will use GDOS. GDOS will use GIOS.
// Main and Applications should never use BIOS or GIOS functions directly.

int main() {
    stdio_init_all();
    uart_init(uart0, 115200);
    gpio_set_function(0, GPIO_FUNC_UART);
    gpio_set_function(1, GPIO_FUNC_UART);

    // Initialize hardware
    bdos_diskio_init();
    gdos_init_display();

    // Initialize the CP/M system
    bdos_cold_boot();
    // bdos_warm_boot();
    while (true) {
        // Fetch the next CP/M system call
        int function = fetch_system_call();
        int arg = fetch_system_call_argument();

        // Call the BDOS function
        bdos_gdos(function, arg);
    }

    return 0;
}
