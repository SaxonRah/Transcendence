![](https://github.com/SaxonRah/Transcendence/blob/main/imgs/Transcendence.gif)
## What's in a name?
Quite a bit, apparently. ***Transcendence*** has a meaning and itself is a backronym:    
***Transcendence:*** The state of assembly code which **transcends** architectures.  
***T***<sup>echnique <sup>(for)</sup></sup> ***R***<sup>etroactively</sup> ***A***<sup>dapting</sup> ***N***<sup>umerous</sup> ***S***<sup>ource</sup> ***C***<sup>ode</sup> ***E***<sup>xpressions <sup>(and)</sup></sup> ***N***<sup>avigating</sup> ***D***<sup>iverse</sup> ***E***<sup>mbedded</sup> ***N***<sup>otation</sup> ***C***<sup>ontexts</sup> ***E***<sup>fficiently</sup>

## A PL/M & Intel 8080 Assembly to Arm M0+ Translation Tool.
- *__I dream of a translation tool for Assembly/Higher Level Languages to an ARM ISA:__*  
   - *__8-Bit: 8008, 8080, 8085, 6502, Z80, M6800__*  
   - *__16-Bit: 8086, Z800, Z8000, i186, i286__*  
   - *__32-Bit: Z80000, M68000, i386, i486__*
   - *__Languages: PL/M, Forth, Pascal__*

<sup>*__This is the starting point of that dream and tool.  
This is an extremely complex dream and will probably never be fully actualized.  
However I'm willing to try.__*</sup>

# NOTE - AUG 8th/9th 2024:
With the release of the Pico2 / RP2350, I will be switching over to utilize the M33 in the Pico2 rather than the M0+ in the Pico. 

This change will happen because the instruction set has changed from Thumb-1 on the Pico/M0+ to Thumb-2 on the Pico2/M33. 

This is a massive change if you worked with Thumb1/Thumb2. Thumb-1 has a limited set of instructions, while Thumb-2 extends this with more complex instructions similar to the full ARM instruction set.

Thumb-2 will allow for much faster and overall better conversion of instruction set to instruction set. In fact many of the pitfalls and problems I've encountered with Thumb-1 can be rectified with the usage of Thumb-2.

I was considering giving up on the Pico entirely because of Thumb-1. It's not really suited for this kind of project where as Thumb-2 more suits the level of complexity required.

For what it's worth, I will probably leave this repo as-is, archive it, and create a fresh repo when I receive my Pico2.

## Overview
Transcendence is a translation tool designed to convert Intel 8080 assembly language code into Arm M0+ assembly language, targeting platforms like the Raspberry Pi RP2040. The tool also aims to transpile PL/M language code into Arm M0+ assembly language, facilitating compatibility with older systems requiring CP/M operating systems or similar environments. Transcendence (for now) aims to bridge the gap between legacy various 8-Bit CPUs and PL/M codebases with modern Arm Cortex-M0+ platforms like the Raspberry Pi RP2040. By providing a reliable and efficient translation mechanism, it enables the preservation and utilization of vintage software while leveraging the capabilities of contemporary hardware.  

## Specification
Current specification is located here -> [Handling Differences a Specification](/specification/Handling_Differences_Specification.md)
- Note: The specification and playground code are NOT 1 to 1.
   - The `/python/playground/` drives the development of a better specification.
   - The `/python/spec/` directory contains a "working" specification example.

- [handling_differences.py](/python/spec/handling_differences.py)
   - This is now the same as [Handling Differences Specification](/specification/Handling_Differences_Specification.md).
   - Going forward, I will make an effort to follow this. The current playground doesn't follow this.

## Playground
You will find Intel 8080 assembly and PL/M regex patterns with subsequent pattern matching in the playground folder.  
This is where I try out ideas/work on designing the specification and Transcendence.
#### Playground History
- CP/M 2.2 in PL/M is completely pattern matched and PL/M has a complete set of regexes.
   - Looking for more PL/M code to test.
- Intel 8080 assembly has a complete set of regexes.
   - Looking for more I8080 assembly to test.
- I've added the files that guided me to create the [Handling Differences Specification](/specification/Handling_Differences_Specification.md).
   - [I8080_M0Plus_Mappings.py](/python/playground/maps/I8080_M0Plus_Mappings.py)
   - [Translate_I8080_to_M0Plus.py](/python/playground/Translate_I8080_to_M0Plus.py)
      - 🐲🐉 These are not great or even good. These are what drove me to create a specification. 🐉🐲
- Added SLY lexer and parser for I8080
   - [SLY_I8080.py](/python/playground/SLY_I8080.py)
      - Technically supports 8080 and 8085. 8085 is untested.
         - 8086 is also possible with a few additions and changes.
      - Allows for highly simplistic Abstract Syntax Tree construction.
      - 🍖🍴 Massive SLY refactor. Dragons cooked. 🍴🍖
         - :godmode: Slain the lexing and parsing dragons. :godmode:
         - :hurtrealbad: Added inital pass for macros and directives. :hurtrealbad:
         - Deprecated.
      - Rebuilt the SLY lexer and Parser in PLY
         - All future updates will happen in PLY, not SLY. 
      - 8080_fp16.ASM lexes and parses in it's entirety.
         - 8080_fp16.ASM is a 8080 assembly implmentation of floating point math by Vitaly Lunyov.
         - 🎆🎆🎆Now I can focus on translating the AST into ARMv6-M ISA. 🎆🎆🎆
            - I might work on 8085/8086 for a bit before I move on to translation.
               - Nah, I will try and fully translate I8080 to ARM THUMB before this, as the changes shouldn't be that major for 8085/8086.
      - Updated PLY lexer and parser to a decent status.
         - [PLY_I8080_NonBacktracking.py](/python/playground/PLY_I8080_NonBacktracking.py)
      - Created a baseline translation layer.
         - [PostProcessing_AST_Traversal_Translator.py](/python/playground/PostProcessing_AST_Traversal_Translator.py)

- M0+ Floating Point Math - m0plus_fp16_fp32.asm
   - Never been assembled, pure theoretical garbage.
   - See fp1632.s in pico/pico-asm-main/source/floatingpoint for a "real" implementation.

- M0+ OS - arm_os.asm
   - Initial theory file. Never been assembled, pure theoretical garbage.

- PLY Backtracking & Non-Backtracking
   - Started to develop a backtracking parser for AST generation. Leaving in repo for historical sake.
   - Terrible very very terrible garbage.
   - Just use a post-processing pass after the non-backtracking parser.

- VSCode Pico ASM PRJ + fp1632.s
   - CMake C/ASM/Cxx VSCode example project from https://blog.smittytone.net aka Tony Smith.
   - Contains fp1632.s in pico/pico-asm-main/source/floatingpoint
   - fp1632.s Has been assembled with the arm-de1soc simulator on https://cpulator.01xz.net/
   - No it has not been tested or assembled with a real assembler.

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

## Target Platform
Transcendence primarily targets the Raspberry Pi RP2040, which features the Arm Cortex-M0+ processor. The tool is optimized for the little-endian architecture of the RP2040, ensuring compatibility with its execution environment.

## Contribution
Contributions to Transcendence are welcome and encouraged. Interested developers can clone the project repository. Contribute enhancements. Fix Bugs. Add additional translation capabilities. Collaboration and feedback are essential for improving the tool.
