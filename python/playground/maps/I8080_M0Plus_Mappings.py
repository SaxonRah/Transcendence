#  Intel 8080 translation mapping for M0Plus
#  The mapping provided is FROM Intel 8080 instructions TO ARM M0+ instructions.
#  Each key in the dictionary represents an Intel 8080 instruction.
#  Its corresponding value represents the ARM M0+ instruction(s) it should be translated to.

mapping_misc_control = {
    "NOP": "NOP",
    "HLT": "NOP",           # Placeholder for HLT instruction
    "RIM": "NOP",           # Placeholder for RIM instruction
    "SIM": "NOP",           # Placeholder for SIM instruction
    "EI": "CPSIE i",        # Enable interrupts
    "DI": "CPSID i",        # Disable interrupts
    "PCHL": "MOV PC, HL",
    "SPHL": "MOV SP, HL",
    "LHLD": "LDR HL, [ADR]",
    "SHLD": "STR HL, [ADR]",
    "XTHL": "LDR R3, [SP], MOV R2, SP, STR R2, [HL], MOV SP, R3",
    "XCHG": "MOV R2, HL, MOV HL, DE, MOV DE, R2"
}

mapping_jumps_calls = {
    "JMP": "B",
    "JC": "BCS",
    "JNC": "BCC",
    "JM": "BMI",
    "JZ": "BEQ",
    "JNZ": "BNE",
    "JP": "B",              # Placeholder for Branch instruction
    # "JP": "BPL", It should be noted here, that many instructions depend on following instructions.
    #
    "CALL": "BL",
    "CC": "BCS",
    "CNC": "BCC",
    "CP": "BPL",
    "CM": "BMI",
    "CZ": "BEQ",
    "CNZ": "BNE",
}

mapping_8bit_load_store_move = {
    "MOV": "MOV",
    "MVI": "MOV",
    "SPHL": "MOV SP, HL",

    "LDA": "LDR A, [ADR]",
    "LXI": "LDR DE, [ADR]",
    "LDAX": "LDR A, [ADR]",
    "LHLD": "LDR HL, [ADR]",

    "STA": "STR A, [ADR]",
    "STAX": "STR A, [ADR]",
    "SHLD": "STR HL, [ADR]",
}

mapping_16bit_load_store_move = {
    "PUSH": "PUSH",
    "POP": "POP",
    "LDAX": "LDR A, [ADR]",
    "STAX": "STR A, [ADR]",
    "LXI": "LDR R2, [ADR], STR R2, [DE]",
}

mapping_8bit_arithmetic_logical = {
    "ADD": "ADD",
    "ADI": "ADD",
    "DAD": "ADD",
    "ANA": "AND",
    "ANI": "AND",
    "INR": "ADD",
    "INX": "ADD",
    "SUB": "SUB",
    "SUI": "SUB",
    "DCR": "SUB",
    "DCX": "SUB",
    "CMP": "CMP",
    "CPI": "CMP",
    "XRA": "EOR",
    "XRI": "EOR",
    "ORA": "ORR",
    "ORI": "ORR",
    "RLC": "ROR",
    "RRC": "ROR",
    "RAL": "ROR",
    "RAR": "ROR",
    "CMA": "MVN",
}

mapping_16bit_arithmetic_logical = {
    "DAD": "ADD"
}


combined_mapping = {}
combined_mapping.update(mapping_misc_control)
combined_mapping.update(mapping_jumps_calls)
combined_mapping.update(mapping_8bit_load_store_move)
combined_mapping.update(mapping_16bit_load_store_move)
combined_mapping.update(mapping_8bit_arithmetic_logical)
combined_mapping.update(mapping_16bit_arithmetic_logical)


