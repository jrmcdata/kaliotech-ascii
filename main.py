#!/usr/bin/python3
'''
############################
# Libraries
############################
'''
from PIL import Image
import string
import math
import sys
import getopt
'''
############################
# Load attributes
############################
inFile    = 'chicken.jpg'
noLines   = 100
inLetters = 'letterMap.txt'
outFile   = 'pp.txt'
'''

# INITIAL ARGUMENTS
iniArguments = dict(getopt.getopt( sys.argv[1:], 'i:l:s:o:')[0])

# PARSE VALUES
# Intro file
try:
	inFile = iniArguments['-i']
except:
	print("ERROR: no initial image declared -i")
	exit()

# Source of character data
try:
	inLetters = iniArguments['-s']
except:
	print("ERROR: no source data -s")
	exit()

# Number of lines
try:
	outFile = iniArguments['-o']
except:
	outFile = inFile.split('.')[0] + '.txt'

# Number of lines
try:
	noLines = int(iniArguments['-l'])
	customLines = True
except:
	customLines = False

'''
############################
# Load image
############################
'''

# LOAD IMAGE
mainImage = Image.open( inFile )
sizeImage = mainImage.size

if customLines == False:
	noLines = min( 75, math.floor(sizeImage[1]/2) )

if 2 * noLines != sizeImage[1]:
	newSize = ( math.floor(sizeImage[0]*2*noLines/sizeImage[1]), 2 * noLines )
	mainImage = mainImage.resize( newSize )

dataImage = mainImage.load()
sizeImage = mainImage.size

'''
############################
# Load letter data
############################
'''

# LOAD DATA FROM FILE
with open( inLetters ) as inFile:
	letterData = inFile.read()

letterData = [ letterData[ 0 + 257*nn: 256 + 257*nn ] for nn in range(0,256) ]

'''
############################
# Image
############################
'''
# Luma variables
lumaR = 0.2126
lumaG = 0.7152
lumaB = 0.0722

letterImage = [ "".join([ \
letterData[ int( dataImage[nn,2*kk][0] * lumaR   + dataImage[nn,2*kk][1] * lumaG   + dataImage[nn,2*kk][2] * lumaB   ) ] \
		  [ int( dataImage[nn,2*kk+1][0] * lumaR + dataImage[nn,2*kk+1][1] * lumaG + dataImage[nn,2*kk+1][2] * lumaB ) ] \
for nn in range(0,sizeImage[0]) ]) for kk in range(0, noLines) ]

'''
############################
# Output
############################
'''

ff = open( outFile,'w')
for xx in letterImage:
	ff.write(xx + '\n')

ff.close()
