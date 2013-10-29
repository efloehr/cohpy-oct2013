#!/usr/bin/env python
#coding:utf-8

# Introduce ImageOps image operations, like invert
# Also introduce another Image method, split, that takes the
# R,G, and B components of an image and creates separate
# grayscale images with just that component

from PIL import Image, ImageOps


def is_RGB(image):
    return image.mode == "RGB"

def get_histogram(image):
    # Histogram will only work on RGB type
    if not is_RGB(image):
        raise Exception("Not RGB mode")

    hg = image.histogram()
    # Returns a 768 member array with counts of R, G, B values
    rhg = hg[0:256]
    ghg = hg[256:512]
    bhg = hg[512:]
    return rhg, ghg, bhg


def get_RGB_split_inverted(image):
    if not is_RGB(image):
        raise Exception("Not RGB mode")

    image_r, image_g, image_b = image.split()
    image_rn = ImageOps.invert(image_r)
    image_gn = ImageOps.invert(image_g)
    image_bn = ImageOps.invert(image_b)

    return image_rn, image_gn, image_bn

    
if __name__ == '__main__':
    # Open the image
    skyimg = Image.open("2013-10-01-16-17-12.jpg")
    
    skyimg_r, skyimg_g, skyimg_b = get_RGB_split_inverted(skyimg)
    
    skyimg_r.show()
    skyimg_g.show()
    skyimg_b.show()
    
