
# CP/M 2.2 disc formats
- https://www.seasip.info/Cpm/formats.html  

The disc format used is to some extent implementation dependent. CP/M has no standard system (like the DOS boot record) to store disc parameters on the disc. Some individual systems use their own boot records (eg Amstrad PCW) but in general the only way to determine a format is to use a program like DISKSTAT on the computer which generated the discs. The sectors of some discs may be software skewed - again, the best way to determine this is to examine the translation table on the source computer.

The layout of a disc is:

- Zero or more reserved tracks;
- One or more data blocks, a multiple of 1k in size.
  - The data blocks can span tracks and usually contain multiple sectors.
- Any spare sectors - ignored by CP/M.
- There is one directory (with a fixed size),
  - which occupies one or more blocks at the start of the file space. 
  - The directory contains 32-byte entries.

CP/M 2.2 works with a much larger range of discs than CP/M 1.4.  
The disc statistics are stored in a parameter block (the DPB), which contains the following information:

	DEFW	spt	;Number of 128-byte records per track
	DEFB	bsh	;Block shift. 3 => 1k, 4 => 2k, 5 => 4k....
	DEFB	blm	;Block mask. 7 => 1k, 0Fh => 2k, 1Fh => 4k...
	DEFB	exm	;Extent mask, see later
	DEFW	dsm	;(no. of blocks on the disc)-1
	DEFW	drm	;(no. of directory entries)-1
	DEFB	al0	;Directory allocation bitmap, first byte
	DEFB	al1	;Directory allocation bitmap, second byte
	DEFW	cks	;Checksum vector size, 0 for a fixed disc
			;No. directory entries/4, rounded up.
	DEFW	off	;Offset, number of reserved tracks

The directory allocation bitmap is interpreted as:

               al0                 al1
        b7b6b5b4b3b2b1b0    b7b6b5b4b3b2b1b0
         1 1 1 1 0 0 0 0     0 0 0 0 0 0 0 0

 - ie, in this example, the first 4 blocks of the disc contain the directory.

The DPB is not stored on disc. It is either hardwired into the BIOS or generated on the fly when a disc is logged in.
The reserved tracks will contain an image of CP/M 2.2, used when the system is rebooted. Discs can be formatted as data only discs, in which case they have no system tracks and cannot be used to reboot the system.

CP/M 2.2 directory
The CP/M 2.2 directory has only one type of entry:

    UU F1 F2 F3 F4 F5 F6 F7 F8 T1 T2 T3 EX S1 S2 RC   .FILENAMETYP....
    AL AL AL AL AL AL AL AL AL AL AL AL AL AL AL AL   ................

- UU = User number. 0-15 (on some systems, 0-31).
     - The user number allows multiple files of the same name to coexist on the disc. 
     - User number = 0E5h => File deleted
- Fn - filename
- Tn - filetype. The characters used for these are 7-bit ASCII.  
     - The top bit of T1 (often referred to as T1') is set if the file is 
     read-only.  
     - T2' is set if the file is a system file (this corresponds to "hidden" on 
     other systems). 
- EX = Extent counter, low byte - takes values from 0-31
- S2 = Extent counter, high byte.

      An extent is the portion of a file controlled by one directory entry.
      If a file takes up more blocks than can be listed in one directory entry,
      it is given multiple entries, distinguished by their EX and S2 bytes. The
      formula is: Entry number = ((32*S2)+EX) / (exm+1) where exm is the 
      extent mask value from the Disc Parameter Block.

- S1 - reserved, set to 0.
- RC - Number of records (1 record=128 bytes) used in this extent, low byte.
     - The total number of records used in this extent is (EX & exm) * 128 + RC
     - If RC is >=80h, this extent is full and there may be another one on the disc.
     - File lengths are only saved to the nearest 128 bytes.

- AL - Allocation. Each AL is the number of a block on the disc. 
    - If an AL number is zero, that section of the file has no storage allocated to it 
      - (ie it does not exist). For example, a 3k file might have allocation 
        - 5,6,8,0,0.... - the first 1k is in block 5, the second in block 6, the third in block 8.
    - AL numbers can either be 8-bit (if there are fewer than 256 blocks on the disc) or 16-bit (stored low byte first). 

Date stamps
Some compatible 3rd-party BDOSes (such as Z80DOS and DOS+) implement date stamping.  
Unfortunately the date stamp format they use is different from that used by CP/M 3.

Every fourth entry of a date-stamped directory will contain stamps for the preceding three entries:

    21 00 C1 C1 M1 M1 M1 M1 A1 A1 A1 A1 C2 C2 M2 M2    !...............
    M2 M2 A2 A2 A2 A2 C3 C3 M3 M3 M3 M3 A3 A3 A3 A3    ................
    
    C1 = File 1 Create date
    M1 = File 1 Modify date/time
    A1 = File 1 Access date/time
    C2 = File 2 Create date
    M2 = File 2 Modify date/time
    A2 = File 2 Access date/time
    C3 = File 3 Create date
    M3 = File 3 Modify date/time
    A3 = File 3 Access date/time

The format of a date/time entry is:

        DW      day     ;Julian day number, stored low byte first.
                        ;Day 1 = 1 Jan 1978.
        DB      hour    ;BCD hour, eg 13h => 13:xx
        DB      min     ;BCD minute
