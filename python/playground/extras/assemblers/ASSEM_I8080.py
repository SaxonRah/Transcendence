# TODO: Fix this trash.
#  So much is wrong, it's almost not even worth fixing.
#  Address mapping is the main thing to fix.
#  Ensure labels addresses are correct.
#  Ensure op conversion to HEX is proper.

def assemble_i8080_asm_file(in_asm_file_path):
    labels = {}
    instructions = []

    # First pass: Extract labels and store instruction addresses
    with open(in_asm_file_path, 'r') as f:
        address = 0
        for line in f:
            line = line.strip()
            line = line.split(';')[0].strip()  # Strip inline comments
            if line and not line.startswith(';'):
                if ':' in line:
                    label, _ = line.split(':', 1)
                    labels[label.strip()] = address
                    address += 1
                else:
                    address += 1

    # Second pass: Assemble instructions
    with open(in_asm_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            line = line.split(';')[0].strip()  # Strip inline comments
            if line and not line.startswith(';'):
                if ':' in line:
                    continue  # Skip label definitions in the second pass
                parts = line.split()
                opcode = parts[0]
                if opcode in labels:
                    address = labels[opcode]
                    parts = parts[1:]  # Remove label from instruction parts
                else:
                    address += 1
                instructions.append((address, ' '.join(parts)))

    return labels, instructions


def instructions_to_hex(instructions):
    instructions_to_hex_code = []
    address_map = {}
    address_counter = 0

    # Pass 1: Populate address_map with label addresses
    for address, instruction in instructions:
        parts = instruction.split()
        if len(parts) > 1 and parts[0].endswith(':'):
            label = parts[0][:-1]
            address_map[label] = address_counter
        else:
            address_counter += 1

    # Pass 2: Convert instructions to hexadecimal, replacing labels with addresses
    for address, instruction in instructions:
        parts = instruction.split()
        opcode = parts[0]
        operands = instruction.split()[1:]

        hex_opcode = opcode
        instructions_to_hex_code.append(hex_opcode)

        for op in operands:
            if op in address_map:
                operand_value = address_map[op]
            else:
                try:
                    if op.endswith('B'):
                        operand_value = int(op[:-1], 2)  # Binary
                    elif op.endswith(('O', 'Q')):
                        operand_value = int(op[:-1], 8)  # Octal
                    elif op.endswith('D'):
                        operand_value = int(op[:-1])  # Decimal
                    elif op.endswith('H'):
                        operand_value = int(op[:-1], 16)  # Hexadecimal
                    else:
                        operand_value = int(op)  # Decimal by default
                except ValueError:
                    operand_value = op
                    # raise ValueError(f"Invalid operand value: {op}")

            instructions_to_hex_code.append(operand_value)

    return address_map, instructions_to_hex_code


def write_hex_file(in_hex_file_path, in_hex_code):
    #  TODO: Finish writing hexadecimal code to a file.
    with open(in_hex_file_path, 'w') as f:
        for item in in_hex_code:
            if isinstance(item, int):
                f.write(format(item, '02X'))
            elif isinstance(item, str):
                hex_str = bytes(item, 'utf-8').hex()
                f.write(hex_str)
            else:
                raise TypeError(f"Unsupported type: {type(item)}")


def test_assemble_i8080_asm_file():
    given_path = '../../example_asm/'
    asm_file = '8080_fp16.ASM'
    hex_file = 'new_8080_fp16.HEX'
    asm_file_path = given_path + asm_file
    hex_file_path = given_path + hex_file

    assembled_labels, assembled_instructions = assemble_i8080_asm_file(asm_file_path)
    print('assembled_labels:\n', assembled_labels)
    for address, instruction in assembled_instructions:
        print(address, instruction)
    address_mapping, hex_code = instructions_to_hex(assembled_instructions)
    print('address_mapping:\n', address_mapping)
    write_hex_file(hex_file_path, hex_code)


if __name__ == "__main__":
    test_assemble_i8080_asm_file()
