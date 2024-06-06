.program qspi
; QSPI program for the Raspberry Pi Pico
; Assumes a simple read/write operation.

.side_set 1 opt

; QSPI Write operation
.wrap_target
    out pins, 1       side 0b0    ; Assert CS (CE# low)
    set x, 31         side 0b0    ; Set up for 32 bits transfer (command + address)
    out pins, 4       side 0b0    ; Send 4-bit nibbles (command/address)
    jmp x--, transfer side 0b0    ; Loop until all bits sent
transfer:
    out pins, 4       side 0b0    ; Send 4-bit nibbles (data)
    jmp x--, transfer side 0b0    ; Loop until all bits sent
    nop               side 0b1    ; Deassert CS (CE# high)
.wrap

; QSPI Read operation
.wrap_target
    out pins, 1       side 0b0    ; Assert CS (CE# low)
    set x, 31         side 0b0    ; Set up for 32 bits transfer (command + address)
    out pins, 4       side 0b0    ; Send 4-bit nibbles (command/address)
    jmp x--, receive  side 0b0    ; Loop until all bits sent
receive:
    in pins, 4        side 0b0    ; Receive 4-bit nibbles (data)
    jmp x--, receive  side 0b0    ; Loop until all bits received
    nop               side 0b1    ; Deassert CS (CE# high)
.wrap
