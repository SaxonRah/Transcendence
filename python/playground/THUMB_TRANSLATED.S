; Directive ORG 1, 0, 0, H
; Unsupported instruction JMP
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
; Unsupported instruction ANA
; Unsupported instruction ORA
; Unsupported instruction RZ
; Unsupported instruction XCHG
MOV A, #('F16SM', '-', '1')
; Unsupported instruction ANA
; Unsupported instruction ORA
; Unsupported instruction RZ
; Unsupported instruction PUSH
MOV A, H
; Unsupported instruction XRA
MOV L, A
; Unsupported instruction XTHL
BL F
SUB C
; Unsupported instruction JNC
MOV B, C
; Unsupported instruction CMA
ADD A, A, #1
MOV C, A
; Unsupported instruction XCHG
; Unsupported instruction XTHL
MOV A, H
; Unsupported instruction XRA
MOV H, A
; Unsupported instruction XTHL
MOV A, C
F16A1:
MOV C, A
BL D
; Unsupported instruction POP
MOV C, A
; Unsupported instruction CM
; Unsupported instruction DAD
MOV D, C
; Unsupported instruction JP
; Unsupported instruction JC
BL N
MOV A, #F16SM
; Unsupported instruction XRA
MOV D, A
F16NRP:
; Unsupported instruction RC
F16PCK:
; Unsupported instruction ANA
MOV H, A
MOV A, B
; Unsupported instruction RLC
; Unsupported instruction RLC
; Unsupported instruction CPI
; Unsupported instruction JNC
; Unsupported instruction ORA
MOV H, A
F16SGN:
; Unsupported instruction ANA
; Unsupported instruction ORA
MOV H, A
BX LR
F16UNP:
BL F
MOV C, B
; Unsupported instruction XCHG
F16UPH:
; Unsupported instruction ANA
; Unsupported instruction RRC
; Unsupported instruction RRC
MOV B, A
MOV A, #F16MM
; Unsupported instruction ANA
; Unsupported instruction ORI
MOV H, A
MOV A, B
; Unsupported instruction ORA
; Unsupported instruction RNZ
MOV A, #F16MI1
; Unsupported instruction XRA
MOV H, A
MOV A, B
BX LR
F16DNP:
LDR H, =F16PCK
; Unsupported instruction XTHL
MOV A, #('F16MI1', '+', 'F16MI1')
; Unsupported instruction ANA
; Unsupported instruction RZ
DIV2X2:
DIV2X1:
DIV2XC:
; Unsupported instruction ORA
; Unsupported instruction RZ
; Unsupported instruction CPI
; Unsupported instruction JNC
DIV2C1:
; Unsupported instruction ORA
; Unsupported instruction RAR
MOV H, A
MOV A, L
; Unsupported instruction RAR
MOV L, A
SUB C, C, #1
; Unsupported instruction JNZ
; Unsupported instruction RNC
; Unsupported instruction INX
MOV A, #('F16MI1', '+', 'F16MI1')
; Unsupported instruction ANA
; Unsupported instruction RZ
; Unsupported instruction JMP
F16NRM:
; Unsupported instruction ORA
; Unsupported instruction STC
; Unsupported instruction RZ
MOV A, B
; Unsupported instruction ORA
; Unsupported instruction RZ
F16N1:
; Unsupported instruction ANA
; Unsupported instruction RNZ
; Unsupported instruction DAD
SUB B, B, #1
; Unsupported instruction JNZ
BX LR
F16MUL:
; Unsupported instruction ANA
; Unsupported instruction ORA
; Unsupported instruction RZ
; Unsupported instruction XCHG
MOV A, #('F16SM', '-', '1')
; Unsupported instruction ANA
; Unsupported instruction ORA
; Unsupported instruction RZ
MOV A, H
; Unsupported instruction XRA
; Unsupported instruction PUSH
BL F
ADD C
; Unsupported instruction SUI
; Unsupported instruction JC
; Unsupported instruction JZ
; Unsupported instruction CPI
; Unsupported instruction JNC
; Unsupported instruction PUSH
MOV B, H
MOV C, L
LDR H, =0
MOV A, #F16MB
F16M1:
MOV A, H
; Unsupported instruction ORA
; Unsupported instruction RAR
MOV H, A
MOV A, L
; Unsupported instruction RAR
MOV L, A
MOV A, B
; Unsupported instruction RAR
MOV B, A
MOV A, C
; Unsupported instruction RAR
MOV C, A
; Unsupported instruction JNC
; Unsupported instruction DAD
F16M2:
SUB A, A, #1
; Unsupported instruction JNZ
; Unsupported instruction POP
; Unsupported instruction POP
; Unsupported instruction JMP
F16DIV:
; Unsupported instruction XRA
; Unsupported instruction PUSH
MOV A, #('F16SM', '-', '1')
; Unsupported instruction ANA
; Unsupported instruction ORA
; Unsupported instruction JZ
MOV A, #('F16SM', '-', '1')
; Unsupported instruction ANA
; Unsupported instruction ORA
; Unsupported instruction JZ
BL F
SUB C
; Unsupported instruction ADI
; Unsupported instruction JM
; Unsupported instruction JZ
; Unsupported instruction CPI
; Unsupported instruction JNC
; Unsupported instruction PUSH
BL F
; Unsupported instruction JNC
; Unsupported instruction DAD
; Unsupported instruction XTHL
SUB H, H, #1
; Unsupported instruction XTHL
F16D3:
BL N
MOV A, #('F16MB', '+', '1')
LDR B, =0
F16D1:
; Unsupported instruction PUSH
; Unsupported instruction DAD
; Unsupported instruction JNC
; Unsupported instruction XCHG
F16D2:
MOV A, C
; Unsupported instruction RAL
MOV C, A
MOV A, B
; Unsupported instruction RAL
MOV B, A
; Unsupported instruction XCHG
; Unsupported instruction DAD
; Unsupported instruction XCHG
; Unsupported instruction POP
SUB A, A, #1
; Unsupported instruction JNZ
MOV H, B
MOV L, C
; Unsupported instruction POP
; Unsupported instruction POP
MOV A, #('F16MI1', '+', 'F16MI1')
; Unsupported instruction ANA
; Unsupported instruction CNZ
; Unsupported instruction JMP
F16SQR:
F16RND:
F16ABS:
; Unsupported instruction ORA
; Unsupported instruction RP
F16NEG:
; Unsupported instruction XRA
MOV H, A
BX LR
F16CMP:
; Unsupported instruction ANA
MOV B, A
MOV A, #F16EM
; Unsupported instruction ANA
; Unsupported instruction CMP
; Unsupported instruction RNZ
F16CPM:
; Unsupported instruction ANA
MOV B, A
MOV A, #F16MM
; Unsupported instruction ANA
; Unsupported instruction CMP
; Unsupported instruction RNZ
MOV A, L
; Unsupported instruction CMP
BX LR
F16OFL:
F16INF:
MOV L, #0
; Unsupported instruction JMP
F16ZRS:
F16ZRO:
BX LR
F16INT:
LDR H, =0
MOV A, #F16EM
; Unsupported instruction ANA
; Unsupported instruction RRC
; Unsupported instruction RRC
; Unsupported instruction SUI
; Unsupported instruction RC
ADD A, A, #1
MOV B, A
MOV A, #F16MI1
; Unsupported instruction ORA
MOV D, A
; Unsupported instruction PUSH
F162I1:
MOV A, #F16MI1
; Unsupported instruction ANA
; Unsupported instruction JZ
; Unsupported instruction INX
F162I2:
; Unsupported instruction DAD
; Unsupported instruction XCHG
SUB B, B, #1
; Unsupported instruction JNZ
; Unsupported instruction POP
; Unsupported instruction RP
NEG16:
; Unsupported instruction CMA
MOV L, A
MOV A, H
; Unsupported instruction CMA
MOV H, A
; Unsupported instruction INX
BX LR
INTF16:
; Unsupported instruction ORA
; Unsupported instruction RZ
LDR B, =F16PCK
; Unsupported instruction PUSH
MOV B, #('F16MB', '+', 'F16BIA', '-', '1')
MOV D, #0
MOV A, H
; Unsupported instruction CPI
; Unsupported instruction JC
MOV C, #('16', '-', 'F16MB', '+', '1')
I2F161:
; Unsupported instruction RLC
; Unsupported instruction JNC
MOV A, B
ADD C
MOV B, A
; Unsupported instruction JMP
STRINT:
; Unsupported instruction XCHG
S2I2:
S2I1:
; Unsupported instruction INX
; Unsupported instruction ORA
; Unsupported instruction RZ
; Unsupported instruction SUI
; Unsupported instruction RC
; Unsupported instruction CPI
; Unsupported instruction RNC
SUB C, C, #1
; Unsupported instruction JZ
; Unsupported instruction PUSH
MOV B, H
MOV C, L
; Unsupported instruction DAD
; Unsupported instruction DAD
; Unsupported instruction DAD
; Unsupported instruction DAD
MOV C, A
MOV B, #0
; Unsupported instruction DAD
; Unsupported instruction POP
; Unsupported instruction JMP
STRF16:
BL S
; Unsupported instruction PUSH
S2F162:
; Unsupported instruction JNC
; Unsupported instruction CPI
; Unsupported instruction JNZ
; Unsupported instruction XCHG
MOV C, #F16FDL
BL S
MOV A, #('F16FDL', '+', '1')
SUB C
; Unsupported instruction JZ
MOV C, A
; Unsupported instruction PUSH
BL I
; Unsupported instruction XTHL
MOV H, #0
; Unsupported instruction DAD
LDR D, =F16X10
; Unsupported instruction DAD
MOV E, M
; Unsupported instruction INX
MOV D, M
; Unsupported instruction POP
BL F
S2F161:
BL I
; Unsupported instruction POP
; Unsupported instruction JMP
INTSTR:
; Unsupported instruction CPI
; Unsupported instruction JZ
LDR B, =('-', '10000')
BL H
LDR B, =('-', '1000')
BL H
FRAC3D:
BL H
LDR B, =('-', '10')
BL H
MOV A, #'0'
ADD L
; Unsupported instruction STAX
; Unsupported instruction INX
; Unsupported instruction XRA
; Unsupported instruction STAX
; Unsupported instruction POP
BX LR
HDIVB:
MOV A, #("'0'", '-', '1')
HDB1:
ADD A, A, #1
; Unsupported instruction JC
; Unsupported instruction XTHL
; Unsupported instruction CMP
; Unsupported instruction JC
MOV H, #'0'
; Unsupported instruction STAX
; Unsupported instruction INX
HDB2:
MOV A, B
; Unsupported instruction CMA
MOV B, A
MOV A, C
; Unsupported instruction CMA
MOV C, A
; Unsupported instruction INX
; Unsupported instruction DAD
; Unsupported instruction POP
BX LR
FRAC1K:
BL I
; Unsupported instruction XCHG
; Unsupported instruction POP
BL F
; Unsupported instruction XCHG
; Unsupported instruction LHLD
; Unsupported instruction JMP
F16STR:
; Unsupported instruction ORA
; Unsupported instruction JP
MOV A, #'-'
; Unsupported instruction STAX
; Unsupported instruction INX
BL F
F16S1:
LDR D, =F16_10
BL F
; Unsupported instruction POP
; Unsupported instruction PUSH
; Unsupported instruction PUSH
; Unsupported instruction PUSH
BL F
; Unsupported instruction POP
MOV A, #'1'
BL I
MOV A, #'.'
; Unsupported instruction STAX
; Unsupported instruction INX
; Unsupported instruction XCHG
; Unsupported instruction XTHL
; Unsupported instruction XCHG
BL F
; Unsupported instruction POP
; Unsupported instruction PUSH
; Unsupported instruction PUSH
BL F
; Unsupported instruction POP
MOV A, #'0'
BL I
; Unsupported instruction XCHG
; Unsupported instruction XTHL
; Unsupported instruction XCHG
BL F
BL F
; Unsupported instruction POP
; Unsupported instruction POP
; Unsupported instruction JNC
MOV A, #'0'
BL I
; Directive DB 3, E, H
F16S3:
F16S2:
; Unsupported instruction LDAX
; Unsupported instruction SUI
; Unsupported instruction JZ
; Unsupported instruction SUI
; Unsupported instruction JNZ
; Unsupported instruction STAX
F16S4:
BX LR
A2F16:
MOV B, #0
LDR H, =A2F16T
; Unsupported instruction DAD
MOV A, M
; Unsupported instruction RAR
MOV H, A
MOV A, B
; Unsupported instruction RAR
MOV L, A
BX LR
A2F16T:
F16X10:
BDSTR:
BL H
MOV A, L
BL H
MOV A, #' '
BL C
LDR D, =BUFFER
; Unsupported instruction PUSH
BL F
MOV A, #13
; Unsupported instruction STAX
; Unsupported instruction INX
MOV A, #10
; Unsupported instruction STAX
; Unsupported instruction INX
MOV A, #'$'
; Unsupported instruction STAX
; Unsupported instruction POP
MOV C, #9
; Unsupported instruction JMP
HEXBYTE:
; Unsupported instruction RRC
; Unsupported instruction RRC
; Unsupported instruction RRC
; Unsupported instruction RRC
BL H
; Unsupported instruction POP
HEXNBL:
; Unsupported instruction ADI
; Unsupported instruction CPI
; Unsupported instruction JC
; Unsupported instruction ADI
CHR:
; Unsupported instruction PUSH
; Unsupported instruction PUSH
MOV C, #2
MOV E, A
BL B
; Unsupported instruction POP
; Unsupported instruction POP
; Unsupported instruction POP
BX LR
F16TST:
BL S
BL B
LDR H, =STR_E
BL S
BL B
LDR H, =STR_42_5
BL S
BL B
LDR H, =STR_N
BL S
BL B
LDR H, =0400H
BL B
LDR H, =('F16_1', '-', '1')
BL B
LDR H, =('F16_1', '+', '1')
BL B
LDR H, =F16_1
LDR D, =4200H
BL F
BL B
B .
STR_PI:
STR_E:
STR_42_5:
STR_N:
BUFFER: