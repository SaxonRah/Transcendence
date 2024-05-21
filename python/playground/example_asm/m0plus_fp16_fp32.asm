.syntax unified
.thumb
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@ Test 16-bit and 32-bit Float Functions
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.global _start
_start:
@ Test 16-bit Addition
ldr r0, =float16_a
ldr r1, =float16_b
ldr r2, =float16_result
bl float16_add
strh r0, [r2]           @ Store the result of 16-bit addition

@ Test 16-bit Multiplication
ldr r0, =float16_a
ldr r1, =float16_b
ldr r2, =float16_result
bl float16_mul
strh r0, [r2]           @ Store the result of 16-bit multiplication

@ Test 16-bit Subtraction
ldr r0, =float16_a
ldr r1, =float16_b
ldr r2, =float16_result
bl float16_sub
strh r0, [r2]           @ Store the result of 16-bit subtraction

@ Test 16-bit Division
ldr r0, =float16_a
ldr r1, =float16_b
ldr r2, =float16_result
bl float16_div
strh r0, [r2]           @ Store the result of 16-bit division

@ Test 32-bit Addition
ldr r0, =float32_a
ldr r1, =float32_b
ldr r2, =float32_result
bl float32_add
str r0, [r2]            @ Store the result of 32-bit addition

@ Test 32-bit Multiplication
ldr r0, =float32_a
ldr r1, =float32_b
ldr r2, =float32_result
bl float32_mul
str r0, [r2]            @ Store the result of 32-bit multiplication

@ Test 32-bit Subtraction
ldr r0, =float32_a
ldr r1, =float32_b
ldr r2, =float32_result
bl float32_sub
str r0, [r2]            @ Store the result of 32-bit subtraction

@ Test 32-bit Division
ldr r0, =float32_a
ldr r1, =float32_b
ldr r2, =float32_result
bl float32_div
str r0, [r2]            @ Store the result of 32-bit division
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@FLOAT 16-BIT ADDITION
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.global float16_add
.type float16_add, %function
float16_add:
    ldrh r2, [r0]          @ Load first float
    ldrh r3, [r1]          @ Load second float

    mov r4, r2              @ Copy first float to r4
    mov r5, r3              @ Copy second float to r5

    lsls r6, r2, #1         @ Extract exponent of first float
    movs r6, r6, lsr #11
    lsls r7, r3, #1         @ Extract exponent of second float
    movs r7, r7, lsr #11

    subs r8, r6, r7         @ Compute difference in exponents
    bgt f16_add_exponent1_bigger   @ If exponent of first float is bigger, jump to exponent1_bigger
    blt f16_add_exponent2_bigger   @ If exponent of second float is bigger, jump to exponent2_bigger

    @ Exponents are equal, align mantissas
    lsls r2, r2, #6         @ Align mantissa of first float
    lsrs r3, r3, #9         @ Align mantissa of second float
    b f16_add_aligned

f16_add_exponent1_bigger:
    subs r8, r8, #FLOAT16_BIAS     @ Compute difference in exponents minus bias
    lsrs r3, r3, r8                @ Right shift mantissa of second float by difference
    b f16_add_aligned

f16_add_exponent2_bigger:
    subs r8, r8, #FLOAT16_BIAS     @ Compute difference in exponents minus bias
    lsrs r2, r2, r8                @ Right shift mantissa of first float by difference

