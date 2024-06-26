
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BINARY COMMA DECIMAL DIRECTIVE HEX INSTRUCTION LABEL MACRO MATH_EXPRESSION MEMORY_ADDRESS OCTAL QUOTED_CHARACTER REGISTERprogram :program : program statementprogram : statementstatement : LABELstatement : LABEL statementstatement : MACROstatement : MACRO operandsstatement : MACRO operands MACROstatement : DIRECTIVE operandsstatement : INSTRUCTIONstatement : INSTRUCTION operandsoperands : operands COMMA operandoperands : operandoperand : QUOTED_CHARACTERoperand : REGISTERoperand : HEXoperand : DECIMALoperand : OCTALoperand : BINARYoperand : MEMORY_ADDRESSoperand : expressionexpression : MATH_EXPRESSIONexpression : operand MATH_EXPRESSION operandsoperand : MATH_EXPRESSION operand'
    
_lr_action_items = {'LABEL':([0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,25,26,27,],[3,3,-3,3,-6,-10,-2,-5,-7,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-9,-11,-8,-24,-12,-23,]),'MACRO':([0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,25,26,27,],[4,4,-3,4,-6,-10,-2,-5,22,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-9,-11,-8,-24,-12,-23,]),'DIRECTIVE':([0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,25,26,27,],[5,5,-3,5,-6,-10,-2,-5,-7,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-9,-11,-8,-24,-12,-23,]),'INSTRUCTION':([0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,25,26,27,],[6,6,-3,6,-6,-10,-2,-5,-7,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-9,-11,-8,-24,-12,-23,]),'$end':([0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,25,26,27,],[-1,0,-3,-4,-6,-10,-2,-5,-7,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-9,-11,-8,-24,-12,-23,]),'QUOTED_CHARACTER':([4,5,6,19,23,24,],[11,11,11,11,11,11,]),'REGISTER':([4,5,6,19,23,24,],[12,12,12,12,12,12,]),'HEX':([4,5,6,19,23,24,],[13,13,13,13,13,13,]),'DECIMAL':([4,5,6,19,23,24,],[14,14,14,14,14,14,]),'OCTAL':([4,5,6,19,23,24,],[15,15,15,15,15,15,]),'BINARY':([4,5,6,19,23,24,],[16,16,16,16,16,16,]),'MEMORY_ADDRESS':([4,5,6,19,23,24,],[17,17,17,17,17,17,]),'MATH_EXPRESSION':([4,5,6,10,11,12,13,14,15,16,17,18,19,23,24,25,26,27,],[19,19,19,24,-14,-15,-16,-17,-18,-19,-20,-21,19,19,19,24,24,-23,]),'COMMA':([9,10,11,12,13,14,15,16,17,18,19,20,21,25,26,27,],[23,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,23,23,-24,-12,23,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'statement':([0,1,3,],[2,7,8,]),'operands':([4,5,6,24,],[9,20,21,27,]),'operand':([4,5,6,19,23,24,],[10,10,10,25,26,10,]),'expression':([4,5,6,19,23,24,],[18,18,18,18,18,18,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> <empty>','program',0,'p_program_empty','PLY_I8080_NonBacktracking.py',142),
  ('program -> program statement','program',2,'p_program_statements','PLY_I8080_NonBacktracking.py',146),
  ('program -> statement','program',1,'p_program_statement','PLY_I8080_NonBacktracking.py',152),
  ('statement -> LABEL','statement',1,'p_statement_label','PLY_I8080_NonBacktracking.py',166),
  ('statement -> LABEL statement','statement',2,'p_statement_label_statement','PLY_I8080_NonBacktracking.py',170),
  ('statement -> MACRO','statement',1,'p_statement_macro','PLY_I8080_NonBacktracking.py',174),
  ('statement -> MACRO operands','statement',2,'p_statement_macro_operands','PLY_I8080_NonBacktracking.py',178),
  ('statement -> MACRO operands MACRO','statement',3,'p_statement_macro_operands_macro','PLY_I8080_NonBacktracking.py',182),
  ('statement -> DIRECTIVE operands','statement',2,'p_statement_directive_operands','PLY_I8080_NonBacktracking.py',186),
  ('statement -> INSTRUCTION','statement',1,'p_statement_instruction','PLY_I8080_NonBacktracking.py',190),
  ('statement -> INSTRUCTION operands','statement',2,'p_statement_instruction_operands','PLY_I8080_NonBacktracking.py',194),
  ('operands -> operands COMMA operand','operands',3,'p_operands_comma_operand','PLY_I8080_NonBacktracking.py',198),
  ('operands -> operand','operands',1,'p_operands_operand','PLY_I8080_NonBacktracking.py',214),
  ('operand -> QUOTED_CHARACTER','operand',1,'p_operand_quoted_character','PLY_I8080_NonBacktracking.py',218),
  ('operand -> REGISTER','operand',1,'p_operand_register','PLY_I8080_NonBacktracking.py',222),
  ('operand -> HEX','operand',1,'p_operand_hex','PLY_I8080_NonBacktracking.py',226),
  ('operand -> DECIMAL','operand',1,'p_operand_decimal','PLY_I8080_NonBacktracking.py',230),
  ('operand -> OCTAL','operand',1,'p_operand_octal','PLY_I8080_NonBacktracking.py',234),
  ('operand -> BINARY','operand',1,'p_operand_binary','PLY_I8080_NonBacktracking.py',238),
  ('operand -> MEMORY_ADDRESS','operand',1,'p_operand_memory_address','PLY_I8080_NonBacktracking.py',242),
  ('operand -> expression','operand',1,'p_operand_expression','PLY_I8080_NonBacktracking.py',246),
  ('expression -> MATH_EXPRESSION','expression',1,'p_expression_math_expression','PLY_I8080_NonBacktracking.py',251),
  ('expression -> operand MATH_EXPRESSION operands','expression',3,'p_expression_operand_math_expression_operands','PLY_I8080_NonBacktracking.py',255),
  ('operand -> MATH_EXPRESSION operand','operand',2,'p_operand_math_expression_operand','PLY_I8080_NonBacktracking.py',269),
]
