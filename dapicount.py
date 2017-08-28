__author__ = 'wendy'

from PIL import Image
from enum import Enum
from os import listdir
from os.path import isfile, join

# White Threshold
# Note: White pixels represent stained nuclei
LOW_WHITE = (15, 15, 15)

# Black threshold
# Note: Black pixels represent empty space
HIGH_BLACK = (14, 14, 14)

# number of microns per pixel
class PixelSizeConversion(Enum):
    TEN_X = 0.641      # 10x = 0.641um/px
    TWENTY_X = 0.322   # 20x = 0.322um/px
    FORTY_X = 0.161    # 40x = 0.161um/px

# Counting anything that's "not black" ala Borat

# definition from hellonello.py
def is_white(pixel):
    if pixel[0] >= LOW_WHITE[0] and \
        pixel[1] >= LOW_WHITE[1] and \
            pixel[2] >= LOW_WHITE[2]:
        return True
    return False

def is_black(pixel):
    if pixel[0] <= HIGH_BLACK[0] and \
        pixel[1] <= HIGH_BLACK[1] and \
            pixel[2] <= HIGH_BLACK[2]:
        return True
    return False

# this refers to the folder
# noinspection PyByteLiteral
image_directory = 'C:\Users\wendy_000\Desktop\p75\NORM\dapi'

# describing the pictures as a list
images = [f for f in listdir(image_directory) if isfile(join(image_directory, f))]

# within the list 'images', open each file 'i' in order and iterate over it
# load one file at a time, define width and height from metadata
for i in xrange(len(images)):
    current_file = Image.open('{0}\{1}'.format(image_directory, images[i]))
    im_pixels = current_file.load()
    width, height = current_file.size

    # starting counts for all pixels
    count_white = 0
    count_black = 0

    # for each x value, than each y value, define if pixel is red, green, or black
    # add 1 to each color count if there are any red, green, or black pixel
    for x in xrange(width):
        for y in xrange(height):
            pixel = im_pixels[x, y]
            # Make sure to only count each pixel once
            if is_white(pixel):
                count_white += 1
            elif is_black(pixel):
                count_black += 1

    # subtract black space from total picture size to determine tissue area
    total_tissue_pixels = width * height - count_black

    print 'File Name: {0}'.format(images[i])
    # Use float for non integers, can hold many values after .
    print 'Total white pixels: {0}, Total white area(um^2): {1}, Total white percent: {2}'.format(count_white, count_white * PixelSizeConversion.TWENTY_X.value, (float)(count_white) / (float)(total_tissue_pixels))
    print 'Total tissue pixels: {0}, Total tissue area(um^2): {1}'.format(total_tissue_pixels, total_tissue_pixels *
                                                                            PixelSizeConversion.TWENTY_X.value)
    print 'Image Dimensions: {0}x{1}, Total pixels: {2}'.format(width, height, width * height)
    print 'black space: {0}'.format(count_black)

