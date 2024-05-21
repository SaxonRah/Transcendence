.float16_add:
    ldrh r2, [r0]          @ Load first float
    ldrh r3, [r1]          @ Load second float

    mov r4, r2             @ Copy first float to r4
    mov r5, r3             @ Copy second float to r5

    lsls r6, r2, #1        @ Extract exponent of first float
    lsrs r6, r6, #11
    lsls r7, r3, #1        @ Extract exponent of second float
    lsrs r7, r7, #11

    subs r8, r6, r7        @ Compute difference in exponents

    cmp r8, #0
    beq .exponents_equal

    bgt .exponent1_bigger
    blt .exponent2_bigger

.exponent1_bigger:
    lsrs r2, r2, #10       @ Get mantissa of first float
    orrs r2, r2, #0x400    @ Set the implicit leading 1
    asrs r2, r8            @ Right shift mantissa by difference in exponents
    b .align_mantissas

.exponent2_bigger:
    lsrs r3, r3, #10       @ Get mantissa of second float
    orrs r3, r3, #0x400    @ Set the implicit leading 1
    asrs r3, r8            @ Right shift mantissa by difference in exponents
    b .align_mantissas

.exponents_equal:
    lsrs r2, r2, #10       @ Get mantissa of first float
    orrs r2, r2, #0x400    @ Set the implicit leading 1
    lsrs r3, r3, #10       @ Get mantissa of second float
    orrs r3, r3, #0x400    @ Set the implicit leading 1

.align_mantissas:
    adds r2, r2, r3        @ Add mantissas
    lsrs r9, r2, #11       @ Check for overflow

    cmp r9, #1
    beq .normalize

    lsls r2, r2, #1        @ No overflow, shift result mantissa left
    b .assemble_result

.normalize:
    adds r6, r6, #1        @ Increment exponent due to normalization

.assemble_result:
    bics r2, r2, #0x400    @ Clear the implicit leading 1
    lsls r2, r2, #10       @ Shift mantissa back
    orrs r2, r2, r6, lsl #10 @ Combine exponent and mantissa
    strh r2, [r0]          @ Store the result

    bx lr                  @ Return
