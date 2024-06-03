.syntax unified
.cpu cortex-m0plus
.thumb_func
// .thumb

.section .text
.global main

main:
init:   bl stdio_init_all           // Jump to SDK STDIO initialisation routine
        movs r0, #0x80              // Set the delay period
        lsls r0, #4
        bl sleep_ms                 // Delay to allow the STDIO-over-USB to ready

        b info                      // Jump to the CPU info readout

loop:
    // Load the integer value into a register
    MOVS R0, #254   // Integer value 754
    // Convert the integer to floating-point
    BL int_to_float

    // Return from main
    BX LR

int_to_float:
    // Prepare space for floating-point conversion
    MOVS R1, #0
    MOVS R2, #0

    // Load the integer into R3 and R4 (low registers)
    MOV R3, R0      // Load the integer into R3
    MOVS R4, #0      // Clear R4 for the second half of the integer

    // Convert integer to floating-point
    // This is a simplified version and may not cover all cases
    // It assumes the integer is already in the correct format
    // Adjust this part based on the specific requirements of your application

    // Sign bit: Set to 0 for positive numbers
    // Exponent: For simplicity, set to 127 + 31 (biased representation)
    // Mantissa: Bits 22-0 of the IEEE 754 format
    MOVS R1, #127 + 31 // Exponent bias
    MOVS R2, R1, LSL #23 // Move exponent into position
    LSRS R3, R3, #9 // Move bits 22-0 of integer to mantissa
    ORRS R2, R2, R3 // OR mantissa with exponent

    // Store the floating-point representation in memory or use it further
    // R1 and R2 contain the floating-point representation

    BX LR // Return

info:   ldr r5, CPUID               // Get the address of CPUID
        ldr r5, [r5]                // Get the contents of CPUID

        // Write out the CPUID register
        ldr r0, =TEXT0              // Set the printf format string
        movs r1, r5                 // Set the printf value
        bl printf

        // Write out the part number
        ldr r0, =TEXT1              // Set the format string
        movs r1, r5                 // Set the printf value to the CPUID value
        movs r3, #0xFF              // Set the AND mask
        lsls r3, #8
        adds r3, #0xF0
        ands r1, r3                 // Mask CPUID bits 15-4
        lsrs r3, #4
        bl printf

        // Write out the revision
        ldr r0, =TEXT2              // Set the format string
        movs r1, r5                 // Set the printf value to the CPUID value
        movs r3, #0x0F              // Set the AND mask
        lsls r3, #20
        ands r1, r3                 // Mask CPUID bits 23-20
        lsrs r3, #20
        bl printf

        // Write out the variant number
        ldr r0, =TEXT3              // Set the format string
        movs r1, r5                 // Set the printf value to the CPUID value
        movs r3, #0x0F              // Set the AND mask
        ands r1, r3                 // Mask CPUID bits 3-0
        bl printf

        // FROM 1.0.1 -- unified syntax test
        movs r0, #0                 // Clear r0
        mvns r0, r0                 // NOT r0 0x00000000 -> 0xFFFFFFFF
        movs r1, #1                 // r1 = 1
        rsbs r1, #0                 // r1 = 0 - r1 = 0xFFFFFFFF
        cmp r0, r1                  // r1 == r2?
        bne xinfo                   // Jump out if r1 != r2

        ldr r0, =TEXT4              // Output match message
        bl printf

 xinfo: b loop                      // Jump back to the LED flash loop
        
.align 4
FLOATY:         .word           0x443C8000
CPUID:          .word           0xE000ED00          // Memory map address of CPUID register
TEXT0:          .asciz          "CPUID: 0x%08X\n"
TEXT1:          .asciz          "Part:  0x%08X\n"
TEXT2:          .asciz          "Rev:   0x%08X\n"
TEXT3:          .asciz          "Var:   0x%08X\n"
TEXT4:          .asciz          "MATCH\n"