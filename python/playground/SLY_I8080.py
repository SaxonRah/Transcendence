from sly import Lexer, Parser

# TODO: create identical PLY version for shits and giggles.
#  Also because SLY is technically not supported anymore but PLY is.
#  I prefer SLY but PLY might be worth the support.
#  This is done, and I will no longer work on this SLY implementation.
#  All future lexing and parsing updates will be in the PLY version.


class I8080Lexer(Lexer):
    labels = {}
    macros = {}
    directives = {}
    tokens = {
        LABEL, DIRECTIVE, MACRO, INSTRUCTION, COMMA,
        HEX, DECIMAL, OCTAL, BINARY, REGISTER,
        QUOTED_CHARACTER, MEMORY_ADDRESS,
        MATH_EXPRESSION,
    }

    ignore = ' \t'
    # TODO: add comments into the lexer and parser for AST traversal translation.
    ignore_comment = r';.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    literals = {'<', '>'}

    QUOTED_CHARACTER = r"'[^']'"

    REGISTER = r'(?<!\w)(A|B|C|D|E|H|L|M|SP|PSW|BC|DE|HL)(?!\w)\b'

    @_(r'\b\w+:')
    def LABEL(self, t):
        t.value = t.value.strip(':')
        self.labels[t.value] = t.value
        # TODO: create label dictionary for AST traversal translation
        return t

    @_(r'(?<!\w)(MACRO|ENDM|LOCAL|REPT|IRP|IRPC|EXITM)(?!\w)')
    def MACRO(self, t):
        self.macros[t.value] = t.value
        # TODO: create macro dictionary for AST traversal translation
        return t

    @_(r'(?<!\w)(EQU|SET|DB|DW|DS|IF|ELSE|ENDIF|END|ASEG|DSEG|CSEG|ORG|PUBLIC|EXTRN|NAME|STKLN|STACK|MEMORY)(?!\w)')
    def DIRECTIVE(self, t):
        self.directives[t.value] = t.value
        # TODO: create directives dictionary for AST traversal translation
        return t

    @_(r'(?<!\w)(MOV|ADD|SUB|INR|DCR|CMA|CMP|ANA|XRA|ORA|ADI|ACI|SUI|SBI|ANI|XRI|ORI|CALL|RET|JMP|JC|JNC|JZ|JNZ|JP|JM|JPE|JPO|HLT|PCHL|SPHL|XCHG|XTHL|DI|EI|NOP|RLC|RRC|RAL|RAR|STC|CMC|HLT|STAX|INX|MVI|PUSH|POP|RNZ|RP|RZ|CM|DAD|RC|CPI|LXI|RNC|CNZ|LHLD|DCX|LDAX)(?!\w)')
    def INSTRUCTION(self, t):
        return t

    COMMA = r'[,]'

    MEMORY_ADDRESS = r'[A-Za-z_\$][A-Za-z0-9_]*(?!\w)'
    # MEMORY_ADDRESS = r'(?![0-9])[A-Za-z_\$][A-Za-z0-9_]*(?!\w)'

    @_(r'([+\-])')
    def MATH_EXPRESSION(self, t):
        return t

    HEX = r'\-?([0-9a-fA-F]+(H))\b'
    OCTAL = r'(\-?[0-7]+([OQ]))\b'
    BINARY = r'\-?([01]+(B))\b'
    DECIMAL = r'\'?\-?[0-9]+D?\.?[0-9]*D?\'?|[0-9]\b'

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1


class I8080Parser(Parser):
    tokens = I8080Lexer.tokens
    debugfile = 'SLY_i8080_parser.out'

    def __init__(self):
        self.ast = []

    # TODO: clean up the 14 shift/reduce conflicts

    @_('')
    def program(self, p):
        return []

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

    @_('MACRO')
    def statement(self, p):
        return [p.MACRO]

    @_('MACRO operands')
    def statement(self, p):
        return [p.MACRO, p.operands]

    @_('MACRO operands MACRO')
    def statement(self, p):
        return [p.MACRO0, p.operands, p.MACRO1]

    @_('DIRECTIVE operands')
    def statement(self, p):
        return [p.DIRECTIVE, p.operands]

    @_('INSTRUCTION')
    def statement(self, p):
        return [p.INSTRUCTION]

    @_('INSTRUCTION operands')
    def statement(self, p):
        return [p.INSTRUCTION, p.operands]

    # @_('operands COMMA operands')
    # def operands(self, p):
    #     return [p.operands0, p.COMMA].append(p.operands1)

    @_('operands COMMA operand')
    def operands(self, p):
        return (p.operands, p.COMMA, p.operand)

    @_('operand')
    def operands(self, p):
        return p.operand

    # @_('MEMORY_ADDRESS COMMA operands')
    # def operands(self, p):
    #     return [p.MEMORY_ADDRESS, p.COMMA, p.operands]

    # @_('DECIMAL COMMA operands')
    # def operands(self, p):
    #     return (p.DECIMAL, p.COMMA, p.operands)

    # @_('expression COMMA operands')
    # def operands(self, p):
    #     return (p.expression, p.COMMA, p.operands)

    @_('MEMORY_ADDRESS')
    def operand(self, p):
        return p.MEMORY_ADDRESS

    @_('QUOTED_CHARACTER')
    def operand(self, p):
        return p.QUOTED_CHARACTER

    @_('REGISTER')
    def operand(self, p):
        return p.REGISTER

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

    # @_('operands MATH_EXPRESSION operands')
    # def expression(self, p):
    #     return (p.operands0, p.MATH_EXPRESSION, p.operands1)

    @_('operand MATH_EXPRESSION operands')
    def expression(self, p):
        return (p.operand, p.MATH_EXPRESSION, p.operands)

    # @_('operand MATH_EXPRESSION operand')
    # def expression(self, p):
    #     return (p.operand0, p.MATH_EXPRESSION, p.operand1)

    @_('MATH_EXPRESSION operand')
    def operand(self, p):
        return (p.MATH_EXPRESSION, p.operand)

    def error(self, p):
        print(f"Syntax error at line: {p.lineno}")
        print(f"\t{p}")
        print()

# TODO: create lexer / parser functions that return
#  tokens, and separate labels, macros, directives dictionaries to build a real AST and not the SLY list.


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
    sly_ast = parser.parse(lexer.tokenize(code))
    #  return sly_ast
    for abs_syn in sly_ast:
        print(abs_syn)
    print(sly_ast)
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


def test_i8080_lexer_parser():
    test_sly_lexer(input_code)
    test_sly_parser(input_code)
    test_fp16()


if __name__ == "__main__":
    test_i8080_lexer_parser()
