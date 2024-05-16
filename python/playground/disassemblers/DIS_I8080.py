# TODO: Finish ASSEM_I8080.py and LINK_I8080.py
#  Then finish this trash. ~ Like disassemble the resultant BIN file from the ASSEM_I8080.py and LINK_I8080.py

def disassemble(buffer, pc):
    opcode = buffer[pc]
    opbytes = 1
    print("0x%04x  " % pc, end="")

    if opcode in [0x00, 0x08, 0x10, 0x18, 0x28, 0x38, 0xcb, 0xd9, 0xdd, 0xed, 0xfd]:
        print("NOP")
    elif opcode == 0x01:
        print("LXI\tB, #$0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0x02:
        print("STAX\tB")
    elif opcode == 0x03:
        print("INX\tB")
    elif opcode == 0x04:
        print("INR\tB")
    elif opcode == 0x05:
        print("DCR\tB")
    elif opcode == 0x06:
        print("MVI\tB, #$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0x07:
        print("RLC")
    elif opcode == 0x09:
        print("DAD\tB")
    elif opcode == 0x0a:
        print("LDAX\tB")
    elif opcode == 0x0b:
        print("DCX\tB")
    elif opcode == 0x0c:
        print("INR\tC")
    elif opcode == 0x0d:
        print("DCR\tC")
    elif opcode == 0x0e:
        print("MVI\tC, #$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0x0f:
        print("RRC")
    elif opcode == 0x11:
        print("LXI\tD, #$0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0x12:
        print("STAX\tD")
    elif opcode == 0x13:
        print("INX\tD")
    elif opcode == 0x14:
        print("INR\tD")
    elif opcode == 0x15:
        print("DCR\tD")
    elif opcode == 0x16:
        print("MVI\tD, #$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0x17:
        print("RAL")
    elif opcode == 0x19:
        print("DAD\tD")
    elif opcode == 0x1a:
        print("LDAX\tD")
    elif opcode == 0x1b:
        print("DCX\tD")
    elif opcode == 0x1c:
        print("INR\tE")
    elif opcode == 0x1d:
        print("DCR\tE")
    elif opcode == 0x1e:
        print("MVI\tE, #$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0x1f:
        print("RAR")
    elif opcode == 0x20:
        print("RIM")
    elif opcode == 0x21:
        print("LXI\tH, #$0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0x22:
        print("SHLD\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0x23:
        print("INX\tH")
    elif opcode == 0x24:
        print("INR\tH")
    elif opcode == 0x25:
        print("DCR\tH")
    elif opcode == 0x26:
        print("MVI\tH, #$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0x27:
        print("DAA")
    elif opcode == 0x29:
        print("DAD\tH")
    elif opcode == 0x2a:
        print("LHLD\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0x2b:
        print("DCX\tH")
    elif opcode == 0x2c:
        print("INR\tL")
    elif opcode == 0x2d:
        print("DCR\tL")
    elif opcode == 0x2e:
        print("MVI\tL, #$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0x2f:
        print("CMA")
    elif opcode == 0x30:
        print("SIM")
    elif opcode == 0x31:
        print("LXI\tSP, #$0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0x32:
        print("STA\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0x33:
        print("INX\tSP")
    elif opcode == 0x34:
        print("INR\tM")
    elif opcode == 0x35:
        print("DCR\tM")
    elif opcode == 0x36:
        print("MVI\tM, #$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0x37:
        print("STC")
    elif opcode == 0x39:
        print("DAD\tSP")
    elif opcode == 0x3a:
        print("LDA\t0x%02x%02X" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0x3b:
        print("DCX\tSP")
    elif opcode == 0x3c:
        print("INR\tA")
    elif opcode == 0x3d:
        print("DCR\tA")
    elif opcode == 0x3e:
        print("MVI\tA, #$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0x3f:
        print("CMC")
    elif opcode == 0x40:
        print("MOV\tB, B")
    elif opcode == 0x41:
        print("MOV\tB, C")
    elif opcode == 0x42:
        print("MOV\tB, D")
    elif opcode == 0x43:
        print("MOV\tB, E")
    elif opcode == 0x44:
        print("MOV\tB, H")
    elif opcode == 0x45:
        print("MOV\tB, L")
    elif opcode == 0x46:
        print("MOV\tB, M")
    elif opcode == 0x47:
        print("MOV\tB, A")
    elif opcode == 0x48:
        print("MOV\tC, B")
    elif opcode == 0x49:
        print("MOV\tC, C")
    elif opcode == 0x4a:
        print("MOV\tC, D")
    elif opcode == 0x4b:
        print("MOV\tC, E")
    elif opcode == 0x4c:
        print("MOV\tC, H")
    elif opcode == 0x4d:
        print("MOV\tC, L")
    elif opcode == 0x4e:
        print("MOV\tC, M")
    elif opcode == 0x4f:
        print("MOV\tC, A")
    elif opcode == 0x50:
        print("MOV\tD, B")
    elif opcode == 0x51:
        print("MOV\tD, C")
    elif opcode == 0x52:
        print("MOV\tD, D")
    elif opcode == 0x53:
        print("MOV\tD, E")
    elif opcode == 0x54:
        print("MOV\tD, H")
    elif opcode == 0x55:
        print("MOV\tD, L")
    elif opcode == 0x56:
        print("MOV\tD, M")
    elif opcode == 0x57:
        print("MOV\tD, A")
    elif opcode == 0x58:
        print("MOV\tE, B")
    elif opcode == 0x59:
        print("MOV\tE, C")
    elif opcode == 0x5a:
        print("MOV\tE, D")
    elif opcode == 0x5b:
        print("MOV\tE, E")
    elif opcode == 0x5c:
        print("MOV\tE, H")
    elif opcode == 0x5d:
        print("MOV\tE, L")
    elif opcode == 0x5e:
        print("MOV\tE, M")
    elif opcode == 0x5f:
        print("MOV\tE, A")
    elif opcode == 0x60:
        print("MOV\tH, B")
    elif opcode == 0x61:
        print("MOV\tH, C")
    elif opcode == 0x62:
        print("MOV\tH, D")
    elif opcode == 0x63:
        print("MOV\tH, E")
    elif opcode == 0x64:
        print("MOV\tH, H")
    elif opcode == 0x65:
        print("MOV\tH, L")
    elif opcode == 0x66:
        print("MOV\tH, M")
    elif opcode == 0x67:
        print("MOV\tH, A")
    elif opcode == 0x68:
        print("MOV\tL, B")
    elif opcode == 0x69:
        print("MOV\tL, C")
    elif opcode == 0x6a:
        print("MOV\tL, D")
    elif opcode == 0x6b:
        print("MOV\tL, E")
    elif opcode == 0x6c:
        print("MOV\tL, H")
    elif opcode == 0x6d:
        print("MOV\tL, L")
    elif opcode == 0x6e:
        print("MOV\tL, M")
    elif opcode == 0x6f:
        print("MOV\tL, A")
    elif opcode == 0x70:
        print("MOV\tM, B")
    elif opcode == 0x71:
        print("MOV\tM, C")
    elif opcode == 0x72:
        print("MOV\tM, D")
    elif opcode == 0x73:
        print("MOV\tM, E")
    elif opcode == 0x74:
        print("MOV\tM, H")
    elif opcode == 0x75:
        print("MOV\tM, L")
    elif opcode == 0x76:
        print("HLT")
    elif opcode == 0x77:
        print("MOV\tM, A")
    elif opcode == 0x78:
        print("MOV\tA, B")
    elif opcode == 0x79:
        print("MOV\tA, C")
    elif opcode == 0x7a:
        print("MOV\tA, D")
    elif opcode == 0x7b:
        print("MOV\tA, E")
    elif opcode == 0x7c:
        print("MOV\tA, H")
    elif opcode == 0x7d:
        print("MOV\tA, L")
    elif opcode == 0x7e:
        print("MOV\tA, M")
    elif opcode == 0x7f:
        print("MOV\tA, A")
    elif opcode == 0x80:
        print("ADD\tB")
    elif opcode == 0x81:
        print("ADD\tC")
    elif opcode == 0x82:
        print("ADD\tD")
    elif opcode == 0x83:
        print("ADD\tE")
    elif opcode == 0x84:
        print("ADD\tH")
    elif opcode == 0x85:
        print("ADD\tL")
    elif opcode == 0x86:
        print("ADD\tM")
    elif opcode == 0x87:
        print("ADD\tA")
    elif opcode == 0x88:
        print("ADC\tB")
    elif opcode == 0x89:
        print("ADC\tC")
    elif opcode == 0x8a:
        print("ADC\tD")
    elif opcode == 0x8b:
        print("ADC\tE")
    elif opcode == 0x8c:
        print("ADC\tH")
    elif opcode == 0x8d:
        print("ADC\tL")
    elif opcode == 0x8e:
        print("ADC\tM")
    elif opcode == 0x8f:
        print("ADC\tA")
    elif opcode == 0x90:
        print("SUB\tB")
    elif opcode == 0x91:
        print("SUB\tC")
    elif opcode == 0x92:
        print("SUB\tD")
    elif opcode == 0x93:
        print("SUB\tE")
    elif opcode == 0x94:
        print("SUB\tH")
    elif opcode == 0x95:
        print("SUB\tL")
    elif opcode == 0x96:
        print("SUB\tM")
    elif opcode == 0x97:
        print("SUB\tA")
    elif opcode == 0x98:
        print("SBB\tB")
    elif opcode == 0x99:
        print("SBB\tC")
    elif opcode == 0x9a:
        print("SBB\tD")
    elif opcode == 0x9b:
        print("SBB\tE")
    elif opcode == 0x9c:
        print("SBB\tH")
    elif opcode == 0x9d:
        print("SBB\tL")
    elif opcode == 0x9e:
        print("SBB\tM")
    elif opcode == 0x9f:
        print("SBB\tA")
    elif opcode == 0xa0:
        print("ANA\tB")
    elif opcode == 0xa1:
        print("ANA\tC")
    elif opcode == 0xa2:
        print("ANA\tD")
    elif opcode == 0xa3:
        print("ANA\tE")
    elif opcode == 0xa4:
        print("ANA\tH")
    elif opcode == 0xa5:
        print("ANA\tL")
    elif opcode == 0xa6:
        print("ANA\tM")
    elif opcode == 0xa7:
        print("ANA\tA")
    elif opcode == 0xa8:
        print("XRA\tB")
    elif opcode == 0xa9:
        print("XRA\tC")
    elif opcode == 0xaa:
        print("XRA\tD")
    elif opcode == 0xab:
        print("XRA\tE")
    elif opcode == 0xac:
        print("XRA\tH")
    elif opcode == 0xad:
        print("XRA\tL")
    elif opcode == 0xae:
        print("XRA\tM")
    elif opcode == 0xaf:
        print("XRA\tA")
    elif opcode == 0xb0:
        print("ORA\tB")
    elif opcode == 0xb1:
        print("ORA\tC")
    elif opcode == 0xb2:
        print("ORA\tD")
    elif opcode == 0xb3:
        print("ORA\tE")
    elif opcode == 0xb4:
        print("ORA\tH")
    elif opcode == 0xb5:
        print("ORA\tL")
    elif opcode == 0xb6:
        print("ORA\tM")
    elif opcode == 0xb7:
        print("ORA\tA")
    elif opcode == 0xb8:
        print("CMP\tB")
    elif opcode == 0xb9:
        print("CMP\tC")
    elif opcode == 0xba:
        print("CMP\tD")
    elif opcode == 0xbb:
        print("CMP\tE")
    elif opcode == 0xbc:
        print("CMP\tH")
    elif opcode == 0xbd:
        print("CMP\tL")
    elif opcode == 0xbe:
        print("CMP\tM")
    elif opcode == 0xbf:
        print("CMP\tA")
    elif opcode == 0xc0:
        print("RNZ")
    elif opcode == 0xc1:
        print("POP\tB")
    elif opcode == 0xc2:
        print("JNZ\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xc3:
        print("JMP\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xc4:
        print("CNZ\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xc5:
        print("PUSH\tB")
    elif opcode == 0xc6:
        print("ADI\t#$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0xc7:
        print("RST\t0")
    elif opcode == 0xc8:
        print("RZ")
    elif opcode == 0xc9:
        print("RET")
    elif opcode == 0xca:
        print("JZ\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xcb:
        print("JMP\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xcc:
        print("CZ\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xcd:
        print("CALL\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xce:
        print("ACI\t#$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0xcf:
        print("RST\t1")
    elif opcode == 0xd0:
        print("RNC")
    elif opcode == 0xd1:
        print("POP\tD")
    elif opcode == 0xd2:
        print("JNC\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xd3:
        print("OUT\t#$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0xd4:
        print("CNC\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xd5:
        print("PUSH\tD")
    elif opcode == 0xd6:
        print("SUI\t#$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0xd7:
        print("RST\t2")
    elif opcode == 0xd8:
        print("RC")
    elif opcode == 0xd9:
        print("RET")
    elif opcode == 0xda:
        print("JC\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xdb:
        print("IN\t#$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0xdc:
        print("CC\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xdd:
        print("CALL\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xde:
        print("SBI\t#$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0xdf:
        print("RST\t3")
    elif opcode == 0xe0:
        print("RPO")
    elif opcode == 0xe1:
        print("POP\tH")
    elif opcode == 0xe2:
        print("JPO\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xe3:
        print("XTHL")
    elif opcode == 0xe4:
        print("CPO\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xe5:
        print("PUSH\tH")
    elif opcode == 0xe6:
        print("ANI\t#$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0xe7:
        print("RST\t4")
    elif opcode == 0xe8:
        print("RPE")
    elif opcode == 0xe9:
        print("PCHL")
    elif opcode == 0xea:
        print("JPE\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xeb:
        print("XCHG")
    elif opcode == 0xec:
        print("CPE\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xed:
        print("CALL\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xee:
        print("XRI\t#$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0xef:
        print("RST\t5")
    elif opcode == 0xf0:
        print("RP")
    elif opcode == 0xf1:
        print("POP\tPSW")
    elif opcode == 0xf2:
        print("JP\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xf3:
        print("DI")
    elif opcode == 0xf4:
        print("CP\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xf5:
        print("PUSH\tPSW")
    elif opcode == 0xf6:
        print("ORI\t#$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0xf7:
        print("RST\t6")
    elif opcode == 0xf8:
        print("RM")
    elif opcode == 0xf9:
        print("SPHL")
    elif opcode == 0xfa:
        print("JM\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xfb:
        print("EI")
    elif opcode == 0xfc:
        print("CM\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xfd:
        print("CALL\t0x%02x%02x" % (buffer[pc + 2], buffer[pc + 1]))
        opbytes = 3
    elif opcode == 0xfe:
        print("CPI\t#$0x%02x" % buffer[pc + 1])
        opbytes = 2
    elif opcode == 0xff:
        print("RST\t7")

    return opbytes


def disassemble_buffer(buffer):
    pc = 0
    while pc < len(buffer):
        pc += disassemble(buffer, pc)


def convert_to_hex(binary_file_path):
    with open(binary_file_path, 'rb') as f:
        binary_data = f.read()
        hex_representation = ' '.join(['{:02x}'.format(byte) for byte in binary_data])
    return hex_representation


def disassemble_8080_binary(binary_file_path):
    hex_representation = convert_to_hex(binary_file_path)
    bytes_list = [int(byte, 16) for byte in hex_representation.split()]
    disassemble_buffer(bytes_list)


def read_hex_file(hex_file_path):
    with open(hex_file_path, 'r') as f:
        lines = f.readlines()
    buffer = []
    for line in lines:
        # Extract data bytes from each line and convert them to integers
        data_bytes = [int(line[i:i+2], 16) for i in range(9, len(line)-2, 2)]
        buffer.extend(data_bytes)
    return buffer


def test_disassemble_buffer():
    #  buffer = [0x3e, 0x05, 0x32, 0x00, 0x80, 0x3e, 0x08, 0x32, 0x00, 0x81, 0x3e, 0x00, 0x32, 0x00, 0x82, 0xc9]
    #  disassemble_buffer(buffer)

    hex_file_path = '../example_asm/8080_fp16.HEX'
    buffer = read_hex_file(hex_file_path)
    disassemble_buffer(buffer)


def test_disassemble_8080_binary():
    binary_file_path = '../example_asm/8080_fp16.BIN'
    disassemble_8080_binary(binary_file_path)


if __name__ == "__main__":
    test_disassemble_buffer()
    #  test_disassemble_8080_binary()
