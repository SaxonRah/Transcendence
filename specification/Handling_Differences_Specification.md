# Handling Differences a Specification
Handling differences in instruction formats, addressing modes, and operand types between Intel 8080 and Arm M0+ architectures requires a thorough understanding of each architecture's specifications and capabilities. By carefully managing instruction formats, addressing modes, and operand types, Transcendence can achieve accurate and efficient translation. Enabling seamless porting of legacy code to modern Arm-based platforms.

To handle these differences effectively, Transcendence may employ techniques such as:
- Opcode mapping tables to translate between Intel 8080 and Arm M0+ instructions.
- Addressing mode conversion routines to transform Intel 8080 addressing modes into equivalent Arm M0+ addressing modes.
- Operand size adjustment mechanisms to align operand sizes between the two architectures.
- Conditional translation logic to handle architecture-specific features or instruction variations.


Here's an overview of how these differences can be managed:

1. **Instruction Formats:**
   - Intel 8080 instructions typically consist of an opcode followed by zero or more operands. Instructions can vary in length, ranging from one to three bytes.
   - Arm M0+ instructions follow a fixed-length format, typically encoded in 16 or 32 bits. Instructions may include fields for opcode, operands, addressing modes, and condition codes.
   - To handle differences in instruction formats, Transcendence needs to map each Intel 8080 instruction to its equivalent Arm M0+ instruction. This mapping involves considering opcode mappings, operand sizes, and any necessary adjustments to accommodate the fixed-length format of Arm instructions.
```python
# Define opcode mappings between Intel 8080 and Arm M0+
opcode_mapping = {
    'MOV': {'arm_opcode': 'MOV', 'num_operands': 2},  # Example: 'MOV' instruction remains the same
    'ADD': {'arm_opcode': 'ADD', 'num_operands': 2},  # Example: 'ADD' instruction remains the same
    # More mappings...
}

# Translate Intel 8080 instruction to Arm M0+ instruction
def translate_instruction(intel_opcode):
    mapping = opcode_mapping.get(intel_opcode, None)
    if mapping:
        return mapping['arm_opcode'], mapping['num_operands']
    else:
        return None, None

# Example usage
intel_opcode = 'MOV'
arm_opcode, num_operands = translate_instruction(intel_opcode)
print(f"Translated '{intel_opcode}' to '{arm_opcode}' with {num_operands} operands")
```

2. **Addressing Modes:**
   - Intel 8080 supports various addressing modes, including immediate, direct, indirect, indexed, and register-based addressing modes.
   - Arm M0+ utilizes a simplified set of addressing modes compared to Intel 8080, typically supporting immediate, register-direct, and offset addressing modes.
   - Transcendence needs to translate Intel 8080 addressing modes into equivalent Arm M0+ addressing modes. This may involve converting indirect or indexed addressing modes to register-based or offset addressing modes compatible with the Arm architecture.
```python
# Define addressing mode mappings between Intel 8080 and Arm M0+
addressing_mode_mapping = {
    'IMM': {'arm_mode': 'IMM', 'size_bytes': 2},    # Immediate addressing mode
    'DIR': {'arm_mode': 'REG', 'size_bytes': 1},    # Direct addressing mode maps to register-direct in Arm M0+
    'IND': {'arm_mode': 'IND', 'size_bytes': 2},    # Indirect addressing mode remains the same
    'IDX': {'arm_mode': 'OFF', 'size_bytes': 2},    # Indexed addressing mode maps to offset addressing mode
    # More mappings...
}

# Translate addressing mode from Intel 8080 to Arm M0+
def translate_addressing_mode(intel_mode):
    mapping = addressing_mode_mapping.get(intel_mode, None)
    if mapping:
        return mapping['arm_mode'], mapping['size_bytes']
    else:
        return None, None

# Example usage
intel_mode = 'IDX'
arm_mode, size_bytes = translate_addressing_mode(intel_mode)
print(f"Translated '{intel_mode}' to '{arm_mode}' with a size of {size_bytes} bytes")
```

3. **Operand Types:**
   - Intel 8080 instructions can operate on various data types, including bytes, words, and memory addresses. Operand sizes can vary depending on the instruction.
   - Arm M0+ instructions typically operate on fixed-size data types, such as 8-bit bytes or 32-bit words. Operand sizes are specified by the instruction encoding.
   - Transcendence must ensure compatibility between operand types in Intel 8080 instructions and the corresponding data types supported by Arm M0+. This may involve sign extension, data truncation, or type conversion as necessary.
