/*
Using 4677_esp-psram64_esp-psram64h_datasheet_en.pdf

The device enters SPI mode on power-up by default, but this can also be switched into QPI mode. 


Table:
                            | SPI Mode (QE=0)                                     | QPI Mode (QE=1)
    Command          | Code | Cmd     | Addr | Wait Cycle | DIO       | MAX Freq. | Cmd | Addr | Wait Cycle | DIO | MAX Freq.
    Read             | 0x03 | S*note1 | S    | 0          | S         | 33        | N/A | N/A  | N/A        | N/A | N/A
    Fast Read        | 0x0B | S       | S    | 8          | S         | 133/144   | N/A | N/A  | N/A        | N/A | N/A
    Fast Read Quad   | 0xEB | S       | Q    | 6          | Q*note1   | 133/144   | Q   | Q    | 6          | Q   | 133/144*note2
    Write            | 0x02 | S       | S    | 0          | S         | 133/144   | Q   | Q    | 0          | Q   | 133/144*note2
    Quad Write       | 0x38 | S       | Q    | 0          | Q         | 133/144   | Q   | Q    | 0          | Q   | 133/144*note2
    Enter Quad Mode  | 0x35 | S       | -    | -          | -         | 133/144   | N/A | N/A  | N/A        | N/A | N/A
    Exit Quad Mode   | 0xF5 | N/A     | N/A  | N/A        | N/A       | N/A       | Q   | -    | -          | -   | 133/144
    Reset Enable     | 0x66 | S       | -    | -          | -         | 133/144   | Q   | -    | -          | -   | 133/144
    Reset            | 0x99 | S       | -    | -          | -         | 133/144   | Q   | -    | -          | -   | 133/144
    Set Burst Length | 0xC0 | S       | -    | -          | -         | 133/144   | Q   | -    | -          | -   | 133/144
    Read ID          | 0x9F | S       | S    | 0          | S         | 133/144   | N/A | N/A  | N/A        | N/A | N/A
    
          1. S=Serial I/O; Q=Quad I/O.
          2. 133/144 MHz max without crossing page boundaries, 84 MHz max when burst commands cross page boundaries.
          3. For ESP-PSRAM64, the maximum frequency is 144 MHz, while for ESP-PSRAM64H it is 133 MHz.


FIG 5-1 :
    In order to terminate ongoing read and write operations and put the chip into standby mode.
    CE# must be pulled high immediately after all read/write operations.
    Not doing so will block internal refresh operations and cause memory failure


FIG 5-2 :
    For a memory controller to correctly latch the last piece of data prior to read-termination,
    it is recommended that a longer CE# hold time (tCHD > tACLK + tCLK) be provided, allowing for a sufficient data window. 


For all reads, data will be available after tACLK following the falling edge of CLK. SPI reads can be done in three ways:
    0x03: Serial CMD, Serial I/O, low frequency,  configurable in linear or burst 32-byte wrap mode.
    0x0B: Serial CMD, Serial I/O, high frequency, configurable in 32/1K-byte burst wrap mode.
    0xEB: Serial CMD, Quad I/O,   high frequency, configurable in 32/1K-byte burst wrap mode.


SPI and QSPI Commands:
    SPI Read Command:                 0x03 (Max frequency: 33 MHz) 
    SPI Fast Read Command:            0x0B (Max frequency: 104 MHz) 
    SPI Fast Quad Read Command:       0xEB (Max frequency: 144 MHz for ESP-PSRAM64, 133 MHz for ESP-PSRAM64H)
    SPI Write Command:                0x02
    SPI Quad Write Command:           0x38
    Quad Mode Enable Command:         0x35 (Available only in SPI mode) 
    SPI Read ID Command:              0x9F (Available only in SPI mode)
      |->  KDG[7:0] Known Good Die:   0101_0101 Fail
                                      0101_1101 Pass
    QPI Fast Read Command:            0xEB (Max frequency: 144 MHz for ESP-PSRAM64, 133 MHz for ESP-PSRAM64H)
    QPI Write Command:                0x02 or 0x38 
    Quad Mode Exit Command:           0xF5 (Available only in QPI mode)


The reset operation is used as a system (software) reset that puts the device in SPI standby mode, 
which is also the default mode after power-up. This operation is based on two commands:
    
    ResetEnable (RSTEN):   0x66
    Reset (RST):           0x99

    
Timing Specifications:
    tCH/tCL (Clock high/low width):                 0.45 * tCLK (minimum)
    tKHKL (Clock rise or fall time):                     1.5 ns (maximum)
    tCSP (CE# setup time to CLK rising edge):            2.5 ns (minimum)
    tCHD (CE# hold time from CLK rising edge):            20 ns (minimum)
    tSP (Setup time to active CLK edge):                   2 ns (minimum)
    tHD (Hold time from active CLK edge):                  2 ns (minimum)
    tACLK (CLK to output delay):                      2 to 6 ns
    tKOH (Data hold time from clock falling edge):       1.5 ns (minimum)
    

Only Linear Burst allows page boundary crossing.
Frequency limits are therefore 133/144 MHz MAX without crossing page boundaries, and 84 MHz MAX when burst commands cross page boundaries.
For ESP-PSRAM64, the maximum frequency is 144 MHz, while for ESP-PSRAM64H, it is 133 MHz.
For operating frequencies > 84 MHz, refer to JEDEC JESD84-B50 for data sampling training.
*/
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/dma.h"
#include "hardware/irq.h"
#include "qspi.pio.h"

