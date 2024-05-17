# TODO: Fix this trash.
#  So much is wrong, it's almost not even worth fixing.
#  Uses ASSEM_I8080.py which is also trash that first needs to be fixed.
#  ASSEM_I8080.py generates 'new_8080_fp16.HEX' and this should read that HEX and link.
#  ATM it does 'link' the 'new_8080_fp16.HEX' if you can even call it linking, since it's not even remotely correct.
#  If the '8080_fp16.HEX' is read, it produces the Error:
#  data_bytes = [int(line[i:i+2], 16) for i in range(9, 9 + byte_count * 2, 2)]
#  ValueError: invalid literal for int() with base 16: ''
#       That line is hardcoded to accept the 'new_8080_fp16.HEX' format.

def read_i8080_hex_file(hex_file_path):
    data = []  # a list of tuples containing address and data.
    with open(hex_file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        record_type = int(line[7:9], 16)
        if record_type == 0:  # Data record
            address = int(line[3:7], 16)
            byte_count = int(line[1:3], 16)
            data_bytes = [int(line[i:i+2], 16) for i in range(9, 9 + byte_count * 2, 2)]
            data.append((address, data_bytes))
    return data


def link_i8080_hex_file(hex_file_path):
    data = read_i8080_hex_file(hex_file_path)
    linked_data = []
    base_address = None
    for address, data_bytes in data:
        if base_address is None:
            base_address = address
        offset = address - base_address
        linked_data.extend([(offset + i, byte) for i, byte in enumerate(data_bytes)])
    return linked_data


def test_link_i8080_hex_file():
    hex_file = '../../example_asm/8080_fp16.HEX'
    # hex_file = '../example_asm/new_8080_fp16.HEX'
    linked_data = link_i8080_hex_file(hex_file)
    print(linked_data)


if __name__ == "__main__":
    test_link_i8080_hex_file()
