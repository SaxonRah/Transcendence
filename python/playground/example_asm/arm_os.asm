;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;ARMOS - Baseline OS
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.syntax unified
.thumb

.equ STACK_SIZE, 512    ; Define stack size

.section .text
.global _start
.type _start, %function
_start:
    ; Initialize stack pointer
    ldr r0, =__stack_end__
    mov sp, r0

    ; Call initialization routine
    bl init

    ; Enter main loop
main_loop:
    bl prompt_input    ; Display prompt and get user input
    bl process_input   ; Process user input
    b main_loop        ; Repeat main loop

prompt_input:
    ; Print prompt
    ldr r0, =prompt_message
    bl print_string
    ; Receive input from user
    ldr r0, =input_buffer
    bl receive_input
    bx lr

process_input:
    ; Check for commands
    ldr r0, =input_buffer
    ldrb r1, [r0]   ; Load the first character of the input
    cmp r1, #'h'    ; Compare it with the 'h' command
    beq display_help  ; If equal, display help
    cmp r1, #'q'    ; Compare it with the 'q' command
    beq quit         ; If equal, quit the program
    bl print_string  ; Otherwise, print unknown command
    ldr r0, =unknown_command_message
    bl print_string
    bx lr

display_help:
    ; Print help message
    ldr r0, =help_message
    bl print_string
    bx lr

quit:
    ; Quit the program
    movs r0, #0x00  ; Exit code 0
    ldr r7, =__exit
    bx r7

print_string:
    ; Print the null-terminated string pointed to by r0
print_string_loop:
    ldrb r1, [r0], #1   ; Load the byte and increment the pointer
    cmp r1, #0          ; Check if it's the null terminator
    beq print_string_done  ; If yes, exit the loop
    bl putchar          ; Print the character
    b print_string_loop
print_string_done:
    bx lr

receive_input:
    ; Receive input from the user and store it in the buffer pointed to by r0
    movs r1, #0          ; Initialize input length to 0
receive_input_loop:
    bl getchar           ; Get a character from input
    strb r0, [r0, r1]    ; Store the character in the buffer
    adds r1, r1, #1      ; Increment input length
    cmp r0, #'\n'        ; Check if it's a newline character
    bne receive_input_loop  ; If not, continue receiving
    bx lr

