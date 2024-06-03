# Define the translation rules from 8080 to THUMB
translation_rules = {
    'MOV': 'MOV',
    'ADD': 'ADD',
    'SUB': 'SUB',
    'INR': 'ADD',   # Example: INR can be translated to ADD with an immediate value of 1
    'DCR': 'SUB',   # Example: DCR can be translated to SUB with an immediate value of 1
    'MVI': 'MOV',
    'LXI': 'LDR',   # Load Register (LDR) with an immediate value
    'HLT': 'B .',   # HLT can be translated to an infinite loop in THUMB
    'CALL': 'BL',   # Branch with Link for subroutine calls
    'RET': 'BX LR'  # Return from subroutine
    # Add other translations as needed
}


def translate_instruction(instruction, operands):
    # Translate the instruction and its operands
    thumb_instruction = translation_rules.get(instruction, None)
    if not thumb_instruction:
        return f"; Unsupported instruction {instruction}"

    # Handling different instructions
    if instruction == 'INR':
        return f"{thumb_instruction} {operands[0]}, {operands[0]}, #1"
    elif instruction == 'DCR':
        return f"{thumb_instruction} {operands[0]}, {operands[0]}, #1"
    elif instruction == 'MOV':
        return f"{thumb_instruction} {operands[0]}, {operands[1]}"
    elif instruction == 'MVI':
        return f"{thumb_instruction} {operands[0]}, #{operands[1]}"
    elif instruction == 'LXI':
        return f"{thumb_instruction} {operands[0]}, ={operands[1]}"
    elif instruction == 'HLT':
        return f"{thumb_instruction}"
    elif instruction == 'CALL':
        return f"{thumb_instruction} {operands[0]}"
    elif instruction == 'RET':
        return f"{thumb_instruction}"

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
    # test_translator()
    # TODO Create Testing System
