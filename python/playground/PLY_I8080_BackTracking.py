import ply.lex as lex
import ply.yacc as yacc

# TODO: 26 shift/reduce conflicts


class I8080Lexer:

    def __init__(self):
        self.current_label = None
        self.labels = {}
        self.macros = {}
        self.directives = {}

    tokens = (
        'LABEL', 'DIRECTIVE', 'MACRO', 'INSTRUCTION', 'COMMA',
        'HEX', 'DECIMAL', 'OCTAL', 'BINARY', 'REGISTER',
        'QUOTED_CHARACTER', 'MEMORY_ADDRESS',
        'PLUS', 'MINUS'
    )

    t_ignore = ' \t'
    t_ignore_COMMENT = r';.*'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    literals = ['<', '>', '$', '+', '-']

    def t_dollar(self, t):
        r'\$'
        t.type = 'REGISTER'
        return t

    def t_PLUS(self, t):
        r'\+'
        t.type = 'PLUS'
        return t

    def t_MINUS(self, t):
        r'\-'
        t.type = 'MINUS'
        return t

    def t_QUOTED_CHARACTER(self, t):
        r"'[^']'"
        return t

    # TODO: implement the reserved chain below
    #  for labels, macro, directives, and instructions.
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
        t.value = t.value.strip(':')
        self.current_label = t.value
        if self.current_label not in self.labels:
            self.labels[self.current_label] = [t.lexer.lineno]
        elif t.lexer.lineno in self.labels[self.current_label]:
            print(rf'LEX ERROR: Possible malformed code with {self.current_label}, at {t.lexer.lineno}')
        else:
            self.labels[self.current_label].append(t.lexer.lineno)
        print('Labels: \t\n', self.labels)
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
        r'[,]'
        return t

    # TODO: check for F16TST label, seems to be eaten
    # MEMORY_ADDRESS will never show up in the lex tokens.
    # This is used to convert a usage of pre-defined labels into labels
    def t_MEMORY_ADDRESS(self, t):
        r'\b[A-Za-z_][A-Za-z0-9_]*(?!\w)'
        t.type = 'LABEL'
        self.current_label = t.value
        if self.current_label in self.labels.keys():
            self.labels[self.current_label].append(t.lexer.lineno)
        else:
            self.labels[self.current_label] = [t.lexer.lineno]
        return t

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.current_label = None
        self.labels = {}
        self.macros = {}
        self.directives = {}
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


# TODO: Create list of instructions until the next label is encountered like:
#  [['LABEL1', 'XCHG', ('CALL', 'F16NEG')],
#  ['LABEL2', 'XCHG', ('CALL', 'F16NEG')]]
#  instead of :
#  [('LABEL1', 'XCHG'),
#  ('CALL', 'F16NEG'),
#  ('LABEL2', 'XCHG'),
#  ('CALL', 'F16NEG')]
#  SEEMS TO WORK FOR NOW SEE PROBLEM COMMENT BELOW
#  V----------------------------------------------V
"""
Problem: 
    If a label is encountered, it's output encapsulates the first instruction by it's label:
['BUFFER', ('DB', '0'), 'BUFFER']
['F16SUB', 'XCHG', 'F16SUB', ['CALL', 'F16NEG']]
As you can see the BUFFER and F16SUB label is added after it's first instruction.

Fix the first instruction label encapsulation.
It's a ton better than before, however this will need a rethink on how to handle this.

self.ast = [] in parser is used here, and the file is now being parsed into it by parser rules.
The handling of this is quite bad and complicated, but it works for now.

There might be many new major problems with the parser now but I couldn't find any at the moment.
"""


