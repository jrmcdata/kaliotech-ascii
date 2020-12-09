kalio-ascii: an ASCII art generator (v1.00)
===========================================

Introduction
------------

kalio-ASCII generates ASCII art from any image file.

Options
-------

> -h	Prints help..

> -i	Input image file.

> -l	Number of lines for ASCII art (defaults to minimum of image height/2 or 75).
> -o	Output file for ASCII art (defaults to IMAGE_NAME.txt).
> -s	Source file for letter-map file (defaults to 'map/letter_map_default.txt').
> -v	Verbose: print status and diagnostics.

Usage
-----
./kalio-ascii.py -i file_name.jpg -l 100 -v

> Generates a text file 'file_name.txt', containing ASCII art from 'file_name.jpg'on a 100-line grid. Allow verbose output. 

To-do
-----

- [ ] Refactor map-generator script to allow for custom monospace fonts.
- [ ] Extend map-generator script for non-monospace fonts.
