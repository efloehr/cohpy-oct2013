#!/usr/bin/env python
#coding:utf-8

# Introduce PIL, show properties (mode) and methods (like histogram, show) on Image object

from PIL import Image


def get_histogram(image):
    # Histogram will only work on RGB type
    if image.mode <> "RGB":
        raise Exception("Not RGB mode")

    hg = image.histogram()
    # Returns a 768 member array with counts of R, G, B values
    rhg = hg[0:256]
    ghg = hg[256:512]
    bhg = hg[512:]
    return rhg, ghg, bhg


if __name__ == '__main__':
    # Open the image
    skyimg = Image.open("2013-10-01-16-17-12.jpg")
    
    # Need ImageMagick to view
    skyimg.show()
    
    get_histogram(skyimg)
