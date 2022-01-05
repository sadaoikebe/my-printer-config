#!python
# This script changes the color of the Voron Stealthburner logo LED to the color of
# the Feature Type (which is classified by the slicer) that is currently being printed.
# 
# This postprocess script, especially the idea of adding gcode by the TYPE string,
# was inspired by RomRider's https://github.com/RomRider/klipper-FastGyroidInfill
#
# In order to make this work, you first need Stealthburner, which (of course) has
# built-in LEDs. And the LEDs must be configured in printer.cfg.
# If the toolhead LEDs don't have a dedicated chain, e.g. are strung after the
# same string as the ceiling LEDs, you'll have to give it a different INDEX. 
# 
# printer.cfg example:
#
# [neopixel stealthburner]
# pin: PD3  # Fysetc Spider v2.2
# chain_count: 3
# initial_RED: 1
# initial_GREEN: 1
# initial_BLUE: 1
# color_order: GRB
#
# written by Sadao Ikebe 2022
# 
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

with open(destFile, "w") as of:
    for lIndex in range(len(lines)):
        oline = lines[lIndex]
        of.write(oline)
        # print(oline)
        # Parse gcode line
        if oline.startswith(';TYPE:Internal perimeter'):
            of.write('SET_LED LED=stealthburner INDEX=1 RED=1 GREEN=1 BLUE=0\n')
        elif oline.startswith(';TYPE:External perimeter'):
            of.write('SET_LED LED=stealthburner INDEX=1 RED=1 GREEN=0.6 BLUE=0\n')
        elif oline.startswith(';TYPE:Overhang perimeter'):
            of.write('SET_LED LED=stealthburner INDEX=1 RED=0 GREEN=0 BLUE=1\n')
        elif oline.startswith(';TYPE:Internal infill'):
            of.write('SET_LED LED=stealthburner INDEX=1 RED=0.6 GREEN=0 BLUE=0\n')
        elif oline.startswith(';TYPE:Solid infill'):
            of.write('SET_LED LED=stealthburner INDEX=1 RED=0.7 GREEN=0 BLUE=0.7\n')
        elif oline.startswith(';TYPE:Top solid infill'):
            of.write('SET_LED LED=stealthburner INDEX=1 RED=1 GREEN=0 BLUE=0\n')
        elif oline.startswith(';TYPE:Bridge infill'):
            of.write('SET_LED LED=stealthburner INDEX=1 RED=0.6 GREEN=0.6 BLUE=1\n')
        elif oline.startswith(';TYPE:Internal bridge infill'):
            of.write('SET_LED LED=stealthburner INDEX=1 RED=0.7 GREEN=0.7 BLUE=0.9\n')
        elif oline.startswith(';TYPE:Support material'):
            of.write('SET_LED LED=stealthburner INDEX=1 RED=0 GREEN=1 BLUE=0\n')
        elif oline.startswith(';TYPE:Gap fill'):
            of.write('SET_LED LED=stealthburner INDEX=1 RED=1 GREEN=1 BLUE=1\n')
        elif oline.startswith(';TYPE:Skirt'):
            of.write('SET_LED LED=stealthburner INDEX=1 RED=0.5 GREEN=0.3 BLUE=0\n')
of.close()
f.close()