f16_add_aligned:
    adds r2, r2, r3         @ Add mantissas
    movs r3, r2, lsr #10    @ Extract result exponent
    subs r3, r3, #FLOAT16_BIAS  @ Subtract bias from exponent
    strh r2, [r0]           @ Store result mantissa
    ands r3, r3, #31        @ Clear out any extra bits in exponent
    orrs r2, r2, r3, lsl #10 @ Combine mantissa and exponent
    strh r2, [r0]           @ Store result

    bx lr                   @ Return
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@FLOAT 16-BIT MULTIPLY
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.global float16_mul
.type float16_mul, %function
.float16_mul:
    ldrh r2, [r0]          @ Load first float
    ldrh r3, [r1]          @ Load second float

    mov r4, r2              @ Copy first float to r4
    mov r5, r3              @ Copy second float to r5

    lsls r6, r2, #1         @ Extract exponent of first float
    movs r6, r6, lsr #11
    lsls r7, r3, #1         @ Extract exponent of second float
    movs r7, r7, lsr #11

    adds r8, r6, r7         @ Add exponents
    subs r8, r8, #FLOAT16_BIAS  @ Subtract bias
    movs r9, #1             @ Prepare to handle implicit leading bit
    lsls r9, r9, #FLOAT16_MANTISSA_BITS  @ Shift 1 to the left by number of mantissa bits
    lsls r2, r2, #FLOAT16_MANTISSA_BITS  @ Shift mantissa of first float by number of mantissa bits
    lsls r3, r3, #FLOAT16_MANTISSA_BITS  @ Shift mantissa of second float by number of mantissa bits
    umull r2, r3, r2, r3   @ Multiply mantissas, results stored in r2:r3
    adds r3, r3, r9         @ Add implicit leading bit
    adc r2, r2, #0          @ Propagate any carry from addition of implicit bit
    orrs r2, r2, r3, lsr #FLOAT16_MANTISSA_BITS  @ Combine mantissas

    lsrs r2, r2, #16        @ Normalize mantissa to 16 bits

    strh r2, [r0]           @ Store result mantissa
    orrs r8, r8, r2, lsl #FLOAT16_EXPONENT_BITS  @ Combine exponent with mantissa
    strh r8, [r0]           @ Store result

    bx lr                   @ Return
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@FLOAT 16-BIT SUBTRACT
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.global float16_sub
.type float16_sub, %function
float16_sub:
    ldrh r2, [r0]          @ Load first float
    ldrh r3, [r1]          @ Load second float

    mov r4, r2              @ Copy first float to r4
    mov r5, r3              @ Copy second float to r5

    lsls r6, r2, #1         @ Extract exponent of first float
    movs r6, r6, lsr #11
    lsls r7, r3, #1         @ Extract exponent of second float
    movs r7, r7, lsr #11

    subs r8, r6, r7         @ Compute difference in exponents
    bgt f16_sub_exponent1_bigger   @ If exponent of first float is bigger, jump to exponent1_bigger
    blt f16_sub_exponent2_bigger   @ If exponent of second float is bigger, jump to exponent2_bigger

    @ Exponents are equal, align mantissas
    lsls r2, r2, #6         @ Align mantissa of first float
    lsrs r3, r3, #9         @ Align mantissa of second float
    b f16_sub_aligned

f16_sub_exponent1_bigger:
    subs r8, r8, #FLOAT16_BIAS     @ Compute difference in exponents minus bias
    lsrs r3, r3, r8                @ Right shift mantissa of second float by difference
    b f16_sub_aligned

f16_sub_exponent2_bigger:
    subs r8, r8, #FLOAT16_BIAS     @ Compute difference in exponents minus bias
    lsrs r2, r2, r8                @ Right shift mantissa of first float by difference

f16_sub_aligned:
    subs r2, r2, r3         @ Subtract mantissas
    movs r3, r2, lsr #10    @ Extract result exponent
    subs r3, r3, #FLOAT16_BIAS  @ Subtract bias from exponent
    strh r2, [r0]           @ Store result mantissa
    ands r3, r3, #31        @ Clear out any extra bits in exponent
    orrs r2, r2, r3, lsl #10 @ Combine mantissa and exponent
    strh r2, [r0]           @ Store result

    bx lr                   @ Return
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@FLOAT 16-BIT DIVIDE
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.global float16_div
.type float16_div, %function
.float16_div:
    ldrh r2, [r0]          @ Load first float
    ldrh r3, [r1]          @ Load second float

    mov r4, r2              @ Copy first float to r4
    mov r5, r3              @ Copy second float to r5

    lsls r6, r2, #1         @ Extract exponent of first float
    movs r6, r6, lsr #11
    lsls r7, r3, #1         @ Extract exponent of second float
    movs r7, r7, lsr #11

    subs r8, r6, r7         @ Compute difference in exponents
    subs r8, r8, #FLOAT16_BIAS  @ Subtract bias
    movs r9, #1             @ Prepare to handle implicit leading bit
    lsls r9, r9, #FLOAT16_MANTISSA_BITS  @ Shift 1 to the left by number of mantissa bits
    lsls r2, r2, #FLOAT16_MANTISSA_BITS  @ Shift mantissa of first float by number of mantissa bits
    lsls r3, r3, #FLOAT16_MANTISSA_BITS  @ Shift mantissa of second float by number of mantissa bits
    umull r2, r3, r2, r3   @ Multiply mantissas, results stored in r2:r3
    adds r3, r3, r9         @ Add implicit leading bit
    adc r2, r2, #0          @ Propagate any carry from addition of implicit bit
    orrs r2, r2, r3, lsr #FLOAT16_MANTISSA_BITS  @ Combine mantissas

    lsrs r2, r2, #16        @ Normalize mantissa to 16 bits

    strh r2, [r0]           @ Store result mantissa
    orrs r8, r8, r2, lsl #FLOAT16_EXPONENT_BITS  @ Combine exponent with mantissa
    strh r8, [r0]           @ Store result

    bx lr                   @ Return
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@FLOAT 32-BIT ADDITION
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.global float32_add
.type float32_add, %function
float32_add:
    ldr r2, [r0]            @ Load first float
    ldr r3, [r1]            @ Load second float

    mov r4, r2              @ Copy first float to r4
    mov r5, r3              @ Copy second float to r5

    lsls r6, r2, #1         @ Extract exponent of first float
    movs r6, r6, lsr #24
    lsls r7, r3, #1         @ Extract exponent of second float
    movs r7, r7, lsr #24

    subs r8, r6, r7         @ Compute difference in exponents
    bgt f32_add_exponent1_bigger   @ If exponent of first float is bigger, jump to exponent1_bigger
    blt f32_add_exponent2_bigger   @ If exponent of second float is bigger, jump to exponent2_bigger

    @ Exponents are equal, align mantissas
    lsls r2, r2, #9         @ Align mantissa of first float
    lsrs r3, r3, #14        @ Align mantissa of second float
    b f32_add_aligned