```python
# Define operand mappings between Intel 8080 and Arm M0+
operand_mapping = {
    'Register': {
        'A': 'R0', 'B': 'R1', 'C': 'R2', 'D': 'R3', 'E': 'R4',
        'H': 'R5', 'L': 'R6', 'M': 'R7',  # 'M' represents memory location pointed to by HL
        # Additional mappings...
    },
    'Register Pair': {
        'B': 'R1R2', 'D': 'R3R4', 'H': 'R5R6',  # Register pairs BC, DE, HL
        # Additional mappings...
    },
    'Immediate Data': {
        'Hexadecimal': {'arm_type': 'HEX', 'size_bits': 8},  # Example: Immediate data in hexadecimal format
        'Decimal': {'arm_type': 'DEC', 'size_bits': 8},      # Immediate data in decimal format
        'Octal': {'arm_type': 'OCT', 'size_bits': 8},        # Immediate data in octal format
        'Binary': {'arm_type': 'BIN', 'size_bits': 8},       # Immediate data in binary format
        # Additional mappings...
    },
    '16-bit Memory Address': {
        # Define mappings for addressing modes or specify how memory addresses are represented in Arm M0+ assembly
        # Example: 'LABEL' in Intel 8080 can be translated to 'LABEL' or its corresponding memory address in Arm M0+
        # Additional mappings...
    }
}

# Translate operand from Intel 8080 to Arm M0+
def translate_operand(intel_operand_type, intel_operand_value):
    if intel_operand_type in operand_mapping:
        mappings = operand_mapping[intel_operand_type]
        if intel_operand_value in mappings:
            return mappings[intel_operand_value]
        else:
            # Handle cases like expressions, labels, or other custom operand types
            # Example: Evaluate expressions, resolve labels, or apply custom translation rules
            # Additional logic...
            return None
    else:
        # Handle unsupported operand types or invalid values
        # Additional logic...
        return None

# Example usage
intel_operand_type = 'Immediate Data'
intel_operand_value = 'Hexadecimal'
arm_operand = translate_operand(intel_operand_type, intel_operand_value)
print(f"Translated '{intel_operand_value}' to '{arm_operand}'")
```

# Mapping
When mapping 8080 assembly instructions to ARM Thumb (specifically ARM Cortex-M0+) assembly instructions, we need to take into account that the architectures are quite different, so the mapping is not always direct and might require several ARM instructions to achieve the same result as a single 8080 instruction.

### Registers
The Intel 8080 has the following registers: A, B, C, D, E, H, L, SP (Stack Pointer), and PC (Program Counter).

The ARM Cortex-M0+ uses the following registers: R0-R7 (general-purpose "low registers"), SP (R13) (Stack Pointer), LR (R14) (Link Register), and PC (R15) (Program Counter), in addition to R8-R12 (high registers). If we map them directly, this will net us an extra/unused single low register R7, the link register LR, and all high registers R8-R12.
- A -> R0
- B -> R1
- C -> R2
- D -> R3
- E -> R4
- H -> R5
- L -> R6
- SP -> SP (both use SP for stack pointer)
- PC -> PC (both use PC for program counter)

### Instructions
Most instructions can be mapped directly, however, since the M0+ is a RISC architecture and the 8080 is a CISC architecture, we will need to map several ARM instructions to a single 8080 instruction.

The blocks below might contain missing and incorrect instrcutions/registers/formatting, it has only gone over once or twice and mostly from memory. I will update this in the future to align with the quick reference cards of THUMB and 8080.

#### Data Movement
| 8080       | Description                    | ARM Thumb (M0+)                                | Notes                                            |
|------------|--------------------------------|------------------------------------------------|--------------------------------------------------|
| MOV B, C   | Move r2/C to r1/B              | MOV r1, r2                                     | Direct mapping                                   |
| MVI r, data| Move immediate to register     | MOVS r, #data                                  | Use immediate MOVS                               |
| LDA addr   | Load A from memory             | LDR R0, [addr]                                 | Load value at memory address to R0 (A)           |
| STA addr   | Store A to memory              | STR R0, [addr]                                 | Store value in R0 (A) to memory address          |
| LHLD addr  | Load H and L direct            | LDR R5, [addr]; LDR R6, [addr+1]               | Load value at addr to R5 (H) and addr+1 to R6 (L)|
| SHLD addr  | Store H and L direct           | STR R5, [addr]; STR R6, [addr+1]               | Store R5 (H) at addr and R6 (L) at addr+1        |
| LDAX rp    | Load A from address in rp pair | LDR R0, [Rn]                                   | Load from memory address in base register pair   |
| STAX rp    | Store A to address in rp pair  | STR R0, [Rn]                                   | Store to memory address in base register pair    |
| XCHG       | Exchange D and H, E and L      | MOV R3, R5; MOV R5, R3; MOV R4, R6; MOV R6, R4 | Swap R3 with R5 and R4 with R6                   |