class I8080Parser:
    tokens = I8080Lexer.tokens

    def __init__(self):
        self.ast = []
        self.current_label = None

    def p_program_empty(self, p):
        'program :'
        p[0] = []

    def p_program_statements(self, p):
        '''program : program statement'''
        # TODO: Find a way to not use self.ast
        #          OR commit to using self.ast
        if self.current_label:
            self.ast[-1].append(p[2])
        else:
            self.ast.append(p[2])
        p[0] = self.ast

    def p_program_statement(self, p):
        '''program : statement'''
        # TODO: Find a way to not use self.ast
        #          OR commit to using self.ast
        # if self.current_label:
        self.ast[-1].append(p[1])
        # else:
        #     self.ast.append(p[1])
        p[0] = self.ast

    def p_statement_label(self, p):
        'statement : LABEL'
        # TODO: Find a way to not use self.ast
        #          OR commit to using self.ast
        self.current_label = p[1]
        self.ast.append([p[1]])
        p[0] = p[1]
        # p[0] = self.ast

    def p_statement_label_statement(self, p):
        'statement : LABEL statement'
        # TODO: Find a way to not use self.ast
        #          OR commit to using self.ast
        # TODO: Find a way to remove label encapsulation of first instruction. Like:
        #  ['STR_E', ('DB', ("'2.718'", '0')), 'STR_E']
        #  ['STR_42_5', ('DB', ("'42.5'", '0')), 'STR_42_5']
        #  PLY returns None if no p[0] is assigned.
        if self.current_label == p[1]:
            p[0] = p[2]
        else:
            self.current_label = p[1]
            self.ast.append([p[1], p[2]])
            p[0] = p[1]
            # p[0] = self.ast

    def p_statement_single(self, p):
        '''statement : INSTRUCTION
                     | DIRECTIVE
                     | MACRO'''
        p[0] = p[1]

    def p_statement_singe_operands(self, p):
        '''statement : INSTRUCTION operands
                     | DIRECTIVE operands
                     | MACRO operands'''
        p[0] = [p[1], p[2]]

    def p_statement_macro_ops_macro(self, p):
        '''statement : MACRO operands MACRO'''
        if len(p) == 4:
            p[0] = [p[1], p[2], p[3]]
        elif len(p) == 3:
            p[0] = [p[1], p[2]]

    # TODO: Create list/tuple of operands like:
    #  ['LXI', ['H', ',', ['1', '-', "'-'", '-', "'+'", '+', '1']]]
    #  instead of:
    #  ['LXI', ['H', ',', ['1', '-', ["'-'", '-', ["'+'", '+', '1']]]]]
    def p_operands_comma_operand(self, p):
        'operands : operands COMMA operand'
        p[0] = [p[1], p[2], p[3]]

    def p_operands_comma_negoperand(self, p):
        'operands : operands COMMA MINUS operand'
        p[0] = [p[1], p[2], p[3], p[4]]

    def p_expression_math(self, p):
        '''expression : operand PLUS operand
                      | operand MINUS operand'''
        p[0] = [p[1], p[2], p[3]]

    # TODO: Deal with negative numbers better.
    def p_expression_math_negnumb(self, p):
        '''expression : operand PLUS MINUS operand
                      | operand MINUS MINUS operand'''
        p[0] = [p[1], p[2], p[3], p[4]]

    def p_expression_recursive(self, p):
        '''expression : expression PLUS operand
                      | expression MINUS operand'''

        p[0] = [p[1], p[2], p[3]]

    def p_operands_operand(self, p):
        'operands : operand'
        p[0] = p[1]

    def p_operand(self, p):
        '''operand : QUOTED_CHARACTER
                    | REGISTER
                    | HEX
                    | DECIMAL
                    | OCTAL
                    | BINARY
                    | LABEL
                    | expression
                    | MEMORY_ADDRESS'''
        p[0] = p[1]

    # TODO: Create list/tuple of operands like:
    #  ('16', '-', 'F16MB', '+', '1')
    #  instead of:
    #  ('16', '-', ('F16MB', '+', '1'))
    # TODO: Find a way to concatenate expressions without self.ast
    #       OR commit to using self.ast
    #  It would be possible to index the last expression encountered like labels and merge them.
    #       However this is extremely bad, ugly and prone to errors.

    def p_error(self, p):
        if p:
            print(f"Syntax error at line: {p.lineno}")
            print(f"\t{p}")
        else:
            print("Syntax error at EOF")

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data):
        self.ast = []
        self.current_label = None
        return self.parser.parse(data)


def test_ply_lexer(code):
    lexer = I8080Lexer()
    lexer.build()
    print("Lexing-----------------------------------------------------------------------------------------------Lexing")
    lexer.test(code)
    print("End Lexing---------------------------------------------------------------------------------------End Lexing")


def test_ply_parser(code):
    lexer = I8080Lexer()
    lexer.build()
    parser = I8080Parser()
    parser.build()
    abstract_syntax_tree = parser.parse(code)
    print("Parsing---------------------------------------------------------------------------------------------Parsing")
    print('Abstract Syntax Tree:\n', abstract_syntax_tree)
    for branch in abstract_syntax_tree:
        print(branch)
    print("End Parsing-------------------------------------------------------------------------------------End Parsing")


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


if __name__ == "__main__":
    test_i8080_lexer_parser()