f32_add_exponent1_bigger:
    subs r8, r8, #FLOAT32_BIAS     @ Compute difference in exponents minus bias
    lsrs r3, r3, r8                @ Right shift mantissa of second float by difference
    b f32_add_aligned

f32_add_exponent2_bigger:
    subs r8, r8, #FLOAT32_BIAS     @ Compute difference in exponents minus bias
    lsrs r2, r2, r8                @ Right shift mantissa of first float by difference

f32_add_aligned:
    adds r2, r2, r3         @ Add mantissas
    movs r3, r2, lsr #23    @ Extract result exponent
    subs r3, r3, #FLOAT32_BIAS  @ Subtract bias from exponent
    str r2, [r0]            @ Store result mantissa
    ands r3, r3, #255       @ Clear out any extra bits in exponent
    orrs r2, r2, r3, lsl #23 @ Combine mantissa and exponent
    str r2, [r0]            @ Store result

    bx lr                   @ Return
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@FLOAT 32-BIT MULTIPLY
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.global float32_mul
.type float32_mul, %function
.float32_mul:
    ldr r2, [r0]            @ Load first float
    ldr r3, [r1]            @ Load second float

    mov r4, r2              @ Copy first float to r4
    mov r5, r3              @ Copy second float to r5

    lsls r6, r2, #1         @ Extract exponent of first float
    movs r6, r6, lsr #24
    lsls r7, r3, #1         @ Extract exponent of second float
    movs r7, r7, lsr #24

    adds r8, r6, r7         @ Add exponents
    subs r8, r8, #FLOAT32_BIAS  @ Subtract bias
    movs r9, #1             @ Prepare to handle implicit leading bit
    lsls r9, r9, #FLOAT32_MANTISSA_BITS  @ Shift 1 to the left by number of mantissa bits
    lsls r2, r2, #FLOAT32_MANTISSA_BITS  @ Shift mantissa of first float by number of mantissa bits
    lsls r3, r3, #FLOAT32_MANTISSA_BITS  @ Shift mantissa of second float by number of mantissa bits
    umull r2, r3, r2, r3   @ Multiply mantissas, results stored in r2:r3
    adds r3, r3, r9         @ Add implicit leading bit
    adc r2, r2, #0          @ Propagate any carry from addition of implicit bit
    orrs r2, r2, r3, lsr #FLOAT32_MANTISSA_BITS  @ Combine mantissas

    lsrs r2, r2, #32        @ Normalize mantissa to 32 bits

    str r2, [r0]            @ Store result mantissa
    orrs r8, r8, r2, lsl #FLOAT32_EXPONENT_BITS  @ Combine exponent with mantissa
    str r8, [r0]            @ Store result

    bx lr                   @ Return
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@FLOAT 32-BIT SUBTRACT
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.global float32_sub
.type float32_sub, %function
float32_sub:
    ldr r2, [r0]            @ Load first float
    ldr r3, [r1]            @ Load second float

    mov r4, r2              @ Copy first float to r4
    mov r5, r3              @ Copy second float to r5

    lsls r6, r2, #1         @ Extract exponent of first float
    movs r6, r6, lsr #24
    lsls r7, r3, #1         @ Extract exponent of second float
    movs r7, r7, lsr #24

    subs r8, r6, r7         @ Compute difference in exponents
    bgt f32_sub_exponent1_bigger   @ If exponent of first float is bigger, jump to exponent1_bigger
    blt f32_sub_exponent2_bigger   @ If exponent of second float is bigger, jump to exponent2_bigger

    @ Exponents are equal, align mantissas
    lsls r2, r2, #9         @ Align mantissa of first float
    lsrs r3, r3, #14        @ Align mantissa of second float
    b f32_sub_aligned

