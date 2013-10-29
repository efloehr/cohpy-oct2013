#!/usr/bin/env python
#coding:utf-8

from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import itertools
import cStringIO

# Add the histogram graphs to the combined image

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


def get_histogram_graph_image(image):
    rhg, ghg, bhg = get_histogram(image)
    
    # Get x values
    xpoints = range(len(bhg))
    ymax = max(itertools.chain(rhg, ghg, bhg))

    plt.figure(1, figsize=[3,9], frameon=False)
    
    plt.subplot(311)
    plt.plot(xpoints, rhg, 'k', linewidth=2)
    plt.plot(xpoints, ghg, 'g', linewidth=2)
    plt.plot(xpoints, bhg, 'b', linewidth=2)
    plt.fill_between(xpoints, rhg, color='r')
    plt.axis([0, 255, 0, int(ymax*1.05)])
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['left'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    
    plt.subplot(312)
    plt.plot(xpoints, rhg, 'r', linewidth=2)
    plt.plot(xpoints, ghg, 'k', linewidth=2)
    plt.plot(xpoints, bhg, 'b', linewidth=2)
    plt.fill_between(xpoints, ghg, color='g')
    plt.axis([0, 255, 0, int(ymax*1.05)])
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['left'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    
    plt.subplot(313)
    plt.plot(xpoints, rhg, 'r', linewidth=2)
    plt.plot(xpoints, ghg, 'g', linewidth=2)
    plt.plot(xpoints, bhg, 'k', linewidth=2)
    plt.fill_between(xpoints, bhg, color='b')
    plt.axis([0, 255, 0, ymax])
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['left'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    
    plt.tight_layout()
    
    ram = cStringIO.StringIO()
    plt.savefig(ram, format='png', dpi=120)
    plt.close()
    
    ram.seek(0)
    return Image.open(ram)


def compose_histogram(image):
    # Will create a 1080p picture composed of 4:3 original and R, G, B breakouts inverted
    if not is_RGB(image):
        raise Exception("Not RGB mode")

    # Create a new image of 1080p size
    combimg = Image.new("RGB", (1920, 1080))
    
    # Resize the main image and paste into right size
    combimg.paste(image.resize((1080, 810)), (840, 0))
    
    # Get the rgb components, resize to 480x360 and stack on mid-left
    skyimg_r, skyimg_g, skyimg_b = get_RGB_split_inverted(image)
    combimg.paste(skyimg_r.resize((480, 360)), (360, 0))
    combimg.paste(skyimg_g.resize((480, 360)), (360, 360))
    combimg.paste(skyimg_b.resize((480, 360)), (360, 720))
       
    # Get the histogram and put on far left
    histimg = get_histogram_graph_image(image)
    combimg.paste(histimg.resize((360,1080)), (0,0))
    
    return combimg

    
if __name__ == '__main__':
    # Open the image
    skyimg = Image.open("2013-10-01-16-17-12.jpg")

    histimg = compose_histogram(skyimg)
    
    histimg.show()
