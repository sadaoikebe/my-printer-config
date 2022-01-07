#!python
# 
# This postprocess script is an RRF version of RomRider's https://github.com/RomRider/klipper-FastGyroidInfill
# Unlike Klipper, this script just issues M566 to set jerk so it doesn't need to set up macros separately.
# It also set M593 to disable input shaper during the infill.
#
# written by Sadao Ikebe 2022
# 
#!python
import sys
import re
import os
import time

sourceFile=sys.argv[1]

# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()

if (sourceFile.endswith('.gcode')):
    destFile = re.sub('\.gcode$','',sourceFile)
    try:
        os.rename(sourceFile, destFile+".sqv.bak")
    except FileExistsError:
        os.remove(destFile+".sqv.bak")
        os.rename(sourceFile, destFile+".sqv.bak")
    destFile = re.sub('\.gcode$','',sourceFile)
    destFile = destFile + '.gcode'
else:
    destFile = sourceFile
    os.remove(sourceFile)

inInfill = False
inSupport = False

with open(destFile, "w") as of:
    for lIndex in range(len(lines)):
        oline = lines[lIndex]
        # print(oline)
        # Parse gcode line
        if oline.startswith(';TYPE:Internal infill'):
            inInfill = True
            if inSupport:
                inSupport = False
            else:
                of.write(oline)
                of.write('M566 X2200 Y1400 Z80 E8000\n')
                of.write('M593 P"none"\n')
        elif oline.startswith(';TYPE:Support material'):
            inSupport = True
            if inInfill:
                inInfill = False
            else:
                of.write(oline)
                of.write('M566 X2200 Y1400 Z80 E8000\n')
                of.write('M593 P"none"\n')
        elif (oline.startswith(';TYPE:') or oline.startswith('; INIT')) and (inInfill or inSupport):
            inInfill = False
            inSupport = False
            of.write(oline)
            of.write('M566 X600 Y300 Z80 E8000\n')
            of.write('M593 P"mzv" F33\n')
        else:
            of.write(oline)

of.close()
f.close()