#### Arithmetic
| 8080         | Description                    | ARM Thumb (M0+)                      | Notes                                                  |
|--------------|--------------------------------|--------------------------------------|--------------------------------------------------------|
| ADD r        | Add register to A              | ADDS R0, R0, r                       | Add r to R0 (A)                                        |
| ADI data     | Add immediate to A             | ADDS R0, R0, #data                   | Add immediate data to R0 (A)                           |
| SUB r        | Subtract register from A       | SUBS R0, R0, r                       | Subtract r from R0 (A)                                 |
| SUI data     | Subtract immediate from A      | SUBS R0, R0, #data                   | Subtract immediate data from R0 (A)                    |
| INR r        | Increment register             | ADDS r, r, #1                        | Increment r by 1                                       |
| DCR r        | Decrement register             | SUBS r, r, #1                        | Decrement r by 1                                       |
| INX rp       | Increment register pair        | ADDS rn, rn, #1                      | Increment base register of pair by 1                   |
| DCX rp       | Decrement register pair        | SUBS rn, rn, #1                      | Decrement base register of pair by 1                   |
| DAD rp       | Add register pair to HL        | ADDS R5, R5, rn;  ADCS R6, R6, rn_hi | Add base register pair to R5 (H) and R6 (L) with carry |

#### Logical
| 8080         | Description                    | ARM Thumb (M0+)                 | Notes                                           |
|--------------|--------------------------------|---------------------------------|-------------------------------------------------|
| ANA r        | Logical AND register with A    | ANDS R0, R0, r                  | AND r with R0 (A)                               |
| ANI data     | Logical AND immediate with A   | ANDS R0, R0, #data              | AND immediate data with R0 (A)                  |
| ORA r        | Logical OR register with A     | ORRS R0, R0, r                  | OR r with R0 (A)                                |
| ORI data     | Logical OR immediate with A    | ORRS R0, R0, #data              | OR immediate data with R0 (A)                   |
| XRA r        | Logical XOR register with A    | EORS R0, R0, r                  | XOR r with R0 (A)                               |
| XRI data     | Logical XOR immediate with A   | EORS R0, R0, #data              | XOR immediate data with R0 (A)                  |
| CMA          | Complement A (logical NOT)     | MVNS R0, R0                     | NOT R0 (A)                                      |

#### Control
| 8080       | Description                    | ARM Thumb (M0+)                 | Notes                                           |
|------------|--------------------------------|---------------------------------|-------------------------------------------------|
| JMP addr   | Jump to address                | B addr                          | Branch to address                               |
| JC addr    | Jump if carry                  | BCS addr                        | Branch if carry set                             |
| JNC addr   | Jump if no carry               | BCC addr                        | Branch if carry clear                           |
| JZ addr    | Jump if zero                   | BEQ addr                        | Branch if equal (zero set)                      |
| JNZ addr   | Jump if not zero               | BNE addr                        | Branch if not equal (zero clear)                |
| CALL addr  | Call subroutine at address     | BL addr                         | Branch with link (call subroutine)              |
| RET        | Return from subroutine         | BX LR                           | Branch to link register (return)                |
| HLT        | Halt processor                 | BKPT #0                         | Breakpoint (similar to halt)                    |

#### Stack Operations
| 8080       | Description                    | ARM Thumb (M0+)                 | Notes                                           |
|------------|--------------------------------|---------------------------------|-------------------------------------------------|
| PUSH rp    | Push register pair onto stack  | PUSH {rn, rn_hi}                | Push base register pair onto stack              |
| POP rp     | Pop register pair from stack   | POP {rn, rn_hi}                 | Pop base register pair from stack               |

### Example Translation
Based on the blocks above we can generate this example Thumb from example 8080.
#### 8080 Code
```assembly
LDA 0x2000       ; Load A from memory address 0x2000
INR A            ; Increment A
MOV B, A         ; Move A to B
JZ loop          ; Jump to loop if A is zero
```