f32_sub_exponent1_bigger:
    subs r8, r8, #FLOAT32_BIAS     @ Compute difference in exponents minus bias
    lsrs r3, r3, r8                @ Right shift mantissa of second float by difference
    b f32_sub_aligned

f32_sub_exponent2_bigger:
    subs r8, r8, #FLOAT32_BIAS     @ Compute difference in exponents minus bias
    lsrs r2, r2, r8                @ Right shift mantissa of first float by difference

f32_sub_aligned:
    subs r2, r2, r3         @ Subtract mantissas
    movs r3, r2, lsr #23    @ Extract result exponent
    subs r3, r3, #FLOAT32_BIAS  @ Subtract bias from exponent
    str r2, [r0]            @ Store result mantissa
    ands r3, r3, #255       @ Clear out any extra bits in exponent
    orrs r2, r2, r3, lsl #23 @ Combine mantissa and exponent
    str r2, [r0]            @ Store result

    bx lr                   @ Return
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@FLOAT 32-BIT DIVIDE
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.global float32_div
.type float32_div, %function
.float32_div:
    ldr r2, [r0]            @ Load first float
    ldr r3, [r1]            @ Load second float

    mov r4, r2              @ Copy first float to r4
    mov r5, r3              @ Copy second float to r5

    lsls r6, r2, #1         @ Extract exponent of first float
    movs r6, r6, lsr #24
    lsls r7, r3, #1         @ Extract exponent of second float
    movs r7, r7, lsr #24

    adds r8, r6, r7         @ Add exponents
    subs r8, r8, #FLOAT32_BIAS  @ Subtract bias
    movs r9, #1             @ Prepare to handle implicit leading bit
    lsls r9, r9, #FLOAT32_MANTISSA_BITS  @ Shift 1 to the left by number of mantissa bits
    lsls r2, r2, #FLOAT32_MANTISSA_BITS  @ Shift mantissa of first float by number of mantissa bits
    lsls r3, r3, #FLOAT32_MANTISSA_BITS  @ Shift mantissa of second float by number of mantissa bits
    umull r2, r3, r2, r3   @ Multiply mantissas, results stored in r2:r3
    adds r3, r3, r9         @ Add implicit leading bit
    adc r2, r2, #0          @ Propagate any carry from addition of implicit bit
    orrs r2, r2, r3, lsr #FLOAT32_MANTISSA_BITS  @ Combine mantissas

    lsrs r2, r2, #32        @ Normalize mantissa to 32 bits

    str r2, [r0]            @ Store result mantissa
    orrs r8, r8, r2, lsl #FLOAT32_EXPONENT_BITS  @ Combine exponent with mantissa
    str r8, [r0]            @ Store result

    bx lr                   @ Return
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@FLOAT 16-BIT Test and Data
@~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@ Data Section
.data
float16_a: .hword 0x3C00     @ 1.0 in 16-bit float
float16_b: .hword 0x4000     @ 2.0 in 16-bit float
float16_result: .hword 0x0000

float32_a: .word 0x3F800000  @ 1.0 in 32-bit float
float32_b: .word 0x40000000  @ 2.0 in 32-bit float
float32_result: .word 0x00000000

.equ FLOAT16_EXPONENT_BITS, 5
.equ FLOAT16_MANTISSA_BITS, 10
.equ FLOAT16_BIAS, 15
.equ FLOAT16_SIGN_BIT, 15
.equ FLOAT16_EXPONENT_MASK, ((1 << FLOAT16_EXPONENT_BITS) - 1) << (FLOAT16_MANTISSA_BITS)
.equ FLOAT16_MANTISSA_MASK, (1 << FLOAT16_MANTISSA_BITS) - 1

.equ FLOAT32_EXPONENT_BITS, 8
.equ FLOAT32_MANTISSA_BITS, 23
.equ FLOAT32_BIAS, 127
.equ FLOAT32_SIGN_BIT, 31
.equ FLOAT32_EXPONENT_MASK, ((1 << FLOAT32_EXPONENT_BITS) - 1) << (FLOAT32_MANTISSA_BITS)
.equ FLOAT32_MANTISSA_MASK, (1 << FLOAT32_MANTISSA_BITS) - 1

