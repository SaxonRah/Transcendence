# Transcendence
## A PL/M & Intel 8080 Assembly to Arm M0+ Translation Tool.
![](https://github.com/SaxonRah/Transcendence/blob/main/imgs/Transcendence.gif)

*__One day I'd like to see a tool that could translate 8080, 8085, 8086, 6502, Z80, M6800, M68000, i186, i286, i386, i486 to an ARM ISA.__*

*__This is the starting point of that dream.__*
## Overview
Transcendence is a translation tool designed to convert Intel 8080 assembly language code into Arm M0+ assembly language, targeting platforms like the Raspberry Pi RP2040. The tool also aims to transpile PL/M language code into Arm M0+ assembly language, facilitating compatibility with older systems requiring CP/M operating systems or similar environments. 

Transcendence aims to bridge the gap between legacy Intel 8080 and PL/M codebases and modern Arm Cortex-M0+ platforms like the Raspberry Pi RP2040. By providing a reliable and efficient translation mechanism, it enables the preservation and utilization of vintage software while leveraging the capabilities of contemporary hardware.

## Specification
Current specification is located here -> [Handling Differences a Specification](/specification/Handling_Differences_Specification.md)
- Note: The specification and playground code are NOT 1 to 1.
   - The `/python/playground/` drives the development of a better specification.
   - The `/python/spec/` directory contains a "working" specification example.

- [handling_differences.py](/python/spec/handling_differences.py)
   - This is now the same as [Handling Differences Specification](/specification/Handling_Differences_Specification.md).
   - Going forward, I will make an effort to follow this. The current playground doesn't follow this.

- [Dual RP2040's with Dual Core usage using Mailbox and UART](/specification/DualRP2040_DualCore_Mailbox.md)
   - 🐲🐉 Just for fun. Never assembled it. It probably has errors and won't work. 🐉🐲
   - Just wanted to write it before I forgot about wanting to try it.
   - Think of this as a little bonus M0+ assembly application. 😙

## Playground
You will find Intel 8080 assembly and PL/M regex patterns with subsequent pattern matching in the playground folder. This is where I try out ideas and work on designing the specification and development of Transcendence.

- CP/M 2.2 in PL/M is completely pattern matched and PL/M has a complete set of regexes.
   - Looking for more PL/M code to test.
- Intel 8080 assembly has a complete set of regexes.
   - Looking for more I8080 assembly to test.

- I've added the files that guided me to create the [Handling Differences Specification](/specification/Handling_Differences_Specification.md).
   - [I8080_M0Plus_Mappings.py](/python/playground/maps/I8080_M0Plus_Mappings.py)
   - [Translate_I8080_to_M0Plus.py](/python/playground/Translate_I8080_to_M0Plus.py)
      - 🐲🐉 These are not great or even good. These are what drove me to create a specification. 🐉🐲

## Features Desired
1. **Translation from Intel 8080 Assembly to Arm M0+ Assembly:**
   - Convert Intel 8080 assembly language instructions to equivalent Arm M0+ assembly instructions.
   - Handle differences in instruction formats, addressing modes, and operand types between the two architectures.
   - Ensure efficient translation to leverage the capabilities of the Arm M0+ processor.
   
2. **Transpilation of PL/M Code to Arm M0+ Assembly:**
   - Translate PL/M language constructs into Arm M0+ assembly language.
   - Support a wide range of PL/M syntax and constructs, including control structures, data types, and procedures.
   - Ensure compatibility with CP/M operating system requirements and other legacy systems.

3. **Pattern Matching and Parsing:**
   - Utilize regular expressions for pattern matching Intel 8080 assembly and PL/M language constructs.
   - Parse matched patterns to construct an Abstract Syntax Tree (AST) for subsequent translation.
   - Employ tools like LEX and YACC, or alternatives like PLY or SLY, for efficient parsing and AST generation.

4. **Optimization and Code Generation:**
   - Implement optimizations to improve the efficiency and performance of translated code.
   - Generate optimized Arm M0+ assembly code with consideration for resource constraints and execution speed.
   - Employ techniques such as instruction look-ahead for enhancing translation accuracy and performance.

5. **Modularity and Extensibility:**
   - Design Transcendence with a modular architecture to facilitate future enhancements and additions.
   - Allow for easy integration of new translation rules, optimizations, and target architectures.
   - Support multiple input and output formats to accommodate diverse usage scenarios.

## Motivation
Transcendence addresses the challenge of translating code between architectures with differing instruction sets and design philosophies. By enabling the conversion of legacy Intel 8080 and PL/M code to Arm M0+ assembly, it facilitates the utilization of modern hardware while preserving compatibility with vintage systems.

One day I'd like to see a tool that could translate 8080, 8085, 8086, 6502, Z80, M6800, M68000, i186, i286, i386, i486 to an ARM ISA. This is the starting point of that dream.

## Target Platform
Transcendence primarily targets the Raspberry Pi RP2040, which features the Arm Cortex-M0+ processor. The tool is optimized for the little-endian architecture of the RP2040, ensuring compatibility with its execution environment.

## Contribution
Contributions to Transcendence are welcome and encouraged. Interested developers can clone the project repository. Contribute enhancements. Fix Bugs. Add additional translation capabilities. Collaboration and feedback are essential for improving the tool.
