#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~INSTRUCTION MATCHING
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Arithmetic and Logic Instructions
add_pattern = r'ADD\s+(?:[A-Z]|[@#])'
sub_pattern = r'SUB\s+(?:[A-Z]|[@#])'
mul_pattern = r'MUL\s+(?:[A-Z]|[@#])'
div_pattern = r'DIV\s+(?:[A-Z]|[@#])'
and_pattern = r'AND\s+(?:[A-Z]|[@#])'
or_pattern = r'OR\s+(?:[A-Z]|[@#])'
xor_pattern = r'XOR\s+(?:[A-Z]|[@#])'
not_pattern = r'NOT\s+(?:[A-Z]|[@#])'

# Control Transfer Instructions
jmp_pattern = r'JMP\s+(?:[A-Z]|[@#])'
jz_pattern = r'JZ\s+(?:[A-Z]|[@#])'
jnz_pattern = r'JNZ\s+(?:[A-Z]|[@#])'
jc_pattern = r'JC\s+(?:[A-Z]|[@#])'
jnc_pattern = r'JNC\s+(?:[A-Z]|[@#])'
call_pattern = r'CALL\s+(?:[A-Z]|[@#])'
ret_pattern = r'RET'

# Data Transfer Instructions
mov_pattern = r'MOV\s+(?:[A-Z]|[@#]),\s*(?:[A-Z]|[@#])'
xchg_pattern = r'XCHG\s+(?:[A-Z]|[@#]),\s*(?:[A-Z]|[@#])'
push_pattern = r'PUSH\s+(?:[A-Z]|[@#])'
pop_pattern = r'POP\s+(?:[A-Z]|[@#])'
ldi_pattern = r'LDI\s+(?:[A-Z]|[@#]),\s*(?:[A-Z]|[@#])'
ldx_pattern = r'LDX\s+(?:[A-Z]|[@#]),\s*(?:[A-Z]|[@#])'
stx_pattern = r'STX\s+(?:[A-Z]|[@#]),\s*(?:[A-Z]|[@#])'
lea_pattern = r'LEA\s+(?:[A-Z]|[@#]),\s*(?:[A-Z]|[@#])'

# Shift and Rotate Instructions
shl_pattern = r'SHL\s+(?:[A-Z]|[@#])'
shr_pattern = r'SHR\s+(?:[A-Z]|[@#])'
rol_pattern = r'ROL\s+(?:[A-Z]|[@#])'
ror_pattern = r'ROR\s+(?:[A-Z]|[@#])'

# Miscellaneous Instructions
nop_pattern = r'NOP'
hlt_pattern = r'HLT'
in_pattern = r'IN\s+(?:[A-Z]|[@#])'
out_pattern = r'OUT\s+(?:[A-Z]|[@#])'

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ASSEMBLER MATCHING
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Assembler Directives
equ_pattern = r'^\s*(\w+)\s*=\s*(.+)$'
org_pattern = r'^\s*ORG\s+(.+)$'
end_pattern = r'^\s*END$'
include_pattern = r'^\s*INCLUDE\s+(.+)$'
title_pattern = r'^\s*TITLE\s+"(.+)"$'
segment_pattern = r'^\s*SEGMENT\s+(.+)$'
ends_pattern = r'^\s*ENDS\s+(.+)$'
assume_pattern = r'^\s*ASSUME\s+(.+)$'
public_pattern = r'^\s*PUBLIC\s+(.+)$'
extern_pattern = r'^\s*EXTERN\s+(.+)$'
db_pattern = r'^\s*DB\s+(.+)$'
dw_pattern = r'^\s*DW\s+(.+)$'
ds_pattern = r'^\s*DS\s+(.+)$'
include_lib_pattern = r'^\s*INCLUDELIB\s+"(.+)"$'

# Comments
comment_pattern = r';.*$'

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~OPERAND MATCHING
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Operand Patterns
identifier_pattern = r'[A-Za-z_][A-Za-z0-9_]*'
number_pattern = r'(?:\d+)|(?:0x[0-9A-Fa-f]+)|(?:0[0-7]+)|(?:0b[01]+)|(?:0c[0-7]+)'
memory_pattern = r'\[\s*(?:[A-Za-z_][A-Za-z0-9_]*|[0-9]+)\s*\]'
immediate_pattern = r'#\s*(?:\d+)|(?:0x[0-9A-Fa-f]+)|(?:0[0-7]+)|(?:0b[01]+)|(?:0c[0-7]+)'
register_pattern = r'(?:AX|BX|CX|DX|SI|DI|SP|BP|CS|DS|ES|SS)'
register_memory_pattern = r'(?:[A-Za-z_][A-Za-z0-9_]*|[0-9]+)?(?:\+[A-Za-z_][A-Za-z0-9_]*|[0-9]+)?'
