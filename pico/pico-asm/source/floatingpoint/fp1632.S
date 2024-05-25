.syntax unified
.cpu cortex-m0plus
.thumb

.section .text
.global main

main:
    // Load the integer value into a register
    LDR R0, =754   // Integer value 754
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
