# Define the combined mapping provided
from maps.I8080_M0Plus_Mappings import combined_mapping


def translate_instruction(instruction, operands):
    # Translate the instruction and its operands
    thumb_instruction = combined_mapping.get(instruction, None)
    if not thumb_instruction:
        return f"; Unsupported instruction {instruction}"

    # Handling specific cases with operands
    if instruction in ['INR', 'DCR', 'ADD', 'SUB', 'CMP', 'AND', 'EOR', 'ORR', 'MVN', 'ROR']:
        return f"{thumb_instruction} {operands[0]}, {operands[0]}, #1"
    elif instruction == 'MVI':
        return f"{thumb_instruction} {operands[0]}, #{operands[1]}"
    elif instruction == 'LXI':
        return f"{thumb_instruction} {operands[0]}, ={operands[1]}"
    elif instruction == 'LDA':
        return f"{thumb_instruction.replace('[ADR]', f'[{operands[0]}]')}"
    elif instruction == 'STA':
        return f"{thumb_instruction.replace('[ADR]', f'[{operands[0]}]')}"
    elif instruction in ['PUSH', 'POP']:
        return f"{thumb_instruction} {{{operands[0]}}}"
    elif instruction in ['JMP', 'JC', 'JNC', 'JM', 'JZ', 'JNZ', 'JP', 'CALL', 'CC', 'CNC', 'CP', 'CM', 'CZ', 'CNZ']:
        return f"{thumb_instruction} {operands[0]}"

    # Default translation for simple mapping
    if len(operands) == 1:
        return f"{thumb_instruction} {operands[0]}"
    elif len(operands) == 2:
        return f"{thumb_instruction} {operands[0]}, {operands[1]}"
    elif len(operands) == 3:
        return f"{thumb_instruction} {operands[0]}, {operands[1]}, {operands[2]}"
    else:
        return f"; Error translating instruction {instruction}"


def translate_ast_to_thumb(ast):
    thumb_code = []

    for node in ast:
        if node[0] == 'LABEL':
            thumb_code.append(f"{node[1]}")
        elif node[0] == 'INSTRUCTION':
            thumb_code.append(translate_instruction(node[1], node[2] if len(node) > 2 else []))
        elif node[0] == 'MACRO':
            thumb_code.append(f"; Macro {node[1]}")
        elif node[0] == 'DIRECTIVE':
            thumb_code.append(f"; Directive {node[1]} {', '.join(node[2]) if len(node) > 2 else ''}")
        else:
            thumb_code.append(f"; Unsupported node type {node[0]}")

    return "\n".join(thumb_code)


def write_thumb_code_to_file(thumb_code, filename="THUMB_TRANSLATED.S"):
    with open(filename, "w") as f:
        f.write(thumb_code)


# Sample AST for testing
sample_ast = [
    ('LABEL', 'LABEL1:'),
    ('INSTRUCTION', 'MOV', ('A', 'B')),
    ('INSTRUCTION', 'ADD', ('A', '10H')),
    ('INSTRUCTION', 'INR', ('A',)),
    ('INSTRUCTION', 'DCR', ('A',)),
    ('INSTRUCTION', 'MVI', ('A', '1')),
    ('INSTRUCTION', 'LXI', ('H', '1000H')),
    ('INSTRUCTION', 'HLT', ()),
    ('INSTRUCTION', 'CALL', ('SUBROUTINE1',)),
    ('INSTRUCTION', 'RET', ()),
]


# Test the translation
def test_translator():
    thumb_code = translate_ast_to_thumb(sample_ast)
    write_thumb_code_to_file(thumb_code)
    print("Translation complete. Check the THUMB_TRANSLATED.S file.")


if __name__ == "__main__":
    ...
    test_translator()
    # TODO Create Testing System
