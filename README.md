# I8080_to_M0Plus Transsembler

Translate or rather `transsemble` Intel 8080 Assembly to Cortex-M0+ Assembly. This `transsembler` will target a RPi RP2040 (M0+/ARMv6-M) from Intel 8080 assembly. This `transsembler` will also `transsemble` the PL/M language into M0+/ARMv6-M assembly.

There is currently no M0+ (ARMv6-M) translation code. This is being worked on. If you would like to contribute, don't hesitate, clone and go!

# Transsembler

A `transsembler` is like a `transpiler`. A `transpiler` will translate code from a high-level language to another high-level language. A `transsembler` will translate assembly language to a different targeted assembly language. You can call this a `transpiler` if you wanted, as it isn't an a(ssembler) as the word suggests. Both words are badly coined.

# About

Provided is a comprehensive(?) list of regex patterns in python that should cover a wide variety of Intel 8080 code. A good test here would be I8080 code from Rosetta Code. I've added a majority of PL/M regexes in python as well. Combined with I8080 assembly regexes, it should help cover a majority of I8080 code bases. CP/M in PL/M would be a good test here. It should be noted other PL/M code for other microprocessors could be used; for example the Z80. A full complete list of regexes for both I8080 assembly and PL/M language is impractical for the first go around. However, I made a large attempt at both the I8080 and a majority of the PL/M language. Both should have sufficent regexes to pattern match a large majority of I8080 assembly and PL/M.

# What the .... Why?!

I would like to see how feasable it is to create a `transsembler`. I choose the Intel 8080 and M0+ (RP2040) for a few reasons. Intel 8080 is a 8-bit CISC microprocessor. Intel 8080 is little-endian. The Cortex-M0+ is a 32-bit RISC microprocessor. M0+ can be either little-endian or big-endian. The targeted RP2040 is little-endian. 

1. Both the RP2040 and I8080 are Von Neumann architecture. Architecture, bit-width encapsulation, and endian-ness are the main reasons. It's a good match since the M0+ can more than reliably capture the essence of an I8080. The RP2040 is more like complete over-kill in comparison to the I8080.

2. Direct CISC to RISC `transsembly` is a complelling problem to solve and persue. `Transsemmbly` between the two will require a good `transsembler`. Which means lots of neat tricks like instruction look-ahead are needed. 

3. The RP2040 is very much like the I8080 in terms of homebrew and vintage clone computing usage. Take for example RunCPM or the 6502 and Z80 emulators on the RP2040. By directly translating assembly it prompts interesting further questions.

4. `Transsembling` or `Transpiling` PL/M code into M0+(ARMv6-M) will provide a wide range of software for testing the `transsembler`. Which if completed would be very useful to interfacing with older systems that would require CP/M operating system or other systems.
