from sly import Lexer, Parser


class I8080Lexer(Lexer):
    labels = {}
    tokens = {
        LABEL, INSTRUCTION, COMMA,
        HEX, DECIMAL, OCTAL, BINARY,
        QUOTED_CHARACTER, MEMORY_ADDRESS, DECIMAL,
        MATH_EXPRESSION,
    }

    ignore = ' \t'
    ignore_comment = r';.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    QUOTED_CHARACTER = r"'[^']'"

    @_(r'\b\w+:')
    def LABEL(self, t):
        t.value = t.value.strip(':')
        self.labels[t.value] = t.value
        # TODO: create label dictionary for AST traversal after parsing is fixed.
        return t

    INSTRUCTION = r'(?<!\w)(EQU|ORG|MOV|ADD|SUB|INR|DCR|CMA|CMP|ANA|XRA|ORA|ADI|ACI|SUI|SBI|ANI|XRI|ORI|CALL|RET|JMP|JC|JNC|JZ|JNZ|JP|JM|JPE|JPO|HLT|PCHL|SPHL|XCHG|XTHL|DI|EI|NOP|RLC|RRC|RAL|RAR|STC|CMC|HLT|STAX|INX|MVI|PUSH|POP|RNZ|RP|RZ|CM|DAD|RC|CPI|LXI|RNC|CNZ|LHLD|DB|DCX|LDAX|DW)(?!\w)'

    COMMA = r','

    MEMORY_ADDRESS = r'(?![0-9])[A-Za-z_\$][A-Za-z0-9_]*(?!\w)'

    @_(r'([+\-])')
    def MATH_EXPRESSION(self, t):
        # print("\t\t\t VALUE: ", t.value)
        # if t.value.startswith("'"):
        #     print("\t found ':  ", t)
        #     return None
        # else:
        #     print('\t t:  ', t)
        return t

    HEX = r'\-?([0-9a-fA-F]+(H))'
    OCTAL = r'(\-?[0-7]+([OQ]))'
    BINARY = r'\-?([01]+(B))'
    DECIMAL = r'\'?\-?[0-9]+D?\.?[0-9]*D?\'?|[0-9]'

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1


class I8080Parser(Parser):
    tokens = I8080Lexer.tokens
    debugfile = 'i8080_parser.out'

    def __init__(self):
        self.ast = []

    # @_('')
    # def program(self, p):
    #     return []

    @_('program statement')
    def program(self, p):
        p.program.append(p.statement)
        return p.program

    @_('statement')
    def program(self, p):
        return [p.statement]

    @_('LABEL')
    def statement(self, p):
        return [p.LABEL]

    @_('LABEL statement')
    def statement(self, p):
        return [p.LABEL, p.statement]


    @_('INSTRUCTION')
    def statement(self, p):
        return [p.INSTRUCTION]

    @_('INSTRUCTION operand')
    def statement(self, p):
        return [p.INSTRUCTION, p.operand]

    @_('INSTRUCTION operands')
    def statement(self, p):
        return [p.INSTRUCTION, p.operands]

    @_('operand')
    def operands(self, p):
        return p.operand

    @_('operands COMMA operand')
    def operands(self, p):
        return [p.operands, p.COMMA, p.operand]

    @_('MEMORY_ADDRESS COMMA operands')
    def operands(self, p):
        return [p.MEMORY_ADDRESS, p.COMMA, p.operands]

    @_('DECIMAL COMMA operands')
    def operands(self, p):
        return [p.DECIMAL, p.COMMA, p.operands]

    @_('expression COMMA operands')
    def operands(self, p):
        return [p.expression, p.COMMA, p.operands]

    @_('MEMORY_ADDRESS')
    def operand(self, p):
        return p.MEMORY_ADDRESS

    @_('QUOTED_CHARACTER')
    def operand(self, p):
        return p.QUOTED_CHARACTER

    @_('HEX')
    def operand(self, p):
        return p.HEX

    @_('DECIMAL')
    def operand(self, p):
        return p.DECIMAL

    @_('OCTAL')
    def operand(self, p):
        return p.OCTAL

    @_('BINARY')
    def operand(self, p):
        return p.BINARY

    @_('expression')
    def operand(self, p):
        return p.expression

    @_('MATH_EXPRESSION')
    def expression(self, p):
        return p.MATH_EXPRESSION

    @_('operand MATH_EXPRESSION operands')
    def expression(self, p):
        return (p.operand, p.MATH_EXPRESSION, p.operands)

    @_('operand MATH_EXPRESSION operand')
    def expression(self, p):
        return (p.operand0, p.MATH_EXPRESSION, p.operand1)

    @_('MATH_EXPRESSION operand')
    def operand(self, p):
        return (p.MATH_EXPRESSION, p.operand)

    def error(self, p):
        print(f"Syntax error at line: {p.lineno}")
        print(f"\t{p}")
        print()


def test_sly_lexer(code):
    lexer = I8080Lexer()
    print("Lexing-----------------------------------------------------------------------------------------------Lexing")
    for token in lexer.tokenize(code):
        print(token)
    print("End Lexing")


def test_sly_parser(code):
    lexer = I8080Lexer()
    parser = I8080Parser()
    print("Parsing---------------------------------------------------------------------------------------------Parsing")
    ast = parser.parse(lexer.tokenize(code))
    for abs_syn in ast:
        print(abs_syn)
    print(ast)
    print("End Parsing")


input_code = """LXI H, 1+1
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
LXI H, F16_1 - 1

LXI H, 1+'+'+'-'-1
LXI H, 1 + '+' + '-' - 1
LXI H, 1-'-'-'+'+1
LXI H, 1 - '-' - '+' + 1
LXI H, 1 - '-' - '+' +1

LABEL1: MOV A, B ;Inline comment
ADD M, 10H
;Line comment
LXI H,F16_1+1

LABEL2: SUB H, L
MOV C, M
STAX D
MVI A,'-'
CALL CHR
MVI A,'$'
MVI A,$

LABEL3: ADD A, FFFFH
ADD A, 9999D
ADD A, 0000
SUB B, 0000O
SUB B, 7777Q
MOV M, A

LABEL4:     MOV 0FH, 000CH
DB 0,78H,80H,84H,88H,8AH,8CH,8EH,90H,91H,92H
DB 3C00H,   4170H, 4248H,       4900H
DW F16_1, F16_10,  5640H,   63D0H,    70D2H
"""

test_sly_lexer(input_code)
test_sly_parser(input_code)


def test_fp16():
    #  test fp16.ASM
    file_path = "example_asm/8080_fp16.ASM"
    print(f"\nTesting with {file_path} :")
    try:
        with open(file_path, 'r') as asm_file:
            fp16_file = asm_file.read()
            test_sly_lexer(fp16_file)
            test_sly_parser(fp16_file)

    except Exception as e:
        print(e)


test_fp16()
