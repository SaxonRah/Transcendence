import re

from Patterns_PLM import *


def match_plm_code(code):
    patterns = {
        "arithmetic": [add_pattern, sub_pattern, mul_pattern, div_pattern,
                       and_pattern, or_pattern, xor_pattern, not_pattern],

        "control_transfer": [jmp_pattern, jz_pattern, jnz_pattern, jc_pattern,
                             jnc_pattern, call_pattern, ret_pattern],

        "data_transfer": [mov_pattern, xchg_pattern, push_pattern, pop_pattern,
                          ldi_pattern, ldx_pattern, stx_pattern, lea_pattern],

        "shift_rotate": [shl_pattern, shr_pattern, rol_pattern, ror_pattern],

        "miscellaneous": [nop_pattern, hlt_pattern, in_pattern, out_pattern],

        "directives": [equ_pattern, org_pattern, end_pattern, include_pattern,
                       title_pattern, segment_pattern, ends_pattern, assume_pattern,
                       public_pattern, extern_pattern, db_pattern, dw_pattern,
                       ds_pattern, include_lib_pattern],

        "comments": [comment_pattern]
    }

    matched_lines = {match_category: [] for match_category in patterns.keys()}

    for line in code.split('\n'):
        for category, category_patterns in patterns.items():
            for pattern in category_patterns:
                if re.match(pattern, line.strip(), re.IGNORECASE):
                    matched_lines[category].append(line.strip())
                    break

    return matched_lines


def test_match_plm_code():
    # Test with example PL/M code provided as a string
    plm_code = """
    ORG 100H
    START:  MOV AX, 5
            MOV BX, 10
            ADD AX, BX
            JMP END
    END:    HLT
    """

    matches = match_plm_code(plm_code)
    for category, lines in matches.items():
        if lines:
            print(f"{category.capitalize()} Matches:")
            for line in lines:
                print(line)
            print()

    # Test with a PL/M file
    plm_file_path = "example_asm/cpm22.ASM"
    print("\nTesting with PL/M file:")
    try:
        with open(plm_file_path, 'r') as plm_file:
            for line in plm_file:
                matches = match_plm_code(line)
                for category, lines in matches.items():
                    if lines:
                        print(f"{category.capitalize()} Matches:")
                        for match_line in lines:
                            print(match_line.strip())  # Ensure leading/trailing whitespace is removed
    except Exception as e:
        print(e)


if __name__ == "__main__":
    test_match_plm_code()
