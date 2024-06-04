### Translation Errors:
HLT, CMA, RLC, CPI, SUI, ADI, RAL, RRC, RAR, ORI, XCHG, XTHL.

### Unsupported Instructions:
RET, RNZ, STC, RZ, RC

### PL/M and CP/M
```
example: BDOS:EQU 5 ; CP/M CALL
```
CP/M calls need to be handled
PL/M code should be also handled.

### Translation Issues

- several instructions are getting formatted improperly.
  - due to mapping and AST mismatch.
- should add SUFFIX handling
  - mov -> movs
- probably more issues i missed.

### Improper Translation Examples
```
example: MOV A, #("'0'", '-', '1')
example: MOV B, #('F16MB', '+', 'F16BIA', '-', '1')
```
tuple aren't getting translated.

```
example: FADD: JMP F16ADD
output: FADD:
```
JMP isn't getting translated.
```
example: F16SUB: ; 4B / 22C + 26C
XCHG
CALL F16NEG
output:
F16SUB:
BL F
```
jump/branch labels are getting truncated.

```
example: DB 0
```
DB isn't handled. nor is DW
below is an example of such translation

I8080:
```
; PACKED FP16 - 0..10
A2F16T:
DB 0,78H,80H,84H,88H,8AH,8CH,8EH,90H,91H,92H
; 10^X TABLE, X=0..4
F16X10:
DW F16_1,F16_10,5640H,63D0H,70D2H
```
ARM THUMB:
```
; PACKED FP16 - 0..10
A2F16T:
    .byte 0, 0x78, 0x80, 0x84, 0x88, 0x8A, 0x8C, 0x8E, 0x90, 0x91, 0x92
; 10^X TABLE, X=0..4
F16X10:
    .word F16_1, F16_10, 0x5640, 0x63D0, 0x70D2
```
