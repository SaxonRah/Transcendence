import sys
import ply.lex as lex
import ply.yacc as yacc
from pprint import pprint

recursion_limit = 9999
sys.setrecursionlimit(recursion_limit)


class I8080Lexer:

    labels = {}
    macros = {}
    directives = {}

    tokens = (
        'LABEL', 'DIRECTIVE', 'MACRO', 'INSTRUCTION', 'COMMA',
        'HEX', 'DECIMAL', 'OCTAL', 'BINARY', 'REGISTER',
        'QUOTED_CHARACTER', 'MEMORY_ADDRESS',
        'MATH_EXPRESSION',
    )

    t_ignore = ' \t'
    t_ignore_COMMENT = r';.*'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    literals = ['<', '>', '$']

    def t_dollar(self, t):
        r'\$'
        t.type = 'REGISTER'
        return t

    def t_QUOTED_CHARACTER(self, t):
        r"'[^']'"
        return t

    # TODO: implement the comment chain below for macro, directives, and instructions.
    # reserved = {
    #     'if': 'IF',
    #     'then': 'THEN',
    #     'else': 'ELSE',
    #     'while': 'WHILE',
    #     ...
    # }
    #
    # tokens = ['LPAREN', 'RPAREN', ..., 'ID'] + list(reserved.values())
    #
    # def t_LABEL(t):
    #     r'\b\w+:'
    #     t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    #     return t

    def t_LABEL(self, t):
        r'\b\w+:'
        # t.value = t.value.strip(':')
        self.labels[t.lexer.lineno] = t.value
        # print('Labels: \t\n', self.labels)
        return t

    def t_MACRO(self, t):
        r'(?<!\w)(MACRO|ENDM|LOCAL|REPT|IRP|IRPC|EXITM)(?!\w)'
        self.macros[t.lexer.lineno] = t.value
        # print('Macros: \t\n', self.macros)
        return t

    def t_DIRECTIVE(self, t):
        r'(?<!\w)(EQU|SET|DB|DW|DS|IF|ELSE|ENDIF|END|ASEG|DSEG|CSEG|ORG|PUBLIC|EXTRN|NAME|STKLN|STACK|MEMORY)(?!\w)'
        self.directives[t.lexer.lineno] = t.value
        # print('Directives: \t\n', self.directives)
        return t

    def t_INSTRUCTION(self, t):
        r'(?<!\w)(MOV|ADD|SUB|INR|DCR|CMA|CMP|ANA|XRA|ORA|ADI|ACI|SUI|SBI|ANI|XRI|ORI|CALL|RET|JMP|JC|JNC|JZ|JNZ|JP|JM|JPE|JPO|HLT|PCHL|SPHL|XCHG|XTHL|DI|EI|NOP|RLC|RRC|RAL|RAR|STC|CMC|HLT|STAX|INX|MVI|PUSH|POP|RNZ|RP|RZ|CM|DAD|RC|CPI|LXI|RNC|CNZ|LHLD|DCX|LDAX)(?!\w)'
        return t

    def t_MATH_EXPRESSION(self, t):
        # r'([+\-])'
        r'[+\-]'
        return t

    def t_REGISTER(self, t):
        r'(?<!\w)(A|B|C|D|E|H|L|M|SP|PSW|BC|DE|HL)(?!\w)\b'
        return t

    def t_HEX(self, t):
        r'\-?([0-9a-fA-F]+[H])\b'
        # t.value = t.value.replace('H', '')
        return t

    def t_OCTAL(self, t):
        r'(\-?[0-7]+[OQ])\b'
        # t.value = t.value.replace('O', '')
        # t.value = t.value.replace('Q', '')
        return t

    def t_BINARY(self, t):
        r'\-?([01]+[B])\b'
        # t.value = t.value.replace('B', '')
        return t

    def t_DECIMAL(self, t):
        r'\'?\-?[0-9]+D?\.?[0-9]*[D]?\'?|[0-9]\b'
        # t.value = t.value.replace('D', '')
        return t

    def t_COMMA(self, t):
        # r'[,]'
        r','
        return t

    def t_MEMORY_ADDRESS(self, t):
        r'(?![0-9])[A-Za-z_\$][A-Za-z0-9_]*(?!\w)'
        return t

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


