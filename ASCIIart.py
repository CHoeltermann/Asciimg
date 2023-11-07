#!/usr/bin/env python3

'''
### HELP PAGE ###

use like this:

ASCIIart.py patho-to-file-or-folder

'''

import argparse, sys, yaml, numpy
from PIL import Image

# import config file with default options
cfg_f = open("config.yaml", 'r')

# cgf will be a dic
cfg = yaml.load(cfg_f.read())
    
# set default values

out_path = cfg["output_path"]
ascii_values = cfg["ascii_values"]
scale_factor = cfg["scale_factor"]

# define classes and functions

def is_in(r, n):
    return (n>=min(r)) & (n<=max(r))

class ascii_pic():
    '''
    Here should be a docstring.
    '''
    def __init__(self, path, ascii_values=ascii_values, scale_factor=scale_factor, out_path=out_path):
        self.imagename = path
        self.path = path
        self.image = Image.open(self.path)
        # self.image has these features: format, size, mode
        # create matrix with numpy or nested lists?
        self.ascii_image = []
        self.ascii_sym = ascii_values
        self.ascii_ranges = {}
        self.scale_f = int(scale_factor)

    def scale_pic(self):
        sz = self.image.size
        self.image.resize((round(sz[0]/self.scale_f), round(sz[1]/self.scale_f)))

    def convert_to_gray(self):
        self.image = self.image.convert(mode="L")
        #self.image.convert(mode="L")

    def make_ascii_ranges(self):
        rng = round(255/len(self.ascii_sym))
        # i need a relation from bin values to ASCII sign in a list or dict
        # solution: make a dict with ascii as keys and ranges as value!
        countess = 255
        for symbol in self.ascii_sym:
            # use tuple to discern range:
            self.ascii_ranges[symbol] = (countess, countess-rng)
            countess = countess-rng

    def convert_gray_2_ascii(self):
        # invoke needed prep functions
        self.make_ascii_ranges()
        self.scale_pic()
        self.convert_to_gray()
        # make the ascii grayscale ranges needed to covert gray to the range of ascii symbols desired:
        self.make_ascii_ranges()
        # now go through the pixels by row left to right & construct a matrix with the ASCII symbols
        # for every grayscale check if within range of tuple
        for row in range(0, self.image.size[0]):
            row_str = ""
            for col in range(0, self.image.size[1]): 
                px_val = self.image.getpixel((row, col))
                # is there a better way to locate the key of the dict where the range fits?
                for key, value in self.ascii_ranges.items():
                    if is_in(value, px_val):
                        row_str = row_str + key
            self.ascii_image.append(row_str)

    def save_ascii(self):
        fns = self.imagename.split("/")[-1]
        # substitute .[fileending] with .txt:
        fns = fns.split('.')[0]
        fn = "ASCII-" + fns + ".txt"
        # write list of lists line by line to file -- "row-wise"
        for i, x in enumerate(self.ascii_image):
            with open(fn, 'a') as wf:
                # this overwrites -- but it should append!
                wf.writelines(f"{x}\n")

    def show_image(self):
        # if image.grayscales exists, show it:
        # if image.ascii_image exists, show it:
        if len(self.ascii_image) > 0:
            for i, x in enumerate(self.ascii_image):
                print(x)

# if executed on cmd line, do this:

if __name__ == "__main__":

    # fetch command line argument
    
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument("--path", help="", type=str)
    parser.add_argument("--scale_factor", help="How granular should the image be?", type=int)
    
    args = parser.parse_args()
    
    ## args is now a dictionary like this:
    # Dict format: {'bar': 'bar-val', 'foo': 'foo-val'}
    # with --bar and --foo cmd line args!
    
    # sanity check for cmd line args
    path = args.path

    if not isinstance(args.path, str):
        raise ValueError("The first argument needs to be a path!")
    
    if args.scale_factor is not None:
        scale_factor = args.scale_factor

    ### Invoke class
    current_pic = ascii_pic(args.path, ascii_values=ascii_values, scale_factor=scale_factor, out_path=out_path)
    
    ### convert image:
    current_pic.convert_gray_2_ascii()
    # check if user wants image saved:
    current_pic.save_ascii()
    # image is ALWAYS printed to console. Bc why not.
    current_pic.show_image()
    