old_mapping = {
    "NOP": "NOP",        # No operation
    "HLT": "NOP",        # Halt processor
    "STC": "ORRS",       # Set carry flag
    "RST": "B",          # Restart
    "SPHL": "MOV",       # Stack pointer to HL
    "DI": "NOP",         # Disable interrupts
    "EI": "NOP",         # Enable interrupts
    "XCHG": "MOV",       # Exchange registers
    "XTHL": "MOV",       # Exchange stack top with HL
    "STA": "STR",        # Store accumulator direct
    "STAX": "STR",       # Store accumulator indirect
    "LXI": "LDR",        # Load immediate register pair
    "LDA": "LDR",        # Load accumulator direct
    "LDAX": "LDR",       # Load accumulator indirect
    "INR": "ADD",        # Increment register
    "INX": "ADD",        # Increment register pair
    "DCR": "SUB",        # Decrement register
    "DCX": "SUB",        # Decrement register pair
    "MOV": "MOV",        # Move data between registers
    # "MOV": "LDR",        # Move to/from external device
    "MVI": "MOV",        # Move immediate data
    "RAR": "ROR",        # Rotate right
    "RAL": "ROR",        # Rotate left
    "RRC": "ROR",        # Rotate right through carry
    "RLC": "ROR",        # Rotate left through carry
    "CMA": "MVN",        # Complement accumulator
    "CMC": "EOR",        # Complement carry flag
    "DAD": "ADD",        # Add Double
    "ADI": "ADD",        # Add immediate to accumulator
    "ACI": "ADC",        # Add immediate to accumulator with carry
    "ADD": "ADD",        # Add register to accumulator
    "ADC": "ADC",        # Add register to accumulator with carry
    "SUI": "SUB",        # Subtract immediate from accumulator
    "SUB": "SUB",        # Subtract register from accumulator
    "SBB": "SBC",        # Subtract register from accumulator with borrow
    "ANI": "AND",        # Logical AND immediate with accumulator
    "ANA": "AND",        # Logical AND register with accumulator
    "ORI": "ORR",        # Logical OR immediate with accumulator
    "ORA": "ORR",        # Logical OR register with accumulator
    "XRI": "EOR",        # Logical exclusive OR immediate with accumulator
    "XRA": "EOR",        # Logical exclusive OR register with accumulator
    "POP": "POP",        # Pop from stack
    "PUSH": "PUSH",      # Push onto stack
    "OUT": "STR",        # Output
    "CPI": "CMP",        # Compare immediate with accumulator
    "CMP": "CMP",        # Compare register with accumulator
    "JMP": "B",          # Jump
    "JZ": "BEQ",         # Jump if zero
    "JM": "BMI",         # Jump if minus
    "JP": "BPL",         # Jump if plus
    "JPE": "BVS",        # Jump if parity even
    "JPO": "BVC",        # Jump if parity odd
    "JNZ": "BNE",        # Jump if not zero
    "JN": "BVC",         # Jump if not parity odd
    "JNC": "BCC",        # Jump if not carry
    "CZ": "BEQ",         # Call if zero
    "CM": "BMI",         # Call if minus
    "CP": "CMP",         # Call if plus
    "CNC": "BCC",        # Call if not carry
    "CNZ": "BNE",        # Call if not zero
    "CN": "BVC",         # Call if not parity odd
    "RET": "BX LR",      # Return
    "RZ": "BEQ",         # Return if zero
    "RP": "BPL",         # Return if plus
    "RPE": "BVS",        # Return if parity even
    "RPO": "BVS",        # Return if parity odd
    "RNZ": "BNE",        # Return if not zero
    "RNC": "BCC",        # Return if not carry
    "RN": "BVC",         # Return if not parity odd
}


MOV_INSTRUCTIONS = {
    """
    MOV B,B
    MOV B,C
    MOV B,D
    MOV B,E
    MOV B,H
    MOV B,L
    MOV B,M
    MOV B,A
    MOV C,B
    MOV C,C
    MOV C,D
    MOV C,E
    MOV C,H
    MOV C,L
    MOV C,M
    MOV C,A
    MOV D,B
    MOV D,C
    MOV D,D
    MOV D,E
    MOV D,H
    MOV D,L
    MOV D,M
    MOV D,A
    MOV E,B
    MOV E,C
    MOV E,D
    MOV E,E
    MOV E,H
    MOV E,L
    MOV E,M
    MOV E,A
    MOV H,B
    MOV H,C
    MOV H,D
    MOV H,E
    MOV H,H
    MOV H,L
    MOV H,M
    MOV H,A
    MOV L,B
    MOV L,C
    MOV L,D
    MOV L,E
    MOV L,H
    MOV L,L
    MOV L,M
    MOV L,A
    MOV M,B
    MOV M,C
    MOV M,D
    MOV M,E
    MOV M,H
    MOV M,L
    MOV M,A
    MOV A,B
    MOV A,C
    MOV A,D
    MOV A,E
    MOV A,H
    MOV A,L
    MOV A,M
    MOV A,A
    """
}
