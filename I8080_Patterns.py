#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~INSTRUCTION MATCHING
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mov_regex_pattern = r'MOV\s+(?:[BCEHLMA]),\s*(?:[BCEHLMA])'
arithmetic_regex_pattern = r'(?:ADD|ADC|SUB|SBB|ANA|XRA|ORA|CMP)\s+(?:B|C|D|E|H|L|M|A)'
nop_pattern = r'NOP'
lxi_pattern = r'LXI\s+(?:[BDEHLSP]),\s*(?:\w{2})'
stax_pattern = r'STAX\s+(?:[BDEHL])'
inx_pattern = r'INX\s+(?:[BDEHLSP])'
inr_pattern = r'DCR\s+(?:[BDEHLA])'
mvi_pattern = r'MVI\s+(?:[BDEHLA]),\s*(?:\w{2})'
rlc_pattern = r'RLC'
dad_pattern = r'DAD\s+(?:[BDEHLSP])'
ldax_pattern = r'LDAX\s+(?:[BDEHL])'
dcx_pattern = r'DCX\s+(?:[BDEHLSP])'
ral_pattern = r'RAL'
rar_pattern = r'RAR'
shld_pattern = r'SHLD\s+(?:\w{4})'
daa_pattern = r'DAA'
lhld_pattern = r'LHLD\s+(?:\w{4})'
cma_pattern = r'CMA'
sta_pattern = r'STA\s+(?:\w{4})'
stc_pattern = r'STC'
lda_pattern = r'LDA\s+(?:\w{4})'
cmc_pattern = r'CMC'
rnz_pattern = r'RNZ'
pop_b_pattern = r'POP\s+B'
jnz_pattern = r'JNZ\s+(?:\w{4})'
jmp_pattern = r'JMP\s+(?:\w{4})'
# jmp_pattern = r'(?P<opcode>JMP)\s+(?P<label>\w+)'
cnz_pattern = r'CNZ\s+(?:\w{4})'
push_b_pattern = r'PUSH\s+B'
adi_pattern = r'ADI\s+(?:\w{2})'
rst_0_pattern = r'RST\s+0'
rz_pattern = r'RZ'
ret_pattern = r'RET'
jz_pattern = r'JZ\s+(?:\w{4})'
cz_pattern = r'CZ\s+(?:\w{4})'
call_pattern = r'CALL\s+(?:\w{4})'
aci_pattern = r'ACI\s+(?:\w{2})'
rst_1_pattern = r'RST\s+1'
rnc_pattern = r'RNC'
pop_d_pattern = r'POP\s+D'
jnc_pattern = r'JNC\s+(?:\w{4})'
out_pattern = r'OUT\s+(?:\w{2})'
cnc_pattern = r'CNC\s+(?:\w{4})'
push_d_pattern = r'PUSH\s+D'
sui_pattern = r'SUI\s+(?:\w{2})'
rst_2_pattern = r'RST\s+2'
rc_pattern = r'RC'
jc_pattern = r'JC\s+(?:\w{4})'
in_pattern = r'IN\s+(?:\w{2})'
cc_pattern = r'CC\s+(?:\w{4})'
sbi_pattern = r'SBI\s+(?:\w{2})'
rst_3_pattern = r'RST\s+3'
rpo_pattern = r'RPO'
pop_h_pattern = r'POP\s+H'
jpo_pattern = r'JPO\s+(?:\w{4})'
xthl_pattern = r'XTHL'
cpo_pattern = r'CPO\s+(?:\w{4})'
push_h_pattern = r'PUSH\s+H'
ani_pattern = r'ANI\s+(?:\w{2})'
rst_4_pattern = r'RST\s+4'
rpe_pattern = r'RPE'
pchl_pattern = r'PCHL'
jpe_pattern = r'JPE\s+(?:\w{4})'
xchg_pattern = r'XCHG'
cpe_pattern = r'CPE\s+(?:\w{4})'
xri_pattern = r'XRI\s+(?:\w{2})'
rst_5_pattern = r'RST\s+5'
rp_pattern = r'RP'
pop_psw_pattern = r'POP\s+PSW'
jp_pattern = r'JP\s+(?:\w{4})'
di_pattern = r'DI'
cp_pattern = r'CP\s+(?:\w{4})'
push_psw_pattern = r'PUSH\s+PSW'
ori_pattern = r'ORI\s+(?:\w{2})'
rst_6_pattern = r'RST\s+6'
rm_pattern = r'RM'
sphl_pattern = r'SPHL'
jm_pattern = r'JM\s+(?:\w{4})'
ei_pattern = r'EI'
cm_pattern = r'CM\s+(?:\w{4})'
cpi_pattern = r'CPI\s+(?:\w{2})'
rst_7_pattern = r'RST\s+7'
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ASSEMBLER MATCHING
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
equ_pattern = r'^\s*(\w+)\s*EQU\s*(\w+)\s*;\s*(.*)$'
db_pattern = r'^\s*DB\s*((?:\w{2}\s*,\s*)*\w{2})\s*;\s*(.*)$'
dw_pattern = r'^\s*DW\s*(\w+)\s*;\s*(.*)$'
function_pattern = r'^\s*(\w+)\s*;\s*(.*)$'
org_pattern = r'^\s*ORG\s*(\w+)\s*;\s*(.*)$'                                # Uses re.MULTILINE
end_pattern = r'^\s*END\s*;\s*(.*)$'                                        # Uses re.MULTILINE
include_pattern = r'^\s*INCLUDE\s*["\']([^"\']+)["\']\s*;\s*(.*)$'          # Uses re.MULTILINE
if_else_endif_pattern = r'^\s*(IF|ELSE|ENDIF)\s*;\s*(.*)$'                  # Uses re.MULTILINE
macro_mend_pattern = r'^\s*(MACRO|MEND)\s*;\s*(.*)$'                        # Uses re.MULTILINE
repeat_endr_pattern = r'^\s*(REPEAT|ENDR)\s*;\s*(.*)$'                      # Uses re.MULTILINE
title_pattern = r'^\s*TITLE\s*["\']([^"\']+)["\']\s*;\s*(.*)$'              # Uses re.MULTILINE
public_extern_pattern = r'^\s*(PUBLIC|EXTERN)\s*(\w+)\s*;\s*(.*)$'          # Uses re.MULTILINE
section_segment_pattern = r'^\s*(SECTION|SEGMENT)\s*(\w+)\s*;\s*(.*)$'      # Uses re.MULTILINE
align_pattern = r'^\s*ALIGN\s*(\d+)\s*;\s*(.*)$'                            # Uses re.MULTILINE
eject_pattern = r'^\s*EJECT\s*;\s*(.*)$'                                    # Uses re.MULTILINE
dbyte_dres_pattern = r'^\s*(DBYTE|DRES)\s*(\d+)\s*;\s*(.*)$'                # Uses re.MULTILINE
word_resw_pattern = r'^\s*(WORD|RESW)\s*(\d+)\s*;\s*(.*)$'                  # Uses re.MULTILINE
fill_pattern = r'^\s*FILL\s*(\w+)\s*;\s*(.*)$'                              # Uses re.MULTILINE
includelib_pattern = r'^\s*INCLUDELIB\s*["\']([^"\']+)["\']\s*;\s*(.*)$'    # Uses re.MULTILINE
comment_pattern = r';.*$'                                                   # Uses re.MULTILINE

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~OPERAND MATCHING
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Matching types of operand field information
register_pattern = r'[A-HL]|M'
register_pair_pattern = r'B|D|H|SP'
immediate_data_pattern = r'([0-9A-F]+[Hh])|(\d+)'
memory_address_pattern = r'\w+'

# Matching specifying operand field information
hexadecimal_data_pattern = r'0[xX][0-9A-Fa-f]+'
decimal_data_pattern = r'\d+'
octal_data_pattern = r'0[Oo]?[0-7]+'
binary_data_pattern = r'[01]+'
program_counter_pattern = r'\$'
ascii_constant_pattern = r"'.'"
labels_assigned_values_pattern = r'\w+\s*=\s*[0-9A-F]+'
labels_of_instructions_pattern = r'\w+'
expressions_pattern = r'.+'
