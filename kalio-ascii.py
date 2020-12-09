#!/usr/bin/python3
'''
############################
# Libraries
############################
'''
from PIL import Image
import string, math
import sys, getopt
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
try:
	iniArguments = dict(getopt.getopt( sys.argv[1:], 'i:l:s:o:vh')[0])
except:
	print('[\033[31mERROR\033[39m] Malformed expression. Use -h option for help.')
	sys.exit()

'''print(iniArguments)'''

# PARSE VALUES

# Help file
try:
	tempVar = iniArguments['-h']
	showHelp = True
except:
	#print('NO HELP')
	showHelp = False

if showHelp:
	print('Usage: kalio-ascii.py [OPTION]')
	print('Output ascii art from image to text file \n')
	print('    -h, prints this help file ')
	print('    -i, input image file')
	print('    -l, number of lines for art (defaults to minimum of image height/2 and 75)')
	print('    -o, output file for ascii art (defaults to IMAGE_NAME.txt) ')
	print('    -s, source file for letter map (defaults to \'map/letter_map_default.txt\') ')
	print('    -v, print status and diagnostics ')
	sys.exit()

# Verbose
try:
	tempVar2 = iniArguments['-v']
	doVerbose = True
except:
	doVerbose = False

# Intro file
try:
	inFile = iniArguments['-i']
except:
	print('[\033[31mERROR\033[39m] Declare input image with -i. Use -h option for help.')
	sys.exit()

# Source of character data
try:
	inLetters = iniArguments['-s']
except:
	if doVerbose:
		print('[\033[34mASCII\033[39m] Using default letter map')
	
	inLetters = 'map/letter_map_default.txt'

# Output file
try:
	outFile = iniArguments['-o']
except:
	outFile = inFile.split('.')[0] + '.txt'

# Number of lines
try:
	noLines = int(iniArguments['-l'])
	customLines = True
except:
	noLines = 0
	customLines = False


'''
print(outFile)
print(noLines)
print(inLetters)
'''
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
if doVerbose:
	print('[\033[34mASCII\033[39m] Parsing letter map')

with open( inLetters ) as tempFile:
	letterData = tempFile.read()

letterData = [ letterData[ 0 + 257*nn: 256 + 257*nn ] for nn in range(0,256) ]

'''
############################
# Image
############################
'''

if doVerbose:
	print('[\033[34mASCII\033[39m] Processing pixels in \033[96m' + str(inFile) + '\033[39m')

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

if doVerbose:
	print('[\033[95mWRITE\033[39m] Outputting to \033[96m' + str(outFile) + '\033[39m')

ff = open( outFile,'w')
for xx in letterImage:
	ff.write(xx + '\n')

ff.close()
