# Dual RP2040 and Dual Core Communication.
## ! ! ! WORK IN PROGRESS ! ! ! HERE BE DRAGONS ! ! ! WORK IN PROGRESS ! ! ! 

## Code breakdown for each RP2040 microcontroller:
1. ### RP2040 #1:
  - #### Core 0:
    - **Sends Messages to RP2040 #1 Core 1**: 
      - Core 0 sends messages to Core 1 of the same RP2040.
    - **Receives Messages from RP2040 #1 Core 1**:
      - Core 0 receives messages from Core 1 of the same RP2040.
  - #### Core 1:
    - **Sends and Receives Messages to/from RP2040 #2 Core 1**:
      - Core 1 sends messages to Core 1 of RP2040 #2.
      - Core 1 receives messages from Core 1 of RP2040 #2.
2. ### RP2040 #2:
  - #### Core 0:
    - **Sends Messages to RP2040 #2 Core 1**:
      - Core 0 sends messages to Core 1 of the same RP2040.
    - **Receives Messages from RP2040 #2 Core 1**:
      - Core 0 receives messages from Core 1 of the same RP2040.
  - #### Core 1:
    - **Sends and Receives Messages to/from RP2040 #1 Core 1**:
      - Core 1 sends messages to Core 1 of RP2040 #1.
      - Core 1 receives messages from Core 1 of RP2040 #1.

