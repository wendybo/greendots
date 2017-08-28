__author__ = 'wendy'

from PIL import Image
from enum import Enum
from os import listdir
from os.path import isfile, join

# Red threshold
LOW_RED = (70, 13, 31)
HIGH_RED = (255, 15, 44)

# Green threshold
LOW_GREEN = (25, 70, 34)
HIGH_GREEN = (32, 255, 36)

# Blue threshold
LOW_BLUE = (38, 34, 70)
HIGH_BLUE = (35, 28, 255)

# Black threshold
# Note: Black pixels represent empty space
HIGH_BLACK = (30, 30, 30)

# number of microns per pixel
class PixelSizeConversion(Enum):
    TEN_X = 0.641      # 10x = 0.641um/px
    TWENTY_X = 0.322   # 20x = 0.322um/px
    FORTY_X = 0.161    # 40x = 0.161um/px

# Counting red pixels that fit within low and high red parameters, including low and high red values
#old definition stated (for red or green)
    # def is_red(pixel):
        # if LOW_RED[0] <= pixel[0] <= HIGH_RED[0] and \
            # LOW_RED[1] <= pixel[1] <= HIGH_RED[1] and \
                # LOW_RED[2] <= pixel[2] <= HIGH_RED[2]:
            # return True
        # return False

def is_red(pixel):
    if LOW_RED[0] <= pixel[0] <= HIGH_RED[0]:
        return True
    return False

# same as red but for green
def is_green(pixel):
    if LOW_GREEN[1] <= pixel[1] <= HIGH_GREEN[1]:
        return True
    return False

# define blue
def is_blue(pixel):
    if LOW_BLUE[2] <= pixel[2] <= HIGH_BLUE[2]:
        return True
    return False

# same as red but for black
# black is an absolute limit so you don't need a constant for it
def is_black(pixel):
    if pixel[0] <= HIGH_BLACK[0] and \
        pixel[1] <= HIGH_BLACK[1] and \
            pixel[2] <= HIGH_BLACK[2]:
        return True
    return False

# this refers to the folder, because it's within 'test1' we don't need to specify the path any more
# noinspection PyByteLiteral
image_directory = 'C:\Users\wendy_000\Desktop\p75\pK'

# describing the pictures as a list
images = [f for f in listdir(image_directory) if isfile(join(image_directory, f))]

# within the list 'images', open each file 'i' in order and iterate over it
# load one file at a time, define width and height from metadata
for i in xrange(len(images)):
    current_file = Image.open('{0}\{1}'.format(image_directory, images[i]))
    im_pixels = current_file.load()
    width, height = current_file.size

    # starting counts for all pixels
    count_red = 0
    count_green = 0
    count_blue = 0
    count_black = 0

    # for each x value, than each y value, define if pixel is red, green, or black
    # add 1 to each color count if there are any red, green, or black pixel
    for x in xrange(width):
        for y in xrange(height):
            pixel = im_pixels[x, y]
            # Make sure to only count each pixel once
            if is_red(pixel):
                count_red += 1
            if is_green(pixel):
                count_green += 1
            if is_blue(pixel):
                count_blue += 1
            elif is_black(pixel):
                count_black += 1

    # subtract black space from total picture size to determine tissue area
    total_tissue_pixels = width * height - count_black

    print 'File Name: {0}'.format(images[i])
    # Use float for non integers, can hold many values after .
    print 'Total red pixels: {0}, Total red area(um^2): {1}, Total red percent: {2}'.format(count_red, count_red * PixelSizeConversion.TWENTY_X.value, (float)(count_red) / (float)(total_tissue_pixels))
    print 'Total green pixels: {0}, Total green area(um^2): {1}, Total green percent: {2}'.format(count_green, count_green * PixelSizeConversion.TWENTY_X.value, (float)(count_green) / (float)(total_tissue_pixels))
    print 'Total blue pixels: {0}, Total blue area(um^2): {1}, Total blue percent: {2}'.format(count_blue, count_blue * PixelSizeConversion.TWENTY_X.value, (float)(count_blue) / (float)(total_tissue_pixels))
    print 'Total tissue pixels: {0}, Total tissue area(um^2): {1}'.format(total_tissue_pixels, total_tissue_pixels *
                                                                            PixelSizeConversion.TWENTY_X.value)
    print 'Image Dimensions: {0}x{1}, Total pixels: {2}'.format(width, height, width * height)
    print 'black space: {0}'.format(count_black)
