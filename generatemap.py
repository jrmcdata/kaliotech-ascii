#!/usr/bin/python3
'''
############################
# Libraries
############################
'''
from PIL import Image
import string
import sys

'''
############################
# Load attributes
############################
'''

mainImage = Image.open('out.png')
widthKey  = 24
heightKey = 48

#mainImage = Image.open(sys.argv[1])

'''
############################
# Load image
############################
'''

dataImage = mainImage.load()
sizeImage = mainImage.size

'''
############################
# Character generation
############################
'''

# GENERATING CHARACTER LIST
char1 = '!@#$%^&*()'
char2 = '`-=[]\\;\',./~_+{}|:"<>?'
fullDictionary = string.ascii_uppercase + string.ascii_lowercase + string.digits[1:] + string.digits[0] + char1 + char2

# GENERATING POSITIONS FOR THE CHARACTERS
upperPOS = [ [  1 + 2*nn,  4] for nn in range(0, len(string.ascii_uppercase) ) ]
lowerPOS = [ [  1 + 2*nn, 12] for nn in range(0, len(string.ascii_lowercase) ) ]
digitPOS = [ [  1 + 2*nn, 20] for nn in range(0, len(string.digits) )          ]
char1POS = [ [ 21 + 2*nn, 20] for nn in range(0, len(char1) )                  ]
char2POS = [ [  1 + 2*nn, 28] for nn in range(0, len(char2) )                  ]
# List of character positions
letterPOS = upperPOS + lowerPOS + digitPOS + char1POS + char2POS

# EXTRACTING PIXEL REGIONS FOR EACH CHARACTER
lumaR = 0.2126
lumaG = 0.7152
lumaB = 0.0722

letterREG = [ [ xx // widthKey, yy // widthKey, dataImage[xx,yy][0]*lumaR + dataImage[xx,yy][1]*lumaG + dataImage[xx,yy][2]*lumaB ] \
for yy in range(0,sizeImage[1]) for xx in range(0,sizeImage[0]) \
if ( [ xx // widthKey, yy // widthKey] in letterPOS ) or ([ xx // widthKey, yy // widthKey - 1] in letterPOS ) ]

# ASIGNING VALUES TO UPPER AND LOWER PARTS OF LETTER BY SQUARE AVERAGE
# Luminosity weight, higher overweights darks, 2 by default
lWGT = 0.85
letterVAL = [ \
[ ( sum( map( lambda ii: ii**lWGT,  [ xx[2] for xx in letterREG if xx[0] == yy[0] and xx[1] == yy[1] + 0] ) )/widthKey**2. )**(1/lWGT), \
  ( sum( map( lambda ii: ii**lWGT,  [ xx[2] for xx in letterREG if xx[0] == yy[0] and xx[1] == yy[1] + 1] ) )/widthKey**2. )**(1/lWGT) ] \
for yy in letterPOS ]

# RESCALING LUMINOSITY (BY SQUARE) TO (0,255) FOR LOW INTENSITY REGIONS
minColor = max( min( [ min(xx) for xx in letterVAL ] ), 0   )
maxColor = min( max( [ max(xx) for xx in letterVAL ] ), 255 )

# LETTER WEIGHTS
letterWGT = [ tt for tt in zip( fullDictionary, \
list(map( lambda ii: ( (255**lWGT-0)/(maxColor**lWGT-minColor**lWGT)*(ii**lWGT-minColor**lWGT)+0 )**(1/lWGT), [ xx[0] for xx in letterVAL ] )),    \
list(map( lambda ii: ( (255**lWGT-0)/(maxColor**lWGT-minColor**lWGT)*(ii**lWGT-minColor**lWGT)+0 )**(1/lWGT), [ xx[1] for xx in letterVAL ] )) ) ] \
+ [ (' ', 255, 255) ]

# BEST LETTER FOR EACH COLOR
letterBST = [ \
min([ [xx[0], ( (a0**lWGT-xx[1]**lWGT)**2 + (a1**lWGT-xx[2]**lWGT)**2 )**(1/(2*lWGT))] for xx in letterWGT], key = lambda tt: tt[1])[0] \
for a0 in range(0,256) for a1 in range(0,256) ]

# OUTPUT
with open('letterMap.txt', 'w') as fileOut:
	for xx in range(0,256):
		for yy in range(0,256):
			fileOut.write( letterBST[ xx*256 + yy ] )
			
		
		fileOut.write( '\n' )
	