# Basic Assembly Implementation
## Register Addresses and Mailbox Channels
```assembly
; Define MMIO Register Addresses for Mailbox System
.equ MAILBOX_BASE_ADDRESS, 0x40050000     ; Base address of the mailbox registers

; Define Mailbox Channels for RP2040 Cores
.equ CORE0_MAILBOX_CHANNEL, 0             ; Mailbox channel for RP2040 Core 0
.equ CORE1_MAILBOX_CHANNEL, 1             ; Mailbox channel for RP2040 Core 1
```
## RP2040 #1 Core 0 <-> RP2040 #1 Core 1
```assembly
; RP2040 #1 Core 0
; Function to send a message to RP2040 #1 Core 1
send_msg_to_rp1_core1:
    ldr r0, =message_to_rp1_core1
    bl send_msg_rp1_core1
    bx lr
; Function to receive a message from RP2040 #1 Core 1
recv_msg_from_rp1_core1:
    bl recv_msg_rp1_core1
    ; Process received message
    bx lr
```
## RP2040 #1 Core 1 <-> RP2040 #2 Core 1
```assembly
; RP2040 #1 Core 1
; Function to send a message to RP2040 #2 Core 1
send_msg_to_rp2_core1:
    ldr r0, =message_to_rp2_core1
    bl send_msg_rp2_core1
    bx lr
; Function to receive a message from RP2040 #2 Core 1
recv_msg_from_rp2_core1:
    bl recv_msg_rp2_core1
    ; Process received message
    bx lr
```
## RP2040 #2 Core 0 <-> RP2040 #2 Core 1
```assembly
; RP2040 #2 Core 0
; Function to send a message to RP2040 #2 Core 1
send_msg_to_rp2_core1:
    ldr r0, =message_to_rp2_core1
    bl send_msg_rp2_core1
    bx lr
; Function to receive a message from RP2040 #2 Core 1
recv_msg_from_rp2_core1:
    bl recv_msg_rp2_core1
    ; Process received message
    bx lr
```
## RP2040 #2 Core 1 <-> RP2040 #1 Core 1
```assembly
;RP2040 #2 Core 1
; Function to send a message to RP2040 #1 Core 1
send_msg_to_rp1_core1:
    ldr r0, =message_to_rp1_core1
    bl send_msg_rp1_core1
    bx lr
; Function to receive a message from RP2040 #1 Core 1
recv_msg_from_rp1_core1:
    bl recv_msg_rp1_core1
    ; Process received message
    bx lr
```
# Mailbox Communication Functions
## RP2040 #1 Core0 <-> RP2040 #1 Core1 <-> RP2040 #2 Core1 <-> RP2040 #2 Core0
```assembly
; RP2040 #1 Core 0
send_msg_rp1_core0_to_core1:
    ldr r1, =MAILBOX_BASE_ADDRESS    ; Load Mailbox base address
    ldr r2, =CORE1_MAILBOX_CHANNEL   ; Load mailbox channel for Core 1
.wait_for_space_rp1_core1:
    ldr r3, [r1, r2, lsl #2]         ; Read current mailbox status
    tst r3, #MAILBOX_FULL_BIT        ; Check if mailbox is full
    bne .wait_for_space_core1        ; If mailbox is full, wait
    str r0, [r1, r2, lsl #2]         ; Write message to mailbox
    bx lr
recv_msg_rp1_core0_from_core1:
    ldr r1, =MAILBOX_BASE_ADDRESS    ; Load Mailbox base address
    ldr r2, =CORE0_MAILBOX_CHANNEL   ; Load mailbox channel for Core 0
.wait_for_message_rp1_core1:
    ldr r3, [r1, r2, lsl #2]         ; Read current mailbox status
    tst r3, #MAILBOX_EMPTY_BIT       ; Check if mailbox is empty
    beq .wait_for_message_rp1_core1  ; If mailbox is empty, wait
    ldr r0, [r1, r2, lsl #2]         ; Read message from mailbox
    bx lr

; RP2040 #1 Core 1
send_msg_rp1_core1_to_core0:
    ldr r1, =MAILBOX_BASE_ADDRESS    ; Load Mailbox base address
    ldr r2, =CORE0_MAILBOX_CHANNEL   ; Load mailbox channel for Core 0
.wait_for_space_rp1_core0:
    ldr r3, [r1, r2, lsl #2]         ; Read current mailbox status
    tst r3, #MAILBOX_FULL_BIT        ; Check if mailbox is full
    bne .wait_for_space_rp1_core0    ; If mailbox is full, wait
    str r0, [r1, r2, lsl #2]         ; Write message to mailbox
    bx lr
recv_msg_rp1_core1_from_core0:
    ldr r1, =MAILBOX_BASE_ADDRESS    ; Load Mailbox base address
    ldr r2, =CORE1_MAILBOX_CHANNEL   ; Load mailbox channel for Core 1
.wait_for_message_rp1_core0:
    ldr r3, [r1, r2, lsl #2]         ; Read current mailbox status
    tst r3, #MAILBOX_EMPTY_BIT       ; Check if mailbox is empty
    beq .wait_for_message_rp1_core0  ; If mailbox is empty, wait
    ldr r0, [r1, r2, lsl #2]         ; Read message from mailbox
    bx lr

; RP2040 #2 Core 0
send_msg_rp2_core0_to_core1:
    ldr r1, =MAILBOX_BASE_ADDRESS    ; Load Mailbox base address
    ldr r2, =CORE1_MAILBOX_CHANNEL   ; Load mailbox channel for Core 1
.wait_for_space_rp2_core1:
    ldr r3, [r1, r2, lsl #2]         ; Read current mailbox status
    tst r3, #MAILBOX_FULL_BIT        ; Check if mailbox is full
    bne .wait_for_space_rp2_core1    ; If mailbox is full, wait
    str r0, [r1, r2, lsl #2]         ; Write message to mailbox
    bx lr
recv_msg_rp2_core0_from_core1:
    ldr r1, =MAILBOX_BASE_ADDRESS    ; Load Mailbox base address
    ldr r2, =CORE0_MAILBOX_CHANNEL   ; Load mailbox channel for Core 0
.wait_for_message_rp2_core1:
    ldr r3, [r1, r2, lsl #2]         ; Read current mailbox status
    tst r3, #MAILBOX_EMPTY_BIT       ; Check if mailbox is empty
    beq .wait_for_message_rp2_core1  ; If mailbox is empty, wait
    ldr r0, [r1, r2, lsl #2]         ; Read message from mailbox
    bx lr

; RP2040 #2 Core 1
send_msg_rp2_core1_to_core0:
    ldr r1, =MAILBOX_BASE_ADDRESS    ; Load Mailbox base address
    ldr r2, =CORE0_MAILBOX_CHANNEL   ; Load mailbox channel for Core 0
.wait_for_space_rp2_core0:
    ldr r3, [r1, r2, lsl #2]         ; Read current mailbox status
    tst r3, #MAILBOX_FULL_BIT        ; Check if mailbox is full
    bne .wait_for_space_rp2_core0    ; If mailbox is full, wait
    str r0, [r1, r2, lsl #2]         ; Write message to mailbox
    bx lr

recv_msg_rp2_core1_from_core0:
    ldr r1, =MAILBOX_BASE_ADDRESS    ; Load Mailbox base address
    ldr r2, =CORE1_MAILBOX_CHANNEL   ; Load mailbox channel for Core 1
.wait_for_message_rp2_core0:
    ldr r3, [r1, r2, lsl #2]         ; Read current mailbox status
    tst r3, #MAILBOX_EMPTY_BIT       ; Check if mailbox is empty
    beq .wait_for_message_rp2_core0  ; If mailbox is empty, wait
    ldr r0, [r1, r2, lsl #2]         ; Read message from mailbox
    bx lr
```
# UART Communication Example
I'll give an example of how this might be implemented via UART.
## RP2040 #1 Core 0 UART <-> RP2040 #2 Core 0 UART
```assembly
; Define UART Register Addresses
.equ UART_BASE_ADDRESS, 0x40050000
.equ UART_TX_OFFSET, 0x00
.equ UART_RX_OFFSET, 0x04

; RP2040 #1 Core 0
; Function to send a message to RP2040 #1 Core 1 via UART
send_msg_to_rp1_core1:
    ldr r0, =message_to_rp1_core1
    bl send_uart_message
    bx lr
; Function to receive a message from RP2040 #1 Core 1 via UART
recv_msg_from_rp1_core1:
    bl recv_uart_message
    ; Process received message
    bx lr
; Function to send a message via UART
; Input: r0 - address of the message
send_uart_message:
    ldr r1, =UART_BASE_ADDRESS       ; Load UART base address
    ldr r2, =UART_TX_OFFSET          ; Load UART TX register offset
    strb r0, [r1, r2]                ; Write message byte to UART TX register
    bx lr
; Function to receive a message via UART
; Output: r0 - received message
recv_uart_message:
    ldr r1, =UART_BASE_ADDRESS       ; Load UART base address
    ldr r2, =UART_RX_OFFSET          ; Load UART RX register offset
    ldrb r0, [r1, r2]                ; Read received message byte from UART RX register
    bx lr

; RP2040 #2 Core 0
; Function to send a message to RP2040 #2 Core 1 via UART
send_msg_to_rp2_core1:
    ldr r0, =message_to_rp2_core1
    bl send_uart_message
    bx lr
; Function to receive a message from RP2040 #2 Core 1 via UART
recv_msg_from_rp2_core1:
    bl recv_uart_message
    ; Process received message
    bx lr
; Function to send a message via UART
; Input: r0 - address of the message
send_uart_message:
    ldr r1, =UART_BASE_ADDRESS       ; Load UART base address
    ldr r2, =UART_TX_OFFSET          ; Load UART TX register offset
    strb r0, [r1, r2]                ; Write message byte to UART TX register
    bx lr
; Function to receive a message via UART
; Output: r0 - received message
recv_uart_message:
    ldr r1, =UART_BASE_ADDRESS       ; Load UART base address
    ldr r2, =UART_RX_OFFSET          ; Load UART RX register offset
    ldrb r0, [r1, r2]                ; Read received message byte from UART RX register
    bx lr
```
