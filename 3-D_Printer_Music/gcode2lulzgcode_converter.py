#!/usr/bin/env python
#gcode2lulzgcode_converter.py

import sys
line=0

print "Please enter the full name of the input raw .nc with extension at the prompt below"
#Raw_input is used to collect data from the user
inputfile = raw_input("> ")
outputfile = "lulz_"+inputfile.replace(".nc",".gcode")

#Opens the filename entered above
with open(outputfile, 'w') as open_outputfile:
    open_outputfile.write(""";Sliced at: Sun 16-08-2015 13:30:33 for use with the LulzBot TAZ 5
;Basic settings: Layer height: 0.28 Walls: 1.05 Fill: 20
G21                     ;metric values
G90                     ;absolute positioning
M82                     ;set extruder to absolute mode
M107                    ;start with the fan off
G28 X0 Y0               ;move X/Y to min endstops
G28 Z0                  ;move Z to min endstops
G1 Z15.0 F10500;move the platform down 15mm
G92 E0                  ; zero the extruded length
G1 F200 E0              ; extrude 3mm of feed stock
G92 E0                  ; zero the extruded length again
G1 F10500      ; set travel speed
M203 X192 Y208 Z3       ; speed limits
M117 Printing...        ; send message to LCD
""")
    with open(inputfile, 'r') as file:
        for i in file:
            if (i == 'G21\n'):
                line=1
                open_outputfile.write('\n'+i)  #Write the gcode from line 18 and onwards
            elif (line == 1):
                open_outputfile.write(i)  #Write the gcode from line 18 and onwards
            else:
                pass  #Write the gcode from line 18 and onwards
    open_outputfile.write("""
M400
M104 S0                        ; hotend off
M140 S0                        ; heated bed heater off (if you have it)
M107                           ; fans off
G91                            ; relative positioning
G1 E-1 F300                    ; retract the filament a bit before lifting the nozzle, to release some of the pressure
G1 Z+0.5 E-5 X-20 Y-20 F3000   ; move Z up a bit and retract filament even more
G90                            ; absolute positioning
G1 X0 Y250                     ; move to cooling position
M84                            ; steppers off
G90                            ; absolute positioning
M117 TAZ Ready.
;CURA_PROFILE_STRING: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""")
