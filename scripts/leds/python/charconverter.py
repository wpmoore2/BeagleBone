# !/usr/bin/python


from PIL import Image, ImageDraw, ImageFont
import numpy as np

fonts = ['fonts/Dotrice-Bold-Expanded.otf',
         'fonts/FreeMono.ttf',
         'fonts/verdanab.ttf',
         'fonts/visitor1.ttf']


def char_to_pixels(text, path=fonts[0], fontsize=14):
    """
    Based on https://stackoverflow.com/a/27753869/190597 (jsheperd)
    """
    font = ImageFont.truetype(path, fontsize)
    w, h = font.getsize(text)
    h = 4
    image = Image.new('L', (w, h), 1)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    arr = arr[(arr != 0).any(axis=1)]
    return arr

def display(arr):
    result = np.where(arr, '1', '0')
    print('\n'.join([''.join(row) for row in result]))
    print ('\n\n')
    result = np.where(arr, '#', ' ')
    print('\n'.join([''.join(row) for row in result]))


import sys

arr = char_to_pixels(sys.argv[1], fontsize=6)

print (arr.shape)
print ("------------------")
display(arr)
