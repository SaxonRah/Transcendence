# I8080_to_M0Plus Transsembler
Translate or rather `transsemble` Intel 8080 Assembly to Cortex-M0+ Assembly.

This `transsembler` will target a Raspberry Pi RP2040 (M0+/ARMv6-M) from given Intel 8080 assembly.

# Transsembler
A `transsembler` is a word similar to a `transpiler`. A `transpiler` will translate code from a high-level language to another high-level language. A `transsembler` will translate a given assembly language to a different targeted assembly language. You can call this a `transpiler` if you wanted, as it technically isn't an a(ssembler) as the word suggests. Both words are badly coined.

# About
Provided is a comprehensive(?) list of regex patterns in python that should cover a wide variety of Intel 8080 code. A full complete list is impractical for the first go around, however I made a large attempt at both the instructions and assembler commands.

There is currently no M0Plus(m0+) translation code. This is being worked on.

# What the .... Why?!
I would like to see how feasable it is to create a `transsembler`. I choose the Intel 8080 and M0+ (RP2040) for a few reasons. Intel 8080 is a 8-bit CISC microprocessor. Intel 8080 is little-endian. The Cortex-M0+ is a 32-bit RISC microprocessor. M0+ can be either little-endian or big-endian. The targeted RP2040 is little-endian. 

1. Both the RP2040 and I8080 are Von Neumann architecture. Architecture, bit-width encapsulation, and endian-ness are the main reasons. It's a good match since the M0+ can more than reliably capture the essence of I8080. It's more like complete over-kill.
2. Direct CISC to RISC `transsembly` is a complelling problem to solve and persue. `Transsemmbly` between the two will require a very good `transsembler`, meaning lots of neat tricks like instruction look-ahead, can be employed to solve the problem. 
3. The RP2040 is very much like the I8080 in terms of homebrew and vintage clone computing usage. Take for example RunCPM or the 6502 and Z80 emulators on the RP2040. By directly translating assembly it prompts interesting further questions.