// Define hex commands.
#define SPI_READ                       0x03
#define SPI_FAST_READ                  0x0B
#define SPI_FAST_QUAD_READ             0xEB
#define SPI_WRITE                      0x02
#define SPI_QUAD_WRITE                 0x38
#define SPI_READ_ID_KDG_7_0            0x9F
#define SPI_READ_ID_KDG_7_0_FAIL       01010101
#define SPI_READ_ID_KDG_7_0_PASS       01011101
#define QUAD_MODE_ENABLE               0x35
#define QUAD_MODE_EXIT                 0xF5
#define QPI_FAST_READ                  0xEB
#define QPI_WRITE                      0x38
// For QPI_WRITE Using 0x38 instead of 0x02

// Define QSPI pins
#define QSPI_SCK  18
#define QSPI_CS   17
#define QSPI_IO0  16
#define QSPI_IO1  15
#define QSPI_IO2  14
#define QSPI_IO3  13

// Define DMA channels
#define DMA_CHANNEL_TX 0
#define DMA_CHANNEL_RX 1

void dma_complete_handler() {
    dma_hw->ints0 = 1u << DMA_CHANNEL_TX; // Clear interrupt request
    printf("DMA Transfer Complete\n");
}

void setup_dma(uint8_t *buffer, size_t length, bool is_write, uint pio_sm, uint pio_tx_fifo) {
    dma_channel_config c = dma_channel_get_default_config(DMA_CHANNEL_TX);
    channel_config_set_transfer_data_size(&c, DMA_SIZE_8);
    channel_config_set_dreq(&c, pio_get_dreq(pio0, pio_sm, is_write));
    channel_config_set_read_increment(&c, is_write);
    channel_config_set_write_increment(&c, !is_write);

    dma_channel_configure(
        DMA_CHANNEL_TX,
        &c,                                           // DMA Config Channel
        is_write ? &pio0->txf[pio_tx_fifo] : buffer,  // Write address for PIO TX FIFO
        is_write ? buffer : &pio0->rxf[pio_tx_fifo],  // Read address for buffer
        length,                                       // Number of transfers
        false                                         // Don't start yet
    );

    dma_channel_set_irq0_enabled(DMA_CHANNEL_TX, true);
    irq_set_exclusive_handler(DMA_IRQ_0, dma_complete_handler);
    irq_set_enabled(DMA_IRQ_0, true);
}

void write_qspi(PIO pio, uint sm, uint32_t address, uint8_t *data, size_t length) {
  // Need to handle Quad mode change. For now use SPI Quad Write. 
    uint8_t cmd[4] = {0x38, (uint8_t)(address >> 16), (uint8_t)(address >> 8), (uint8_t)address};
    pio_sm_put_blocking(pio, sm, *(uint32_t *)cmd); // Send command and address
    setup_dma(data, length, true, sm, sm);
    dma_start_channel_mask(1u << DMA_CHANNEL_TX);
}

void read_qspi(PIO pio, uint sm, uint32_t address, uint8_t *data, size_t length) {
  // Need to handle Quad mode change. For now use SPI Fast Quad Read. 
    uint8_t cmd[4] = {0xEB, (uint8_t)(address >> 16), (uint8_t)(address >> 8), (uint8_t)address};
    pio_sm_put_blocking(pio, sm, *(uint32_t *)cmd); // Send command and address
    setup_dma(data, length, false, sm, sm);
    dma_start_channel_mask(1u << DMA_CHANNEL_TX);
}

int main() {
    stdio_init_all();

    PIO pio = pio0;
    uint sm = 0;

    // Load the PIO program
    uint offset = pio_add_program(pio, &qspi_program);
    qspi_program_init(pio, sm, offset, QSPI_SCK, QSPI_CS, QSPI_IO0, QSPI_IO1, QSPI_IO2, QSPI_IO3);

    // Test write and read via data block
    uint8_t write_data[256] = {0xAA, 0xBB, 0xCC, 0xDD};
    uint8_t read_data[256];

    while (true) {
        write_qspi(pio, sm, 0x000000, write_data, sizeof(write_data));
        sleep_ms(100); // Delay to ensure write completion
        read_qspi(pio, sm, 0x000000, read_data, sizeof(read_data));
        
        // Print read data for verification
        for (int i = 0; i < sizeof(read_data); i++) {
            printf("%02x ", read_data[i]);
        }
        printf("\n");

        sleep_ms(1000); // Repeat every second
    }

    return 0;
}
