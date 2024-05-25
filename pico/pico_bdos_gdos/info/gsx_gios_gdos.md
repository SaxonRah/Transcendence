# GSX - GIOS - GDOS

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

# Technical overview of GSX (Graphics System Extension):
CP/M 2.2 itself does not include built-in graphics capabilities, as it was designed primarily for text-based applications and command-line interaction. However, graphics could be implemented through third-party software or hardware extensions. Graphics capabilities were highly dependent on the specific hardware being used, and any graphics operations would typically bypass the standard CP/M BIOS and directly manipulate the hardware.  

GSX was an add-on developed by Digital Research to provide graphics capabilities to CP/M and other operating systems. It served as a portable graphics library and API that allowed programs to include graphical output regardless of the underlying hardware.  

One of the key features of GSX is device independence. Applications written to use GSX can run on any hardware platform that has a GIOS driver for its graphics hardware. This significantly reduces the effort required to port graphics applications between different systems.
#### Main components of GSX:
- GIOS (Graphics Input/Output System): This is the hardware-dependent part of GSX, analogous to the BIOS in CP/M, that provides the low-level interface to the graphics hardware.
- GDOS (Graphics Device Operating System): This is the hardware-independent part that provides the graphics API to applications, analogous to the BDOS in CP/M.

## GIOS (Graphics Input/Output System)
GIOS provides the low-level drivers that interface directly with the graphics hardware. The GIOS drivers translate GDOS calls into hardware-specific instructions, allowing the same GDOS code to work across different systems.
#### These drivers are specific to each type of graphics device and handle:
- Device Initialization: Setting up the graphics hardware and putting it into a known state.
- Primitive Rendering: Implementing the basic drawing functions using hardware capabilities.
- I/O Management: Handling input devices such as mice or graphics tablets, if supported.

## GDOS (Graphics Device Operating System)
GDOS is the core of GSX, providing a set of high-level graphics functions that applications can use to perform graphical operations. 
GDOS functions are accessed through a set of standardized calls, similar to how BDOS functions are accessed in CP/M.
#### These include:
- Drawing Primitives: Functions to draw lines, rectangles, circles, ellipses, and polygons.
- Text Output: Functions to draw text in various fonts and sizes.
- Fill Patterns: Functions to fill areas with patterns or colors.
- Clipping: Functions to define and manage clipping regions.
- Image Handling: Functions to manipulate bitmapped images.

## GSX API and Programming Model
The GSX API provides a rich set of graphics functions. These functions are typically called with parameters specifying the graphics context, coordinates, and attributes like color and line style.
#### Some key functions include:
- v_opnwk: Open a graphics workstation.
- v_clswk: Close a graphics workstation.
- v_clrwk: Clear the workstation (screen).
- v_pline: Draw a polyline.
- v_pmarker: Draw markers at specified points.
- v_gtext: Draw text at a specified location.
- v_fillarea: Fill an area with a specified pattern.
- v_bar: Draw a filled rectangle (bar).

## Usage and Applications
GSX was used in a variety of applications. 
#### Some applications include:
- Business Graphics: Creating charts and graphs for business reports.
- CAD: Basic computer-aided design programs.
- Desktop Publishing: Early efforts at combining text and graphics in printed documents.
- Games: Simple graphical games that required platform-independent graphics.

## Graphics Hardware Support
The range of supported graphics hardware for GSX depended on the availability of GIOS drivers.
#### Commonly supported devices included:
- VDUs (Visual Display Units): Various monochrome and color display terminals.
- Plotters: For high-resolution vector graphics output.
- Graphics Tablets: For input devices in CAD and design applications.

## GSX Disk Formats
GSX itself does not define a specific disk format, as it is a set of graphics extensions for CP/M. However, it relies on CP/M’s file system for storing and retrieving graphics data. The typical CP/M disk format, as described earlier, is used to store GSX-related files, including drivers, fonts, and graphics data.
