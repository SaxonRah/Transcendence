from maps.I8080_M0Plus_Mappings import combined_mapping

unrecognized = []


def translate_8080_to_m0plus(given_instruction, next_instruction=None):
    instruction = ''
    value_a = ''
    value_b = ''
    value_c = ''

    # Split instruction into components
    components = given_instruction.split()
    print("8080 Components:", components)

    # Instruction mapping dictionary
    mapping = combined_mapping
    try:
        try:
            if components[0]:
                instruction = components[0]
        except Exception as exception:
            #  print(exception)
            ...
        try:
            if components[1]:
                value_a = components[1]
        except Exception as exception:
            #  print(exception)
            ...
        try:
            if components[2]:
                value_b = components[2]
        except Exception as exception:
            #  print(exception)
            ...
        try:
            if components[3]:
                value_c = components[3]
        except Exception as exception:
            #  print(exception)
            ...

        # Translate instruction
        if instruction in mapping:
            mnemonic = mapping[instruction]

            translation = ""

            if instruction == "MOV":
                if len(components) == 3 and ',' in value_a:
                    register = value_a.split(',')
                    register = register[0]
                    address = value_b.strip("[]")
                    translation = f"{mnemonic} {register}, {address}"
                    return translation
                else:
                    print("\t\tTranslation:", translation)
                    return "Invalid MOV instruction format"
            elif instruction == "XCHG":
                if len(components) == 3 and ',' in value_a:
                    return f"{mnemonic} A, B"
                else:
                    return "Invalid XCHG instruction format"
            elif instruction == "RLC":
                if len(components) == 1:
                    return f"{mnemonic} A"
                else:
                    return "Invalid RLC instruction format"
            elif instruction == "SET":
                if len(components) == 3 and value_a.isdigit():
                    bit = int(value_a)
                    return f"{mnemonic} {value_b}, {value_b}, #{1 << bit}"
                else:
                    return "Invalid SET instruction format"
            elif instruction == "MVI":
                if len(components) == 3:
                    register, value = value_a, value_b
                    return f"{mnemonic} {register}, #{value}"
                else:
                    return "Invalid MVI instruction format"
            elif instruction == "MUL":
                if len(components) == 2:
                    return f"{mnemonic} A, {value_a}"
                else:
                    return "Invalid MUL instruction format"
            elif instruction in ["ADD", "SUB", "INC", "DEC", "AND", "OR", "XOR", "CMP"]:
                if len(components) == 3:
                    value_a = value_a.strip(",")
                    return f"{mnemonic} {value_a}, {value_b}"
                else:
                    return f"Invalid {instruction} instruction format"
            else:
                return f"\tTranslation {instruction} not implemented"
        else:
            if instruction != '':
                if instruction not in unrecognized:
                    unrecognized.append(instruction)
                return f"\t\tInstruction {instruction} not recognized"
            else:
                ...

    except Exception as exception:
        print(exception)
    finally:
        if len(unrecognized) > 0:
            unrecognized_instruction_print = f'"Unrecognized:", {unrecognized}'
            print(unrecognized_instruction_print)


def test_translate_8080_to_m0_plus():
    print("test_translate_8080_to_M0Plus:")
    instructions_8080 = [
        # MOV test
        "MOV A, @DPTR",
        "MOV A, [HL]",
        "MOV A, [2345H]",
        "MOV A",  # Malformed instruction
        "MOV",  # Malformed instruction

        # XCHG test
        "XCHG A, B",
        "XCHG",  # Malformed instruction
        "XCHG A, B, C",  # Malformed instruction

        # RLC test
        "RLC",
        "RLC A, B",  # Malformed instruction

        # SET test
        "SET 3, C",
        "SET C, 3",  # Malformed instruction
        "SET 3",  # Malformed instruction

        # MVI test
        "MVI B, 10H",
        "MVI C, 20H",
        "MVI B",  # Malformed instruction

        # MUL test
        "MUL B",
        "MUL C",
        "MUL B, C",  # Malformed instruction

        # Additional tests
        "ADD A, B",
        "ADD A",  # Malformed instruction

        "SUB A, B",
        "SUB A",  # Malformed instruction

        "INC D",
        "INC",  # Malformed instruction

        "DEC A",
        "DEC",  # Malformed instruction

        "OR A, B",
        "OR A",  # Malformed instruction

        "XOR A, B",
        "XOR B",  # Malformed instruction

        "CMP A, B",
        "CMP A",  # Malformed instruction

    ]

    for i, inst in enumerate(instructions_8080):
        lookahead_instruction = instructions_8080[i + 1] if i + 1 < len(instructions_8080) else None
        print("Instruction to translate:\n\t", inst)
        print("\t", translate_8080_to_m0plus(inst, lookahead_instruction), "\n")


if __name__ == "__main__":
    test_translate_8080_to_m0_plus()