getchar:
    ; Get a character from input
    movs r0, #0          ; Initialize character to 0
    ldr r7, =0x40007000  ; UART0 base address
    ldrb r0, [r7, #0x18] ; Read the receive buffer
    bx lr

putchar:
    ; Print a character
    ldr r7, =0x40007000  ; UART0 base address
    strb r0, [r7, #0x00] ; Write the character to the transmit buffer
    bx lr

.section .data
prompt_message:     .asciz "ARMOS> "
unknown_command_message:   .asciz "Unknown command.\n"
help_message:       .asciz "Available commands:\n  h - Display this help message\n  q - Quit\n"

.section .bss
input_buffer:   .space 32

.section .heap
    .align 2
__stack_end__:
    .space STACK_SIZE

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;ARMOS - DIRECTORY HANDLING
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.syntax unified
.thumb

.equ STACK_SIZE, 512    ; Define stack size
.equ MAX_FILES, 10      ; Maximum number of files

.section .text
.global _start
.type _start, %function
_start:
    ; Initialize stack pointer
    ldr r0, =__stack_end__
    mov sp, r0

    ; Initialize file system
    bl init_file_system

    ; Call initialization routine
    bl init

    ; Enter main loop
main_loop:
    bl prompt_input    ; Display prompt and get user input
    bl process_input   ; Process user input
    b main_loop        ; Repeat main loop

prompt_input:
    ; Print prompt
    ldr r0, =prompt_message
    bl print_string
    ; Receive input from user
    ldr r0, =input_buffer
    bl receive_input
    bx lr

process_input:
    ; Check for commands
    ldr r0, =input_buffer
    ldrb r1, [r0]   ; Load the first character of the input
    cmp r1, #'h'    ; Compare it with the 'h' command
    beq display_help  ; If equal, display help
    cmp r1, #'q'    ; Compare it with the 'q' command
    beq quit         ; If equal, quit the program
    cmp r1, #'d'    ; Compare it with the 'd' command
    beq display_directory   ; If equal, display directory
    bl print_string  ; Otherwise, print unknown command
    ldr r0, =unknown_command_message
    bl print_string
    bx lr

display_help:
    ; Print help message
    ldr r0, =help_message
    bl print_string
    bx lr

quit:
    ; Quit the program
    movs r0, #0x00  ; Exit code 0
    ldr r7, =__exit
    bx r7

display_directory:
    ; Display directory listing
    ldr r0, =directory_message
    bl print_string
    ; Iterate through file system
    mov r2, #0
display_directory_loop:
    cmp r2, MAX_FILES
    bge display_directory_done
    ldr r0, =file_system
    ldr r1, [r0, r2, lsl #2]   ; Load file entry
    cmp r1, #0                  ; Check if entry is empty
    beq display_directory_next
    bl print_string
    mov r0, r1
    bl print_string
display_directory_next:
    adds r2, r2, #1
    b display_directory_loop
display_directory_done:
    bx lr

init_file_system:
    ; Initialize file system with empty entries
    mov r0, #0
    mov r1, #MAX_FILES
init_file_system_loop:
    str r0, [file_system, r1, lsl #2]  ; Set entry to 0 (empty)
    subs r1, r1, #1
    bne init_file_system_loop
    bx lr

print_string:
    ; Print the null-terminated string pointed to by r0
print_string_loop:
    ldrb r1, [r0], #1   ; Load the byte and increment the pointer
    cmp r1, #0          ; Check if it's the null terminator
    beq print_string_done  ; If yes, exit the loop
    bl putchar          ; Print the character
    b print_string_loop
print_string_done:
    bx lr

receive_input:
    ; Receive input from the user and store it in the buffer pointed to by r0
    movs r1, #0          ; Initialize input length to 0
receive_input_loop:
    bl getchar           ; Get a character from input
    strb r0, [r0, r1]    ; Store the character in the buffer
    adds r1, r1, #1      ; Increment input length
    cmp r0, #'\n'        ; Check if it's a newline character
    bne receive_input_loop  ; If not, continue receiving
    bx lr

getchar:
    ; Get a character from input
    movs r0, #0          ; Initialize character to 0
    ldr r7, =0x40007000  ; UART0 base address
    ldrb r0, [r7, #0x18] ; Read the receive buffer
    bx lr

putchar:
    ; Print a character
    ldr r7, =0x40007000  ; UART0 base address
    strb r0, [r7, #0x00] ; Write the character to the transmit buffer
    bx lr

.section .data
prompt_message:     .asciz "ARMOS> "
unknown_command_message:   .asciz "Unknown command.\n"
help_message:       .asciz "Available commands:\n  h - Display this help message\n  q - Quit\n  d - Display directory\n"
directory_message:  .asciz "Directory Listing:\n"

.section .bss
input_buffer:   .space 32
file_system:    .space MAX_FILES * 4

.section .heap
    .align 2
__stack_end__:
    .space STACK_SIZE
    
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;ARMOS - DIRECTORY Interrupt
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.syntax unified
.thumb

.equ STACK_SIZE, 512    ; Define stack size
.equ MAX_FILES, 10      ; Maximum number of files

.section .text
.global _start
.type _start, %function
_start:
    ; Initialize stack pointer
    ldr r0, =__stack_end__
    mov sp, r0

    ; Initialize file system
    bl init_file_system

    ; Initialize interrupts
    bl init_interrupts

    ; Call initialization routine
    bl init

    ; Enable interrupts
    cpsie i

    ; Enter main loop
main_loop:
    bl prompt_input    ; Display prompt and get user input
    bl process_input   ; Process user input
    b main_loop        ; Repeat main loop

prompt_input:
    ; Print prompt
    ldr r0, =prompt_message
    bl print_string
    ; Receive input from user
    ldr r0, =input_buffer
    bl receive_input
    bx lr

process_input:
    ; Check for commands
    ldr r0, =input_buffer
    ldrb r1, [r0]   ; Load the first character of the input
    cmp r1, #'h'    ; Compare it with the 'h' command
    beq display_help  ; If equal, display help
    cmp r1, #'q'    ; Compare it with the 'q' command
    beq quit         ; If equal, quit the program
    cmp r1, #'d'    ; Compare it with the 'd' command
    beq display_directory   ; If equal, display directory
    bl print_string  ; Otherwise, print unknown command
    ldr r0, =unknown_command_message
    bl print_string
    bx lr

display_help:
    ; Print help message
    ldr r0, =help_message
    bl print_string
    bx lr

quit:
    ; Quit the program
    movs r0, #0x00  ; Exit code 0
    ldr r7, =__exit
    bx r7

display_directory:
    ; Display directory listing
    ldr r0, =directory_message
    bl print_string
    ; Iterate through file system
    mov r2, #0
display_directory_loop:
    cmp r2, MAX_FILES
    bge display_directory_done
    ldr r0, =file_system
    ldr r1, [r0, r2, lsl #2]   ; Load file entry
    cmp r1, #0                  ; Check if entry is empty
    beq display_directory_next
    bl print_string
    mov r0, r1
    bl print_string
display_directory_next:
    adds r2, r2, #1
    b display_directory_loop
display_directory_done:
    bx lr

init_file_system:
    ; Initialize file system with empty entries
    mov r0, #0
    mov r1, #MAX_FILES
init_file_system_loop:
    str r0, [file_system, r1, lsl #2]  ; Set entry to 0 (empty)
    subs r1, r1, #1
    bne init_file_system_loop
    bx lr

print_string:
    ; Print the null-terminated string pointed to by r0
print_string_loop:
    ldrb r1, [r0], #1   ; Load the byte and increment the pointer
    cmp r1, #0          ; Check if it's the null terminator
    beq print_string_done  ; If yes, exit the loop
    bl putchar          ; Print the character
    b print_string_loop
print_string_done:
    bx lr

receive_input:
    ; Receive input from the user and store it in the buffer pointed to by r0
    movs r1, #0          ; Initialize input length to 0
receive_input_loop:
    bl getchar           ; Get a character from input
    strb r0, [r0, r1]    ; Store the character in the buffer
    adds r1, r1, #1      ; Increment input length
    cmp r0, #'\n'        ; Check if it's a newline character
    bne receive_input_loop  ; If not, continue receiving
    bx lr

getchar:
    ; Get a character from input
    movs r0, #0          ; Initialize character to 0
    ldr r7, =0x40007000  ; UART0 base address
    ldrb r0, [r7, #0x18] ; Read the receive buffer
    bx lr

putchar:
    ; Print a character
    ldr r7, =0x40007000  ; UART0 base address
    strb r0, [r7, #0x00] ; Write the character to the transmit buffer
    bx lr

init_interrupts:
    ; Set up UART0 interrupt
    ldr r0, =0xE000E100  ; Address of Interrupt Set-Enable Register (ISER0)
    ldr r1, =1           ; Bit 0 corresponds to UART0
    str r1, [r0]

    ; Set the interrupt vector
    ldr r0, =uart_isr
    ldr r1, =0x00000018  ; UART0 interrupt vector (number 24)
    lsl r1, r1, #2       ; Multiply the vector number by 4 (each vector is 4 bytes)
    ldr r2, =0x00000020  ; Address of the interrupt vector table
    add r1, r1, r2       ; Add the offset to the base address
    str r0, [r1]         ; Store the ISR address in the vector table
    bx lr

uart_isr:
    ; UART interrupt service routine
    bl getchar     ; Handle input
    bx lr

.section .data
prompt_message:     .asciz "ARMOS> "
unknown_command_message:   .asciz "Unknown command.\n"
help_message:       .asciz "Available commands:\n  h - Display this help message\n  q - Quit\n  d - Display directory\n"
directory_message:  .asciz "Directory Listing:\n"

.section .bss
input_buffer:   .space 32
file_system:    .space MAX_FILES * 4

.section .heap
    .align 2
__stack_end__:
    .space STACK_SIZE

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;ARMOS -  QSPI RAM
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.equ QSPI_BASE_ADDR, 0x60000000    ; Base address of the QSPI peripheral
.equ QSPI_COMMAND_REG, QSPI_BASE_ADDR + 0x140    ; QSPI Command register address
.equ QSPI_DATA_REG, QSPI_BASE_ADDR + 0x144       ; QSPI Data register address

init_qspi:
    ldr r1, =0x40043054          ; Load alternate function register 1 address
    ldr r2, =0x60                ; Set GPIOB pin 0 and 1 to alternate function 6 (QSPI)
    str r2, [r1]

    ldr r1, =0x40043100          ; Load RCC_AHB3ENR register address
    ldr r2, [r1]                 ; Read RCC_AHB3ENR
    orr r2, r2, #0x1             ; Enable QSPI clock
    str r2, [r1]                 ; Write RCC_AHB3ENR

    ldr r1, =0x4000300C          ; Load SYSCFG memory remap register address
    ldr r2, =0x01                ; Remap memory to QSPI
    str r2, [r1]                 ; Write SYSCFG memory remap register

    ldr r1, =QSPI_BASE_ADDR + 0x00    ; Load QSPI Control register address
    ldr r2, =0x8                 ; Enable QSPI memory mapped mode
    str r2, [r1]                 ; Write to QSPI Control register

    bx lr

read_qspi_memory:
    ldr r1, =QSPI_COMMAND_REG   ; Load QSPI Command register address
    ldr r2, =0x3                ; Set read command (0x03)
    str r2, [r1]                ; Write command to QSPI Command register

    ldr r1, =QSPI_DATA_REG      ; Load QSPI Data register address
    ldr r2, [r0]                ; Load address to read from
    str r2, [r1]                ; Write address to QSPI Data register

    ldr r1, [r1]                ; Read data from QSPI Data register
    mov r0, r1                  ; Return the read data
    bx lr

write_qspi:
    ; Write data to QSPI memory
    ; Assume that r0 contains the address of the data to write
    ; Assume that r1 contains the length of data to write

    mov r2, #0                  ; Initialize index
write_qspi_loop:
    cmp r2, r1                  ; Compare index with length
    bge write_qspi_done         ; If index >= length, exit loop

    ldrb r3, [r0, r2]          ; Load byte from data buffer
    ; Perform QSPI write operation for the byte in r3
    ; Add your QSPI write operation code here

    adds r2, r2, #1             ; Increment index
    b write_qspi_loop           ; Repeat loop

write_qspi_done:
    bx lr

init_interrupts:
    ; Set up UART0 interrupt
    ldr r0, =0xE000E100  ; Address of Interrupt Set-Enable Register (ISER0)
    ldr r1, =1           ; Bit 0 corresponds to UART0
    str r1, [r0]

    ; Set up QSPI interrupt
    ldr r0, =0xE000E100  ; Address of Interrupt Set-Enable Register (ISER0)
    ldr r1, =1 << 1      ; Bit 1 corresponds to QSPI
    str r1, [r0]

    ; Set the interrupt vector for QSPI
    ldr r0, =qspi_isr
    ldr r1, =0x00000020  ; QSPI interrupt vector (number 32)
    lsl r1, r1, #2       ; Multiply the vector number by 4 (each vector is 4 bytes)
    ldr r2, =0x00000020  ; Address of the interrupt vector table
    add r1, r1, r2       ; Add the offset to the base address
    str r0, [r1]         ; Store the ISR address in the vector table

qspi_isr:
    ; QSPI interrupt service routine
    ; Check the source of the interrupt
    ldr r0, =QSPI_BASE_ADDRESS  ; Load the base address of the QSPI peripheral
    ldr r1, [r0, #QSPI_SR_OFFSET]  ; Load the status register

    ; Check if the interrupt was triggered by a read or write operation completion
    tst r1, #QSPI_SR_TCF  ; Test Transfer Complete Flag
    bne transfer_complete   ; If TCF is set, transfer is complete

    ; Handle other QSPI interrupts here if needed

    bx lr

transfer_complete:
    ; Clear the Transfer Complete Flag by writing 1 to it
    str r1, [r0, #QSPI_SR_OFFSET]

    ; Handle transfer completion
    ; Add your transfer completion handling code here

    bx lr

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;ARMOS - SD CARD
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; Constants
.equ SPI_BASE_ADDRESS, 0x40008000   ; Example SPI peripheral base address
.equ SD_CS_PIN, 0x01                 ; Example chip select pin for SD card

.section .text
.global sd_init
.type sd_init, %function
sd_init:
    ; Initialize SPI peripheral for communication with SD card
    ; Configure SPI pins, clock, and other settings
    ; Configure SPI to operate in SPI mode for SD card communication
    ; Initialize SD card by sending initialization commands (CMD0, CMD8, ACMD41, CMD58, etc.)
    ; Check for successful initialization
    ; Set up SD card for data transfer (set block size, enable CRC, etc.)
    ; Return status indicating success or failure

.global sd_read_block
.type sd_read_block, %function
sd_read_block:
    ; Read a block of data from SD card
    ; Input:
    ;   r0 - Pointer to buffer to store read data
    ;   r1 - Block number to read
    ; Output:
    ;   Data read from SD card stored in the buffer pointed to by r0
    ; Select SD card (assert CS pin)
    ; Send read command (CMD17) with block address
    ; Wait for response (R1 response indicating success)
    ; Read data block from SD card
    ; Deselect SD card (deassert CS pin)
    ; Return status indicating success or failure

.global sd_write_block
.type sd_write_block, %function
sd_write_block:
    ; Write a block of data to SD card
    ; Input:
    ;   r0 - Pointer to buffer containing data to write
    ;   r1 - Block number to write
    ; Output:
    ;   Data written to SD card
    ; Select SD card (assert CS pin)
    ; Send write command (CMD24) with block address
    ; Wait for response (R1 response indicating success)
    ; Write data block to SD card
    ; Deselect SD card (deassert CS pin)
    ; Return status indicating success or failure

.section .data
    ; Define buffer for reading/writing data to/from SD card
    sd_data_buffer: .space 512   ; Assuming block size of 512 bytes

.section .bss
    ; Define any uninitialized variables here if needed


;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;ARMOS - Dual Core M0+
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; Constants
.equ CPU0_STACK_SIZE, 512    ; Define stack size for CPU0
.equ CPU1_STACK_SIZE, 512    ; Define stack size for CPU1

.section .text
.global _start
.type _start, %function
_start:
    ; Initialize stack pointer for CPU0
    ldr r0, =__cpu0_stack_end__
    mov sp, r0

    ; Initialize stack pointer for CPU1
    ldr r0, =__cpu1_stack_end__
    mov sp, r0

    ; Start CPU1 by setting its program counter (PC) to the entry point
    ldr r0, =cpu1_entry
    ldr r1, =CPU1_STACK_SIZE
    mov lr, #0     ; Set return address to 0
    cpsie i        ; Enable interrupts
    svc 0x01       ; Call supervisor call instruction to start CPU1

    ; Continue executing on CPU0

cpu0_entry:
    ; This is the entry point for CPU0
    ; CPU0 code goes here

    bx lr

.global cpu1_entry
.type cpu1_entry, %function
cpu1_entry:
    ; This is the entry point for CPU1
    ; CPU1 code goes here

    bx lr

.section .bss
    .align 2
    __cpu0_stack_end__:
        .space CPU0_STACK_SIZE
    .align 2
    __cpu1_stack_end__:
        .space CPU1_STACK_SIZE

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;ARMOS - Dual Core M0+
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; Constants
.equ CPU0_STACK_SIZE, 512    ; Define stack size for CPU0
.equ CPU1_STACK_SIZE, 512    ; Define stack size for CPU1

; Memory map
.equ RAM_BASE, 0x20000000     ; Base address of RAM
.equ RAM_SIZE, 0x00004000     ; Size of RAM (16KB)
.equ ROM_BASE, 0x00000000     ; Base address of ROM
.equ ROM_SIZE, 0x00040000     ; Size of ROM (256KB)
.equ SD_BASE, 0x10000000      ; Base address of SD card memory
.equ SD_SIZE, 0x00100000      ; Size of SD card memory (1MB)

; SD card filesystem structure
.equ DIRECTORY_ENTRY_SIZE, 32  ; Size of directory entry
.equ MAX_FILES, 64             ; Maximum number of files supported

.section .text
.global _start
.type _start, %function
_start:
    ; Initialize stack pointer for CPU0
    ldr r0, =__cpu0_stack_end__
    mov sp, r0

    ; Initialize stack pointer for CPU1
    ldr r0, =__cpu1_stack_end__
    mov sp, r0

    ; Start CPU1 by setting its program counter (PC) to the entry point
    ldr r0, =cpu1_entry
    ldr r1, =CPU1_STACK_SIZE
    mov lr, #0     ; Set return address to 0
    cpsie i        ; Enable interrupts
    svc 0x01       ; Call supervisor call instruction to start CPU1

    ; Continue executing on CPU0
    bl init_filesystem   ; Initialize filesystem on SD card
    bl init_user_interface  ; Initialize user interface

cpu0_entry:
    ; Main loop for CPU0
    bl process_user_input   ; Process user input
    bl execute_command   ; Execute user command
    ; More tasks for CPU0

    bx lr

.global cpu1_entry
.type cpu1_entry, %function
cpu1_entry:
    ; Main loop for CPU1
    ; Task scheduling, background tasks, etc.

    bx lr

.section .bss
    .align 2
    __cpu0_stack_end__:
        .space CPU0_STACK_SIZE
    .align 2
    __cpu1_stack_end__:
        .space CPU1_STACK_SIZE

.section .data
    ; Define filesystem data structures, buffers, etc.


;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;ARMOS - Dual Core M0+ / Interrupts, SD Card, QSPI RAM, Keyboard, Audio, Video
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; Constants
.equ CPU0_STACK_SIZE, 512    ; Define stack size for CPU0
.equ CPU1_STACK_SIZE, 512    ; Define stack size for CPU1

.equ UART_BASE_ADDRESS, 0x40007000   ; Example UART peripheral base address
.equ UART_RX_IRQ, 12                  ; UART receive interrupt number
.equ UART_TX_IRQ, 13                  ; UART transmit interrupt number
.equ UART_RX_MASK, 1 << UART_RX_IRQ   ; UART receive interrupt mask
.equ UART_TX_MASK, 1 << UART_TX_IRQ   ; UART transmit interrupt mask

.equ SD_IRQ, 14                       ; SD card interrupt number
.equ SD_MASK, 1 << SD_IRQ             ; SD card interrupt mask

.equ QSPI_RAM_IRQ, 15                 ; QSPI RAM interrupt number
.equ QSPI_RAM_MASK, 1 << QSPI_RAM_IRQ ; QSPI RAM interrupt mask

.equ KEYBOARD_IRQ, 16                 ; Keyboard interrupt number
.equ KEYBOARD_MASK, 1 << KEYBOARD_IRQ ; Keyboard interrupt mask

.equ AUDIO_IRQ, 17                    ; Audio interrupt number
.equ AUDIO_MASK, 1 << AUDIO_IRQ       ; Audio interrupt mask

.equ VIDEO_IRQ, 18                    ; Video interrupt number
.equ VIDEO_MASK, 1 << VIDEO_IRQ       ; Video interrupt mask

.section .text
.global _start
.type _start, %function
_start:
    ; Initialize stack pointer for CPU0
    ldr r0, =__cpu0_stack_end__
    mov sp, r0

    ; Initialize stack pointer for CPU1
    ldr r0, =__cpu1_stack_end__
    mov sp, r0

    ; Start CPU1 by setting its program counter (PC) to the entry point
    ldr r0, =cpu1_entry
    ldr r1, =CPU1_STACK_SIZE
    mov lr, #0     ; Set return address to 0
    cpsie i        ; Enable interrupts
    svc 0x01       ; Call supervisor call instruction to start CPU1

    ; Continue executing on CPU0

cpu0_entry:
    ; This is the entry point for CPU0
    ; Initialize peripherals, file systems, and other components
    bl init_peripherals
    bl init_file_systems
    bl init_interrupts

    ; Main loop for CPU0
    b cpu0_main_loop

cpu0_main_loop:
    ; Main loop for CPU0
    ; Implement main loop functionality here
    ; This loop can handle user input, process commands, etc.
    ; It can also coordinate tasks between different peripherals and CPU1
    ; For example, reading from SD card, sending data to audio/video peripherals, etc.
    b cpu0_main_loop

.global cpu1_entry
.type cpu1_entry, %function
cpu1_entry:
    ; This is the entry point for CPU1
    ; Initialize peripherals, file systems, and other components
    bl init_peripherals
    bl init_file_systems
    bl init_interrupts

    ; Main loop for CPU1
    b cpu1_main_loop

cpu1_main_loop:
    ; Main loop for CPU1
    ; Implement main loop functionality here
    ; This loop can handle tasks that can be offloaded to CPU1
    ; For example, handling background tasks, managing disk operations, etc.
    b cpu1_main_loop

.global uart_isr
.type uart_isr, %function
uart_isr:
    ; UART interrupt service routine
    ; Implement UART interrupt handling code here

.global sd_isr
.type sd_isr, %function
sd_isr:
    ; SD card interrupt service routine
    ; Implement SD card interrupt handling code here

.global qspi_ram_isr
.type qspi_ram_isr, %function
qspi_ram_isr:
    ; QSPI RAM interrupt service routine
    ; Implement QSPI RAM interrupt handling code here

.global keyboard_isr
.type keyboard_isr, %function
keyboard_isr:
    ; Keyboard interrupt service routine
    ; Implement keyboard interrupt handling code here

.global audio_isr
.type audio_isr, %function
audio_isr:
    ; Audio interrupt service routine
    ; Implement audio interrupt handling code here

.global video_isr
.type video_isr, %function
video_isr:
    ; Video interrupt service routine
    ; Implement video interrupt handling code here

.section .bss
    .align 2
    __cpu0_stack_end__:
        .space CPU0_STACK_SIZE
    .align 2
    __cpu1_stack_end__:
        .space CPU1_STACK_SIZE

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;ARMOS - Dual Core M0+ / CP/M and DOS Compatibility
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.directory_entry:
    .ascii  "FILENAME"     ; 8-byte filename
    .ascii  "EXT"          ; 3-byte extension
    .byte   0x00           ; Attributes (e.g., read-only, hidden, system)
    .word   0              ; File size
    .word   0              ; Starting cluster
    .word   0              ; Modification timestamp
    .align  4              ; Align to word boundary
    
.file_allocation_table:
    .word   0xFFFF         ; Special values for end-of-file or free cluster
    .word   0xFFFF
    .word   0xFFFF
    ...
    .align  4              ; Align to word boundary

.file_buffer:
    .space  512            ; Example: 512-byte buffer size
    .align  4              ; Align to word boundary

.global read_directory_entry
.type read_directory_entry, %function
read_directory_entry:
    ; Read directory entry from disk into memory
    ; Input: r0 - Pointer to directory entry
    ;        r1 - Entry number (index)
    ;        r2 - Filesystem offset
    ; Output: Directory entry data in memory pointed by r0
    ; Implementation depends on filesystem format

.global write_directory_entry
.type write_directory_entry, %function
write_directory_entry:
    ; Write directory entry from memory to disk
    ; Input: r0 - Pointer to directory entry
    ;        r1 - Entry number (index)
    ;        r2 - Filesystem offset
    ; Implementation depends on filesystem format

.global read_fat_entry
.type read_fat_entry, %function
read_fat_entry:
    ; Read FAT entry from disk into memory
    ; Input: r0 - Pointer to FAT entry
    ;        r1 - Entry number (cluster number)
    ;        r2 - Filesystem offset
    ; Output: FAT entry data in memory pointed by r0
    ; Implementation depends on filesystem format

.global write_fat_entry
.type write_fat_entry, %function
write_fat_entry:
    ; Write FAT entry from memory to disk
    ; Input: r0 - Pointer to FAT entry
    ;        r1 - Entry number (cluster number)
    ;        r2 - Filesystem offset
    ; Implementation depends on filesystem format

.global read_file
.type read_file, %function
read_file:
    ; Read data from file into buffer
    ; Input: r0 - Pointer to buffer
    ;        r1 - File starting cluster
    ;        r2 - Filesystem offset
    ;        r3 - File size
    ; Output: Data read from file in buffer
    ; Implementation depends on filesystem format

.global write_file
.type write_file, %function
write_file:
    ; Write data from buffer to file
    ; Input: r0 - Pointer to buffer
    ;        r1 - File starting cluster
    ;        r2 - Filesystem offset
    ;        r3 - File size
    ; Implementation depends on filesystem format
