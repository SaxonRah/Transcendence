from sly import Lexer, Parser


class I8080Lexer(Lexer):

    tokens = {
        LABEL, INSTRUCTION,
        COMMA, SPECIAL_CHARACTER,
        IMMEDIATE_DATA, MEMORY_ADDRESS, DECIMAL,
        SINGLE_QUOTED_CHAR, MATH_EXPRESSION,
    }

    ignore = ' \t\''
    ignore_comment = r';.*'

    #  LABEL = r'\w+:'
    #  LABEL = r'\b\w+:'

    @_(r'\b\w+:')
    def LABEL(self, t):
        t.value = t.value.strip(':')
        return t


    INSTRUCTION = r'(EQU|ORG|MOV|ADD|SUB|INR|DCR|CMA|CMP|ANA|XRA|ORA|ADI|ACI|SUI|SBI|ANI|XRI|ORI|CALL|RET|JMP|JC|JNC|JZ|JNZ|JP|JM|JPE|JPO|HLT|PCHL|SPHL|XCHG|XTHL|DI|EI|NOP|RLC|RRC|RAL|RAR|STC|CMC|HLT|STAX|INX|MVI|PUSH|POP|RNZ|RP|RZ|CM|DAD|RC|CPI|LXI|RNC|CNZ|LHLD|DB|DCX|LDAX|DW)'

    COMMA = r','

    MATH_EXPRESSION = r'[+\-]'
    #  MATH_EXPRESSION = r'[A-Za-z0-9_]+(?:[+\-][A-Za-z0-9_]+)*'

    SINGLE_QUOTED_CHAR = r'\'([^\']*)\''


    IMMEDIATE_DATA = r'(-)?\b(?:0x[0-9A-Fa-f]+|\d+(?:\.\d+)?(?:[Hh])?)\b'
    #  IMMEDIATE_DATA = r'(-)?\b(?:0x[0-9A-Fa-f]+|\d+(?:\.\d+)?(?:[Hh])?)\b(?![\+\-\*\/\.\'])'
    #  IMMEDIATE_DATA = r'(-)?\b(?:0x[0-9A-Fa-f]+|\d+(?:\.\d+)?(?:[Hh])?)(?![\+\-\*\/\.])'
    #  IMMEDIATE_DATA = r'(-)?\b(?:0x[0-9A-Fa-f]+|\d+(?:\.\d+)?(?:[Hh])?)\b(?![\+\-\*\/\.])'
    #  IMMEDIATE_DATA = r'(-)?\b(?:0x[0-9A-Fa-f]+|\d+(?:\.\d+)?(?:[Hh])?)\b(?![\+\-\*\/])'
    #  IMMEDIATE_DATA = r'(-)?\b(?:0x[0-9A-Fa-f]+|\d+(?:\.\d+)?(?:[Hh])?)(?!\w)'
    #  IMMEDIATE_DATA = r'-?\b(?:0x[0-9A-Fa-f]+|\d+(?:\.\d+)?(?:[Hh])?)\b'
    #  IMMEDIATE_DATA = r'(-)?\b(?:0x[0-9A-Fa-f]+|[0-9]+(?:\.[0-9]+)?)(?:[Hh]|\b)'
    #  IMMEDIATE_DATA = r'(-)?\b(?:0x[0-9A-Fa-f]+|[0-9]+(?:\.[0-9]+)?)(?:[Hh])?\b'
    #  IMMEDIATE_DATA = r'(-)?([0-9]+)(.)?(?:0)?([Xx])?([0-9A-Fa-f]+)?([Hh])?'
    #  IMMEDIATE_DATA = r'(?:0[Xx])?[0-9A-Fa-f]+[Hh]'

    #  MEMORY_ADDRESS = r'\b(?![0-9])[A-Za-z_][A-Za-z0-9_]*(?!\w|[\+\-\*\/])\b'
    MEMORY_ADDRESS = r'\b(?![0-9])[A-Za-z_][A-Za-z0-9_]*(?!\w|[\+\-\*\/])'

    SPECIAL_CHARACTER = r'[\!\@\#\$\%\^\&\*\(\)\=\`\~\{\}\[\]\:\;\"\,\/\<\>\?\\\|]'
    #  SPECIAL_CHARACTER = r'\'[\!\@\#\$\%\^\&\*\(\)\_\=\.\`\~\{\}\[\]\:\;\"\,\/\<\>\?\\\|]\''

    DECIMAL = r'(-)?(?:\d+\.\d+)'

    '''
    multiple regexes and data conversion
    @_(r'0x[0-9a-fA-F]+',
       r'\d+')
    def NUMBER(self, t):
        if t.value.startswith('0x'):
            t.value = int(t.value[2:], 16)
        else:
            t.value = int(t.value)
        return t
    '''

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1


class I8080Parser(Parser):
    tokens = I8080Lexer.tokens

    def __init__(self):
        self.ast = []

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

    @_('LABEL statement')
    def statement(self, p):
        return [p.LABEL] + p.statement

    @_('INSTRUCTION')
    def statement(self, p):
        return [p[0]]

    @_('INSTRUCTION operands')
    def statement(self, p):
        return [p.INSTRUCTION] + p.operands

    @_('operand')
    def operands(self, p):
        return [p[0]]

    @_('operands COMMA operand')
    def operands(self, p):
        return [p.operands, p.COMMA, p.operand]

    # @_('operands MATH operand')
    # def operands(self, p):
    #     return [p.operands, p.MATH, p.operand]

    @_('MEMORY_ADDRESS COMMA operands')
    def operands(self, p):
        return [p.MEMORY_ADDRESS] + p.operands

    @_('DECIMAL COMMA operands')
    def operands(self, p):
        return [p.DECIMAL] + p.operands

    @_('IMMEDIATE_DATA')
    def operand(self, p):
        return [p.IMMEDIATE_DATA]

    @_('MEMORY_ADDRESS')
    def operand(self, p):
        return [p.MEMORY_ADDRESS]

    @_('SPECIAL_CHARACTER')
    def operand(self, p):
        return [p.SPECIAL_CHARACTER]

    @_('DECIMAL')
    def operand(self, p):
        return [p.DECIMAL]

    @_('MATH_EXPRESSION')
    def operand(self, p):
        return [p.MATH_EXPRESSION]

    @_('SINGLE_QUOTED_CHAR')
    def operand(self, p):
        return [p.SINGLE_QUOTED_CHAR]

    def error(self, p):
        print(f"Syntax error at line: {p.lineno}")
        print(f"\t{p}")
        print()


def test_sly_lexer(code):
    lexer = I8080Lexer()
    print("Lexing-----------------------------------------------------------------------------------------------Lexing")
    for token in lexer.tokenize(code):
        if token.type == "INSTRUCTION":
            print(token)
            #  print("\t", token)
        else:
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


input_code = \
    """ LABEL1: MOV A, B ;Inline comment
        ADD M, 10H
        ;Line comment
        
        LABEL2: SUB H, L
        MOV C, M
            
        LABEL3: ADD A, 2050h
        ADD A, 2050H
        SUB B, 0x001A
        MOV M, A
        
        LABEL4:     MOV 0FH, 0x00CH
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
    fp16_file = """"""
    try:
        with open(file_path, 'r') as asm_file:
            fp16_file = asm_file.read()
            test_sly_lexer(fp16_file)
            test_sly_parser(fp16_file)

    except Exception as e:
        print(e)


test_fp16()
