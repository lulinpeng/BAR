from PIL import Image
import math
import argparse
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

class AsciiArt:
    def __init__(self, scale_ratio_width:float=1.0, scale_ratio_height:float=1.0):
        self.ascii_chars = " %#*+=-:" # "@%#*+=-:. "
        self.ascii_art = [] # list of all ascii art strings of rows
        self.scale_ratio_width = scale_ratio_width # width scale ratio
        self.scale_ratio_height = scale_ratio_height # height scale ratio
        logging.info(f'scale_ratio_width = {self.scale_ratio_width}, scale_ratio_height = {self.scale_ratio_height}')
        self.max_width = 90 # max number of ascii characters of each row
        self.max_height = 90 # max number of ascii characters of each column
        logging.info(f'max_height = {self.max_height}, max_width = {self.max_width}')
        return

    def load_and_preprocess_image(self, img_path:str):
        img = Image.open(img_path).convert('L')
        w, h = img.size
        logging.debug(f'w * h = {w} * {h}, max_w * max_h = {self.max_width} * {self.max_height}')
        w, h = round(w * self.scale_ratio_width), round(h * self.scale_ratio_height)
        logging.debug(f'w * h = {w} * {h}, max_w * max_h = {self.max_width} * {self.max_height}')
        w, h = (self.max_width, math.floor(h * self.max_width / w)) if w > self.max_width else (w, h)
        logging.debug(f'w * h = {w} * {h}, max_w * max_h = {self.max_width} * {self.max_height}')
        w, h = (math.floor(w * self.max_height / h), self.max_height) if h > self.max_height else (w, h)
        logging.debug(f'w * h = {w} * {h}, max_w * max_h = {self.max_width} * {self.max_height}')
        img = img.resize((w,h))
        
        return img, w, h

    # map pixel to ascii character
    def pixel_to_char(self, pixel, min_pixel:int, max_pixel:int):
        n = len(self.ascii_chars) - 1
        idx = round(n * (pixel - min_pixel) / (max_pixel - min_pixel))
        return self.ascii_chars[idx]

    def image_to_ascii(self, img_path:str, outfile:str):
        img, width, height = self.load_and_preprocess_image(img_path)
        pixels = img.getdata()
        min_pixel, max_pixel  = min(pixels), max(pixels)
        logging.debug(f'min_pixel = {min_pixel}, max_pixel= {max_pixel}')
        self.ascii_art = []
        self.matrix = []
        for h in range(height):
            art_str = ''
            row = []
            for w in range(width):
                pixel = img.getpixel((w, h))
                row.append(pixel)
                art_str += self.pixel_to_char(pixel, min_pixel, max_pixel)
            self.matrix.append(row)
            self.ascii_art.append(art_str)
        
        self.save_ascii_art(outfile)
        return self.ascii_art
    
    # save ascill art (as well as the digital matrix of the image) as a text file
    def save_ascii_art(self, outfile:str):
        logging.info(f'save ascii art to {outfile}')
        with open(outfile, 'w') as f:
            for art_str in self.ascii_art:
                f.write(art_str + '\n')
        outfile_mat = outfile + '.mat'
        logging.info(f'save digital matrix to {outfile_mat}')
        max_pixels = max([max(row) for row in self.matrix])
        decimal_digits = math.ceil(math.log10(max_pixels))
        logging.debug(f'max_pixels = {max_pixels}, decimal_digits = {decimal_digits}')
        with open(outfile_mat, 'w') as f:
            for row in self.matrix:
                f.write(' '.join([str(e).rjust(decimal_digits,' ') for e in row]) + '\n')
        return
    
    def draw_ascii_art(self):
        for art_str in self.ascii_art:
            print(art_str)
        return
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a picture into ASCII art')
    parser.add_argument('--infile', type=str, help='path of your image', required=True)
    parser.add_argument('--outfile', type=str, default='ascii_art.txt', help='outoput file')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG) 
    logging.debug(f'infile = {args.infile}, outfile = {args.outfile}')
    art = AsciiArt(scale_ratio_width = 1.8)
    art.image_to_ascii(args.infile, args.outfile) 
    art.draw_ascii_art()
    