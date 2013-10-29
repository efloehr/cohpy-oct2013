#!/usr/bin/env python
#coding:utf-8

# Introduce creating a new image and pasting other images
# into it using Image.new() and resize and paste method
# on Image object

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

def compose_histogram(image):
    # Will create a 1080p picture composed of 4:3 original and R, G, B breakouts inverted
    if not is_RGB(image):
        raise Exception("Not RGB mode")

    # Create a new image of 1080p size
    combimg = Image.new("RGB", (1920, 1080))
    
    # Resize the main image and paste into right size
    combimg.paste(image.resize((1440, 1080)), (480, 0))
    
    # Get the rgb components, resize to 480x360 and stack on left
    skyimg_r, skyimg_g, skyimg_b = get_RGB_split_inverted(image)
    combimg.paste(skyimg_r.resize((480, 360)), (0, 0))
    combimg.paste(skyimg_g.resize((480, 360)), (0, 360))
    combimg.paste(skyimg_b.resize((480, 360)), (0, 720))
       
    return combimg

    
if __name__ == '__main__':
    # Open the image
    skyimg = Image.open("2013-10-01-16-17-12.jpg")

    histimg = compose_histogram(skyimg)
    
    histimg.show()
    
    histimg.save('hist.png')