class I8080Parser:
    tokens = I8080Lexer.tokens

    def __init__(self):
        self.ast = []

    def p_program_empty(self, p):
        'program :'
        p[0] = []

    def p_program_statements(self, p):
        '''program : program statement'''
        p[1].append(p[2])
        p[0] = p[1]
        # p[0] = (p[1], p[2])

    def p_program_statement(self, p):
        '''program : statement'''
        p[0] = [p[1]]

    # TODO: Create list of instructions until the next label is encountered like:
    #  [['LABEL1', 'XCHG', ('CALL', 'F16NEG')],
    #  ['LABEL2', 'XCHG', ('CALL', 'F16NEG')]]
    #  instead of :
    #  [('LABEL1', 'XCHG'),
    #  ('CALL', 'F16NEG'),
    #  ('LABEL2', 'XCHG'),
    #  ('CALL', 'F16NEG')]


    def p_statement_label(self, p):
        'statement : LABEL'
        p[0] = ('LABEL', p[1])

    def p_statement_label_statement(self, p):
        'statement : LABEL statement'
        p[0] = ('LABEL', p[1], p[2])

    def p_statement_macro(self, p):
        'statement : MACRO'
        p[0] = ('MACRO', p[1])

    def p_statement_macro_operands(self, p):
        'statement : MACRO operands'
        p[0] = ('MACRO', p[1], p[2])

    def p_statement_macro_operands_macro(self, p):
        'statement : MACRO operands MACRO'
        p[0] = ('MACRO', p[1], p[2], p[3])

    def p_statement_directive_operands(self, p):
        'statement : DIRECTIVE operands'
        p[0] = ('DIRECTIVE', p[1], p[2])

    def p_statement_instruction(self, p):
        'statement : INSTRUCTION'
        p[0] = ('INSTRUCTION', p[1])

    def p_statement_instruction_operands(self, p):
        'statement : INSTRUCTION operands'
        p[0] = ('INSTRUCTION', p[1], p[2])

    def p_operands_comma_operand(self, p):
        'operands : operands COMMA operand'
        #  p[0] = p[1], p[2], p[3]
        #  p[0] = p[1], p[3]
        # DONE: Create list/tuple of operands like:
        #  ('16', '-', 'F16MB', '+', '1')
        #  instead of:
        #  ('16', '-', ('F16MB', '+', '1'))
        #  SEEMS TO WORK FOR NOW
        # ('INSTRUCTION', 'MVI', ('C', ('16', '-', 'F16MB', '+', '1')))
        if isinstance(p[1], tuple):
            p[0] = p[1] + (p[3],)
        else:
            p[0] = (p[1], p[3])


    def p_operands_operand(self, p):
        'operands : operand'
        p[0] = p[1]

    def p_operand_quoted_character(self, p):
        'operand : QUOTED_CHARACTER'
        p[0] = p[1]

    def p_operand_register(self, p):
        'operand : REGISTER'
        p[0] = p[1]

    def p_operand_hex(self, p):
        'operand : HEX'
        p[0] = p[1]

    def p_operand_decimal(self, p):
        'operand : DECIMAL'
        p[0] = p[1]

    def p_operand_octal(self, p):
        'operand : OCTAL'
        p[0] = p[1]

    def p_operand_binary(self, p):
        'operand : BINARY'
        p[0] = p[1]

    def p_operand_memory_address(self, p):
        'operand : MEMORY_ADDRESS'
        p[0] = p[1]

    def p_operand_expression(self, p):
        'operand : expression'
        p[0] = p[1]

    # TODO: Fixup math expression parsing rules
    def p_expression_math_expression(self, p):
        'expression : MATH_EXPRESSION'
        p[0] = p[1]

    def p_expression_operand_math_expression_operands(self, p):
        'expression : operand MATH_EXPRESSION operands'
        # DONE: Create list/tuple of operands like:
        #  ('LXI', ('H', ('1', '+', "'+'", '+', "'-'", '-', '1')))
        #  instead of:
        #  ('LXI', ('H', ('1', '+', ("'+'", '+', ("'-'", '-', '1')))))
        #       It now properly adds all mathematical expressions into a single tuple.
        #       ('INSTRUCTION', 'LXI', ('H', ('1', '+', "'+'", '+', "'-'", '-', '1')))
        #       ('INSTRUCTION', 'LXI', ('H', ('1', '+', "'+'", '+', "'-'", '-', '1')))
        #       ('INSTRUCTION', 'LXI', ('H', ('1', '-', "'-'", '-', "'+'", '+', '1')))
        #       ('INSTRUCTION', 'LXI', ('H', ('1', '-', "'-'", '-', "'+'", '+', '1')))
        #       ('INSTRUCTION', 'LXI', ('H', ('1', '-', "'-'", '-', "'+'", '+', '1')))
        p[0] = (p[1], p[2]) + (p[3] if isinstance(p[3], tuple) else (p[3],))

    def p_operand_math_expression_operand(self, p):
        'operand : MATH_EXPRESSION operand'
        p[0] = (p[1], p[2])

    def p_error(self, p):
        if p:
            print(f"Syntax error at line: {p.lineno}")
            print(f"\t{p}")
        else:
            print("Syntax error at EOF")

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data):
        return self.parser.parse(data)


def test_ply_lexer(code):
    lexer = I8080Lexer()
    lexer.build()
    print("Lexing-----------------------------------------------------------------------------------------------Lexing")
    lexer.test(code)
    print("End Lexing")


def test_ply_parser(code):
    lexer = I8080Lexer()
    lexer.build()
    parser = I8080Parser()
    parser.build()
    print("Parsing---------------------------------------------------------------------------------------------Parsing")
    ply_ast = parser.parse(code)
    for abs_syn in ply_ast:
        print(abs_syn)
    print(ply_ast)
    # print(ply_ast)
    print("End Parsing")


input_code = """F16_1:EQU 3C00H
LXIHEXP:
LXI H, 1+1
LXI H, 1-1
LXI H, 1 + 1
LXI H, 1 - 1
LXI H, 1+'+'
LXI H, 1-'-'
LXI H, 1+ '+'
LXI H, 1 - '-'

LXI H, F16_1+1
LXI H, F16_1-1
LXI H, F16_1 + 1
LXI H, F16_1 + -1
LXI H, F16_1 + - 1
LXI H, F16_1 - 1
LXI H, F16_1 - -1
LXI H, F16_1 - - 1

LXI H, 1+'+'+'-'-1
LXI H, 1 + '+' + '-' - 1
LXI H, 1-'-'-'+'+1
LXI H, 1 - '-' - '+' + 1
LXI H, 1 - '-' - '+' +1

LABEL1: MOV A, B ;Inline comment
ADD M, 10H
;Line comment
LXI H,F16_1+1
CALL LABEL2
CALL LABEL3
CALL LABEL4
CALL LABEL5

LABEL5:
ADD A, -1
CALL LABEL1
CALL LABEL2
CALL LABEL3
CALL LABEL4

LABEL2: SUB H, L
MOV C, M
STAX D
MVI A,'-'
CALL CHR
MVI A,'$'
MVI A,$
CALL LABEL1
CALL LABEL3
CALL LABEL4
CALL LABEL5

LABEL3: ADD A, FFFFH
ADD A, 9999D
ADD A, 0000
SUB B, 0000O
SUB B, 7777Q
MOV M, A
CALL LABEL1
CALL LABEL2
CALL LABEL4
CALL LABEL5

LABEL4:     MOV 0FH, 000CH
DB 0,78H,80H,84H,88H,8AH,8CH,8EH,90H,91H,92H
DB 3C00H,   4170H, 4248H,       4900H
DW F16_1, F16_10,  5640H,   63D0H,    70D2H
CALL LABEL1
CALL LABEL2
CALL LABEL3
CALL LABEL5
"""


def test_fp16():
    file_path = "example_asm/8080_fp16.ASM"
    print(f"\nTesting with {file_path} :")
    try:
        with open(file_path, 'r') as asm_file:
            fp16_file = asm_file.read()
            test_ply_lexer(fp16_file)
            test_ply_parser(fp16_file)

    except Exception as e:
        print(e)


def test_i8080_lexer_parser():
    test_ply_lexer(input_code)
    test_ply_parser(input_code)
    test_fp16()



from PostProcessing_AST_Traversal_Translator import *


def test_postprocessing_ast_traversal_translator():
    file_path = "example_asm/8080_fp16.ASM"
    print(f"\nTesting with {file_path} :")
    fp16_file = None
    try:
        with open(file_path, 'r') as asm_file:
            fp16_file = asm_file.read()
    except Exception as e:
        print(e)
    if fp16_file is not None:

        lexer = I8080Lexer()
        lexer.build()
        parser = I8080Parser()
        parser.build()
        print("Translation---------------------------------------------------------------------------------Translation")
        generated_ast = parser.parse(fp16_file)
        thumb_code = translate_ast_to_thumb(generated_ast)
        write_thumb_code_to_file(thumb_code)
        print("Translation complete. Check the THUMB_TRANSLATED.S file.")
    else:
        print("Translation received 'None'.")


if __name__ == "__main__":
    # test_i8080_lexer_parser()
    test_postprocessing_ast_traversal_translator()