#### ARM Thumb (M0+) Code
```assembly
LDR R0, =0x2000  ; Load address 0x2000 to R0
LDR R0, [R0]     ; Load value at address in R0 to R0 (A)
ADDS R0, R0, #1  ; Increment R0 (A)
MOV R1, R0       ; Move R0 (A) to R1 (B)
BEQ loop         ; Branch to loop if zero flag is set
```

# Register Pairs
On the 8080, we have access to register pairs, mapping the architectures will require careful consideration due to the fundamental differences between the two. The 8080 uses 8-bit registers and allows combining them into 16-bit register pairs for specific operations. In contrast, ARM Thumb uses 16-bit and 32-bit registers. 

### Register Pairs Mapping

Here is a mapping of 8080 register pairs to ARM Cortex-M0+ registers:

- BC (B and C) -> R1 and R2
- DE (D and E) -> R3 and R4
- HL (H and L) -> R5 and R6
- SP (Stack Pointer) -> SP (Stack Pointer)
- PC (Program Counter) -> PC (Program Counter)

This at face value would be correct, however we could pack registers and register pairs in single M0+ registers if we wanted since the space allows for it. This would require far more assembly than just wasting register space, however would result in the best space for both registers, and instruction utilization. I will not cover this efficent packing and is left up to the reader, though I will note on it.

### Example Mapping

#### 8080 to ARM Cortex-M0+ Register Pairs
| 8080 Register Pair | 8080 Individual Registers | ARM Registers |
|--------------------|---------------------------|---------------|
| BC                 | B, C                      | R1, R2        |
| DE                 | D, E                      | R3, R4        |
| HL                 | H, L                      | R5, R6        |
| SP                 | SP                        | SP            |
| PC                 | PC                        | PC            |

### Instruction Differences
Mapping instructions from 8080 to ARM Thumb (M0+) requires multiple instructions because the 8080 can operate directly on 16-bit register pairs, while ARM Cortex-M0+ cannot.

#### Example: INX (Increment Register Pair)

**8080 Assembly**
```assembly
INX H           ; Increment HL pair (H and L registers)
```

**Equivalent ARM Thumb (M0+) Assembly**
```assembly
ADDS R6, R6, #1        ; Increment L (R6)
ADCS R5, R5, #0        ; Increment H (R5) with carry
```
- **ADDS**: Adds the immediate value to the lower register (L).
- **ADCS**: Adds with carry to handle overflow from the lower register to the higher register (H).

#### Example: DCX (Decrement Register Pair)

**8080 Assembly**
```assembly
DCX B           ; Decrement BC pair (B and C registers)
```

**Equivalent ARM Thumb (M0+) Assembly**
```assembly
SUBS R2, R2, #1        ; Decrement C (R2)
SBCS R1, R1, #0        ; Subtract with carry to handle borrow from C (R2) to B (R1)
```
- **SUBS**: Subtracts the immediate value from the lower register (C).
- **SBCS**: Subtracts with carry to handle the borrow from the lower register to the higher register (B).

### Example of Complex Instruction: DAD (Double Add Register Pair to HL)

**8080 Assembly**
```assembly
DAD B           ; Add BC pair to HL pair
```

**Equivalent ARM Thumb (M0+) Assembly**
```assembly
ADDS R6, R6, R2        ; Add L (R6) and C (R2)
ADCS R5, R5, R1        ; Add H (R5) and B (R1) with carry
```
- **ADDS**: Adds the lower register (C) to the lower register (L).
- **ADCS**: Adds with carry to handle the overflow from the lower register addition to the higher registers (H and B).

### Instructions Analysis
For most 8080 instructions involving register pairs, you will need at least two ARM Thumb instructions:
1. One for the lower 8-bit register.
2. One for the higher 8-bit register, often incorporating a carry/borrow flag for proper handling of 16-bit operations.

In contrast, the 8080 often accomplishes these with a single instruction. This makes ARM Thumb assembly more verbose but also more flexible with its 32-bit architecture, offering more power and capabilities in complex operations. This still signals for the need of efficent register packing, while not covered in this document, it could be worth it to you to investigate how this could be done. The more advanced translation would reduce the wasted register space, and wasted instruction space. 

### Example Translation

#### 8080 Code
```assembly
MOV H, L        ; Move L to H
INX H           ; Increment HL pair
```

#### ARM Thumb (M0+) Code
```assembly
MOV R5, R6      ; Move L (R6) to H (R5)
ADDS R6, R6, #1 ; Increment L (R6)
ADCS R5, R5, #0 ; Increment H (R5) with carry
```
