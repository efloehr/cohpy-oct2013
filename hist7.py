#!/usr/bin/env python
#coding:utf-8

# Go from a single image to a set of images in a directory.
# Introduce os.listdir which returns the contents of a directory,
# fnmatch.filter which will filter those contents by shell-like
# regex, and the built-in method "enumerate" which will take a
# list and return a number and an item in the list as an iterator.
#
# Also show save method of Image object to save an image to a file

from PIL import Image, ImageOps, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import itertools
import cStringIO
import os.path
import os
import fnmatch


font = ImageFont.truetype("/usr/share/fonts/levien-inconsolata/Inconsolata.ttf", 72)

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


def get_image_and_time(filepath):
    skyimg = Image.open(filepath)
    timetuple = os.path.basename(filepath).split(".")[0].split("-")
    return skyimg, timetuple

    
def compose_histogram(filepath):
    # Will create a 1080p picture composed of 4:3 original and R, G, B breakouts inverted
    image, timetuple = get_image_and_time(filepath)
    
    if not is_RGB(image):
        raise Exception("Not RGB mode")

    # Create  new image of 1080p size
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
    
    # Draw time info on image
    draw = ImageDraw.Draw(combimg)
    global font
    draw.text((880, 850), "{0}/{1}/{2} {3}:{4}:{5} UTC".format(*timetuple), font=font)
    
    return combimg


if __name__ == '__main__':
    dirpath = "timelapse/"
    resultpath = "done/"
    
    # Get list of images in directory
    files = fnmatch.filter(os.listdir(dirpath), "201[0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9].jpg")
    files.sort()
    
    count = len(files)
    
    for i, filename in enumerate(files):
        print "{0}/{1} Working on {2}".format(i,count,filename)
        histimg = compose_histogram(os.path.join(dirpath, filename))
        histimg.save(os.path.join(resultpath, '{0}.png'.format(i)))
