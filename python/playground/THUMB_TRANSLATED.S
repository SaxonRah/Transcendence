; Directive ORG 1, 0, 0, H
B F
FADD:
FSUB:
FMUL:
FDIV:
F16_1:
F16_E:
F16_PI:
F16_10:
BDOS:
F16SM:
F16EM:
F16MM:
F16MB:
F16BIA:
F16UEM:
F16MI1:
F16FDL:
F16SUB:
BL F
F16ADD:
AND D
ORR E
; Unsupported instruction RZ
; Error translating instruction XCHG
MOV A, #('F16SM', '-', '1')
AND D
ORR E
; Unsupported instruction RZ
PUSH {H}
MOV A, H
EOR D
MOV L, A
; Error translating instruction XTHL
BL F
SUB C, C, #1
BCC F
MOV B, C
; Error translating instruction CMA
ADD A, A, #1
MOV C, A
; Error translating instruction XCHG
; Error translating instruction XTHL
MOV A, H
EOR L
MOV H, A
; Error translating instruction XTHL
MOV A, C
F16A1:
MOV C, A
BL D
POP {P}
MOV C, A
BMI N
ADD D
MOV D, C
B F
BCS F
BL N
MOV A, #F16SM
EOR D
MOV D, A
F16NRP:
; Unsupported instruction RC
F16PCK:
AND H
MOV H, A
MOV A, B
; Error translating instruction RLC
; Error translating instruction RLC
; Error translating instruction CPI
BCC F
ORR H
MOV H, A
F16SGN:
AND D
ORR H
MOV H, A
; Unsupported instruction RET
F16UNP:
BL F
MOV C, B
; Error translating instruction XCHG
F16UPH:
AND H
; Error translating instruction RRC
; Error translating instruction RRC
MOV B, A
MOV A, #F16MM
AND H
; Error translating instruction ORI
MOV H, A
MOV A, B
ORR A
; Unsupported instruction RNZ
MOV A, #F16MI1
EOR H
MOV H, A
MOV A, B
; Unsupported instruction RET
F16DNP:
LDR R2, [ADR], STR R2, [DE] H, =F16PCK
; Error translating instruction XTHL
MOV A, #('F16MI1', '+', 'F16MI1')
AND H
; Unsupported instruction RZ
DIV2X2:
DIV2X1:
DIV2XC:
ORR A
; Unsupported instruction RZ
; Error translating instruction CPI
BCC F
DIV2C1:
ORR A
; Error translating instruction RAR
MOV H, A
MOV A, L
; Error translating instruction RAR
MOV L, A
SUB C, C, #1
BNE D
; Unsupported instruction RNC
ADD H
MOV A, #('F16MI1', '+', 'F16MI1')
AND H
; Unsupported instruction RZ
B D
F16NRM:
ORR L
; Unsupported instruction STC
; Unsupported instruction RZ
MOV A, B
ORR A
; Unsupported instruction RZ
F16N1:
AND H
; Unsupported instruction RNZ
ADD H
SUB B, B, #1
BNE F
; Unsupported instruction RET
F16MUL:
AND H
ORR L
; Unsupported instruction RZ
; Error translating instruction XCHG
MOV A, #('F16SM', '-', '1')
AND H
ORR L
; Unsupported instruction RZ
MOV A, H
EOR D
PUSH {P}
BL F
ADD C, C, #1
; Error translating instruction SUI
BCS F
BEQ F
; Error translating instruction CPI
BCC F
PUSH {P}
MOV B, H
MOV C, L
LDR R2, [ADR], STR R2, [DE] H, =0
MOV A, #F16MB
F16M1:
MOV A, H
ORR A
; Error translating instruction RAR
MOV H, A
MOV A, L
; Error translating instruction RAR
MOV L, A
MOV A, B
; Error translating instruction RAR
MOV B, A
MOV A, C
; Error translating instruction RAR
MOV C, A
BCC F
ADD D
F16M2:
SUB A, A, #1
BNE F
POP {B}
POP {D}
B F
F16DIV:
EOR D
PUSH {P}
MOV A, #('F16SM', '-', '1')
AND D
ORR E
BEQ F
MOV A, #('F16SM', '-', '1')
AND H
ORR L
BEQ F
BL F
SUB C, C, #1
; Error translating instruction ADI
BMI F
BEQ F
; Error translating instruction CPI
BCC F
PUSH {P}
BL F
BCC F
ADD H
; Error translating instruction XTHL
SUB H, H, #1
; Error translating instruction XTHL
F16D3:
BL N
MOV A, #('F16MB', '+', '1')
LDR R2, [ADR], STR R2, [DE] B, =0
F16D1:
PUSH {H}
ADD D
BCC F
; Error translating instruction XCHG
F16D2:
MOV A, C
; Error translating instruction RAL
MOV C, A
MOV A, B
; Error translating instruction RAL
MOV B, A
; Error translating instruction XCHG
ADD H
; Error translating instruction XCHG
POP {P}
SUB A, A, #1
BNE F
MOV H, B
MOV L, C
POP {B}
POP {D}
MOV A, #('F16MI1', '+', 'F16MI1')
AND H
BNE D
B F
F16SQR:
F16RND:
F16ABS:
ORR A
; Unsupported instruction RP
F16NEG:
EOR H
MOV H, A
; Unsupported instruction RET
F16CMP:
AND D
MOV B, A
MOV A, #F16EM
AND H
CMP B, B, #1
; Unsupported instruction RNZ
F16CPM:
AND D
MOV B, A
MOV A, #F16MM
AND H
CMP B, B, #1
; Unsupported instruction RNZ
MOV A, L
CMP E, E, #1
; Unsupported instruction RET
F16OFL:
F16INF:
MOV L, #0
B F
F16ZRS:
F16ZRO:
; Unsupported instruction RET
F16INT:
LDR R2, [ADR], STR R2, [DE] H, =0
MOV A, #F16EM
AND D
; Error translating instruction RRC
; Error translating instruction RRC
; Error translating instruction SUI
; Unsupported instruction RC
ADD A, A, #1
MOV B, A
MOV A, #F16MI1
ORR D
MOV D, A
PUSH {P}
F162I1:
MOV A, #F16MI1
AND D
BEQ F
ADD H
F162I2:
ADD H
; Error translating instruction XCHG
SUB B, B, #1
BNE F
POP {P}
; Unsupported instruction RP
NEG16:
; Error translating instruction CMA
MOV L, A
MOV A, H
; Error translating instruction CMA
MOV H, A
ADD H
; Unsupported instruction RET
INTF16:
ORR L
; Unsupported instruction RZ
LDR R2, [ADR], STR R2, [DE] B, =F16PCK
PUSH {B}
MOV B, #('F16MB', '+', 'F16BIA', '-', '1')
MOV D, #0
MOV A, H
; Error translating instruction CPI
BCS F
MOV C, #('16', '-', 'F16MB', '+', '1')
I2F161:
; Error translating instruction RLC
BCC I
MOV A, B
ADD C, C, #1
MOV B, A
B D
STRINT:
; Error translating instruction XCHG
S2I2:
S2I1:
ADD D
ORR A
; Unsupported instruction RZ
SUB ', 0, '
; Unsupported instruction RC
CMP 1, 0
; Unsupported instruction RNC
SUB C, C, #1
BEQ S
PUSH {B}
MOV B, H
MOV C, L
ADD H
ADD H
ADD B
ADD H
MOV C, A
MOV B, #0
ADD B
POP {B}
B S
STRF16:
BL S
PUSH {H}
S2F162:
BCC S
CMP '.', -, '0'
BNE S
; Error translating instruction XCHG
MOV C, #F16FDL
BL S
MOV A, #('F16FDL', '+', '1')
SUB C, C, #1
BEQ S
MOV C, A
PUSH {B}
BL I
; Error translating instruction XTHL
MOV H, #0
ADD H
LDR R2, [ADR], STR R2, [DE] D, =F16X10
ADD D
MOV E, M
ADD H
MOV D, M
POP {H}
BL F
S2F161:
BL I
POP {D}
B F
INTSTR:
CMP ', 0, '
BEQ F
LDR R2, [ADR], STR R2, [DE] B, =('-', '10000')
BL H
LDR R2, [ADR], STR R2, [DE] B, =('-', '1000')
BL H
FRAC3D:
BL H
LDR R2, [ADR], STR R2, [DE] B, =('-', '10')
BL H
MOV A, #'0'
ADD L, L, #1
STR A, [ADR] D
ADD D
EOR A
STR A, [ADR] D
POP {H}
; Unsupported instruction RET
HDIVB:
MOV A, #("'0'", '-', '1')
HDB1:
ADD A, A, #1
BCS H
; Error translating instruction XTHL
CMP H, H, #1
BCS H
MOV H, #'0'
STR A, [ADR] D
ADD D
HDB2:
MOV A, B
; Error translating instruction CMA
MOV B, A
MOV A, C
; Error translating instruction CMA
MOV C, A
ADD B
ADD B
POP {P}
; Unsupported instruction RET
FRAC1K:
BL I
; Error translating instruction XCHG
POP {H}
BL F
; Error translating instruction XCHG
LDR HL, [ADR] F16X10, +, 6
B F
F16STR:
ORR A
B F
MOV A, #'-'
STR A, [ADR] D
ADD D
BL F
F16S1:
LDR R2, [ADR], STR R2, [DE] D, =F16_10
BL F
POP {D}
PUSH {P}
PUSH {H}
PUSH {D}
BL F
POP {D}
MOV A, #'1'
BL I
MOV A, #'.'
STR A, [ADR] D
ADD D
; Error translating instruction XCHG
; Error translating instruction XTHL
; Error translating instruction XCHG
BL F
POP {D}
PUSH {H}
PUSH {D}
BL F
POP {D}
MOV A, #'0'
BL I
; Error translating instruction XCHG
; Error translating instruction XTHL
; Error translating instruction XCHG
BL F
BL F
POP {D}
POP {P}
BCC F
MOV A, #'0'
BL I
; Directive DB 3, E, H
F16S3:
F16S2:
LDR A, [ADR] D
SUB ', 0, '
BEQ F
SUB '.', -, '0'
BNE F
STR A, [ADR] D
F16S4:
; Unsupported instruction RET
A2F16:
MOV B, #0
LDR R2, [ADR], STR R2, [DE] H, =A2F16T
ADD B
MOV A, M
; Error translating instruction RAR
MOV H, A
MOV A, B
; Error translating instruction RAR
MOV L, A
; Unsupported instruction RET
A2F16T:
F16X10:
BDSTR:
BL H
MOV A, L
BL H
MOV A, #' '
BL C
LDR R2, [ADR], STR R2, [DE] D, =BUFFER
PUSH {D}
BL F
MOV A, #13
STR A, [ADR] D
ADD D
MOV A, #10
STR A, [ADR] D
ADD D
MOV A, #'$'
STR A, [ADR] D
POP {D}
MOV C, #9
B B
HEXBYTE:
; Error translating instruction RRC
; Error translating instruction RRC
; Error translating instruction RRC
; Error translating instruction RRC
BL H
POP {P}
HEXNBL:
ADD ', 0, '
CMP ', :, '
BCS C
ADD 7
CHR:
PUSH {D}
PUSH {H}
MOV C, #2
MOV E, A
BL B
POP {H}
POP {D}
POP {B}
; Unsupported instruction RET
F16TST:
BL S
BL B
LDR R2, [ADR], STR R2, [DE] H, =STR_E
BL S
BL B
LDR R2, [ADR], STR R2, [DE] H, =STR_42_5
BL S
BL B
LDR R2, [ADR], STR R2, [DE] H, =STR_N
BL S
BL B
LDR R2, [ADR], STR R2, [DE] H, =0400H
BL B
LDR R2, [ADR], STR R2, [DE] H, =('F16_1', '-', '1')
BL B
LDR R2, [ADR], STR R2, [DE] H, =('F16_1', '+', '1')
BL B
LDR R2, [ADR], STR R2, [DE] H, =F16_1
LDR R2, [ADR], STR R2, [DE] D, =4200H
BL F
BL B
; Error translating instruction HLT
STR_PI:
STR_E:
STR_42_5:
STR_N:
BUFFER: