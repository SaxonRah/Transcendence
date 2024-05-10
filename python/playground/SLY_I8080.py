from sly import Lexer, Parser


class I8080Lexer(Lexer):
    tokens = {
        LABEL, INSTRUCTION, REGISTER, IMMEDIATE_DATA, MEMORY_ADDRESS, COMMA
    }

    ignore = ' \t'
    ignore_comment = r';.*'

    LABEL = r'\w+:'
    INSTRUCTION = r'(MOV|ADD|SUB)'  # Define all instructions
    REGISTER = r'[A-HL]|M'
    IMMEDIATE_DATA = r'(0[xX][0-9A-Fa-f]+|\d+)[Hh]?'
    MEMORY_ADDRESS = r'\w+'
    COMMA = r','

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

    @_('program statement')
    def program(self, p):
        p.program.append(p.statement)
        return p.program

    @_('')
    def program(self, p):
        return []

    @_('statement')
    def program(self, p):
        return [p.statement]

    @_('LABEL statement')
    def statement(self, p):
        return ('LABEL', p.LABEL, p.statement)

    @_('INSTRUCTION operands')
    def statement(self, p):
        return ('INSTRUCTION', p.INSTRUCTION, p.operands)

    @_('operand COMMA operand')
    def operands(self, p):
        return (p.operand0, p.operand1)

    @_('operand')
    def operands(self, p):
        return (p.operand)

    @_('REGISTER')
    def operand(self, p):
        return p[0]

    @_('IMMEDIATE_DATA')
    def operand(self, p):
        return p[0]

    @_('MEMORY_ADDRESS')
    def operand(self, p):
        return p[0]

    def error(self, p):
        print(f"Syntax error at line {p.lineno}")
        print(f"Syntax error: {p}")


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
        """

test_sly_lexer(input_code)
test_sly_parser(input_code)
