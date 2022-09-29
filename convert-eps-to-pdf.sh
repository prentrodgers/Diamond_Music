#!/bin/bash
# csound creates a text output with graphical waveforms as an .EPS file, which is not searchable like a .PDF file. This does a batch conversion.
#Batch convert .EPS and .AI files into .PDF format

#EPS to PDF batch convert
#make sure you downloaded eps-to-pdf
#To install type 'sudo apt-get install texlive-font-utils' in terminal
for file in *.eps; do epstopdf --hires "$file"; done
