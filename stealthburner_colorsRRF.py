#!python
# 
# This script changes the color of the Voron Stealthburner logo LED to the color of
# the Feature Type (which is classified by the slicer) that is currently being printed.
# 
# This postprocess script, especially the idea of adding gcode by the TYPE string,
# was inspired by RomRider's https://github.com/RomRider/klipper-FastGyroidInfill
#
# This script is for RRF printers.
# In order to make this work, you first need Stealthburner, which (of course) has
# built-in LEDs. LEDs must be configured in one M150-controllable string.
#
# written by Sadao Ikebe 2022
# 
# #!python
import sys
import re
import os
import time


def setcolor(of, red, green, blue):
    of.write('M150 X2 R255 U255 B255 P255 S57 F1\n') # mini12864
    of.write('M150 X2 R'+str(red)+' U'+str(green)+' B'+str(blue)+' P255 S3 F0\n') # stealthburner


sourceFile=sys.argv[1]

# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()

if (sourceFile.endswith('.gcode')):
    destFile = re.sub('\.gcode$','',sourceFile)
    try:
        os.rename(sourceFile, destFile+".led.bak")
    except FileExistsError:
        os.remove(destFile+".led.bak")
        os.rename(sourceFile, destFile+".led.bak")
    destFile = re.sub('\.gcode$','',sourceFile)
    destFile = destFile + '.gcode'
else:
    destFile = sourceFile
    os.remove(sourceFile)

with open(destFile, "w") as of:
    for lIndex in range(len(lines)):
        oline = lines[lIndex]
        of.write(oline)
        # print(oline)
        # Parse gcode line
        if oline.startswith(';TYPE:Internal perimeter'):
            setcolor(of,255,255,0)
        if oline.startswith(';TYPE:External perimeter'):
            setcolor(of,230,150,0)
        if oline.startswith(';TYPE:Overhang perimeter'):
            setcolor(of,0,0,255)
        elif oline.startswith(';TYPE:Internal infill'):
            setcolor(of,150,0,0)
        elif oline.startswith(';TYPE:Solid infill'):
            setcolor(of,255,0,180)
        elif oline.startswith(';TYPE:Top solid infill'):
            setcolor(of,240,0,60)
        elif oline.startswith(';TYPE:Bridge infill'):
            setcolor(of,80,120,255)
        elif oline.startswith(';TYPE:Internal bridge infill'):
            setcolor(of,160,170,220)
        elif oline.startswith(';TYPE:Support material'):
            setcolor(of,0,255,0)
        elif oline.startswith(';TYPE:Gap fill'):
            setcolor(of,255,255,255)
        elif oline.startswith(';TYPE:Skirt'):
            setcolor(of,120,90,0)
of.close()
f.close()
