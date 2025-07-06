import os
import argparse
from ascii_art import AsciiArt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a batch of images into a batch of ascii-art images in ASCII art form')
    parser.add_argument('--indir', type=str, help='directory of images', required=True)
    parser.add_argument('--outdir', type=str, default='ascii_arts', help='output directory')
    args = parser.parse_args()

    art = AsciiArt(scale_ratio_width = 1.8, max_width=240, ascii_chars=" %#*+=-:,.&$!^abcdfghjpqrstuvwxwzmn")
    art.image_to_ascii_batch(args.indir, args.outdir)
    art.ascii_art_to_image_batch(args.outdir, args.outdir + '_png')
