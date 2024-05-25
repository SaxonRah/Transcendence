# CP/M - BIOS - BDOS

### Information Site
- https://www.seasip.info/Cpm/index.html
## Overview Directory
- [cpm_bios_bdos.md](/pico/pico_bdos_gdos/info/cpm_bios_bdos.md)
  - Overview of CP/M 2.2, BDOS, BIOS
- [gsx_gios_gdos.md](/pico/pico_bdos_gdos/info/gsx_gios_gdos.md)
  - Overview of GSX, GIOS, GDOS

## Technical Directory
- [bdos_function_summary.md](/pico/pico_bdos_gdos/info/bdos_function_summary.md)
  - Summary of bdos functions for CP/M 2.2, CP/M 3.0, MP/M 2.1 
- [bdos_system_calls.md](/pico/pico_bdos_gdos/info/bdos_system_calls.md)
  - CP/M 1, 2 and 3, with partial MP/M and DOSPLUS system calls.
- [cpm_bios.md](/pico/pico_bdos_gdos/info/cpm_bios.md)
  - BIOS is the machine-dependent part of CP/M.
- [disk_formats.md](/pico/pico_bdos_gdos/info/disk_formats.md)
  - CP/M 2.2 disc formats
- [cpm_gsx.md](/pico/pico_bdos_gdos/info/cpm_gsx.md)
  - GSX is a graphics library, for CP/M and CP/M-86, designed to be portable.

# Technical overview of CP/M 2.2:
CP/M (Control Program for Microcomputers) 2.2, developed by Digital Research, Inc., is an early operating system that played a significant role in the microcomputer revolution of the 1970s and early 1980s.
#### CP/M 2.2 is composed of three main parts:
- BIOS (Basic Input/Output System)
- BDOS (Basic Disk Operating System)
- CCP (Console Command Processor)

## BIOS (Basic Input/Output System)
The BIOS is hardware-specific and provides the interface between CP/M and the hardware.
#### Its primary functions include:
- Initialization: Setting up hardware and preparing the system to run CP/M.
- I/O Operations: Handling low-level input/output operations, such as reading from and writing to disk drives, and managing serial ports.
- System Time: Providing a system clock (if supported by hardware).
- Functions in the BIOS are typically written in assembly language for the specific hardware.
#### Common BIOS functions include:
- Boot: Initializes the system and loads the CCP and BDOS from disk.
- Warm Boot: Resets the system without reloading the BIOS.
- Console Input/Output: Functions to read or write a character to and from the console.
- Disk Read/Write: Functions to read a sector from disk or write a sector to disk.

## BDOS (Basic Disk Operating System)
The BDOS provides higher-level disk and file management functions and is hardware-independent. BDOS functions are called through a software interrupt (typically INT 0xE5).
#### Key responsibilities include:
- File Management: Create, delete, read, write, open, close files.
- Directory Management: Manage file directories and perform searches.
- I/O Management: Redirect I/O between different devices and files.
- Error Handling: Provide error codes and handle error conditions.
#### Common BDOS functions include:
- Open File: Opens a file for reading or writing.
- Close File: Closes an open file.
- Search for First/Next: Find files matching a given pattern.
- Read Sequential: Read data from an open file sequentially.
- Write Sequential: Write data to an open file sequentially.

## CCP (Console Command Processor)
The CCP is the user interface for CP/M, responsible for interpreting and executing commands typed by the user.
#### It handles:
- Command Execution: Executes built-in commands (e.g., DIR, ERA, REN) and external programs.
- Command Parsing: Interprets user commands and passes them to the appropriate handler.

# Disk Formats
CP/M supports a variety of disk formats, which are largely dependent on the hardware and the BIOS implementation.
#### Disk formats define:
- Sector Size: Commonly 128 bytes per sector.
- Track and Sector Organization: How sectors are organized on a disk track.
- Directory Structure: Typically uses a flat directory structure, where all files are listed in a single directory per disk.
#### Disk formats may vary, but CP/M 2.2 commonly used:
- Single-sided, single-density: 77 tracks, 26 sectors per track, 128 bytes per sector.
- Double-sided, double-density: Variations exist depending on the hardware.
