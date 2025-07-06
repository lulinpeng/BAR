from PIL import Image, ImageDraw, ImageFont
import math
import argparse
import logging
import time

logging.basicConfig(format='[%(levelname)s] [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)

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
        logging.info(f'outfile = {outfile}')
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
    
    # draw ascii art by print each row ascii art string every 'speed' seconds
    def draw_ascii_art(self, speed:float=0.0):
        for art_str in self.ascii_art:
            print(art_str)
            time.sleep(speed)
        return
    
    # load ascill art from text file
    def load_ascii_art(self, infile:str):
        with open(infile) as f:
            self.ascii_art = f.readlines()
        return
    
    # convert ascii art text into image
    def ascii_art_to_image(self, outfile:str, font_size:int = 24, 
                            text_color=(0, 0, 0),
                            bgc=(255, 255, 255), # background color
                            line_spacing=1.2):
        # get font
        font = ImageFont.truetype("./fonts/Monaco.ttf", font_size)
        logging.debug(f'font = {font}')

        max_line = max(self.ascii_art, key=len) # line with max length
        logging.debug(f'max_line = {max_line}, {type(max_line)}')

        bbox = font.getbbox(max_line) # bounding box of given text
        logging.debug(f'bbox = {bbox}')
        
        char_width, char_height = bbox[2], bbox[3]
        # image size
        width = int(char_width)
        height_step = int(char_height * line_spacing)
        height = int(len(self.ascii_art) * height_step)
        
        canvas = Image.new("RGB", (width, height), bgc)
        draw = ImageDraw.Draw(canvas)
        y = 0
        for line in self.ascii_art:
            draw.text((0, y), line, fill=text_color, font=font)
            y += height_step

        canvas.save(outfile)  # save it as picture
        logging.info(f'outfile = {outfile}')
        return outfile

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a picture into ASCII art')
    parser.add_argument('--infile', type=str, help='path of your image', required=True)
    parser.add_argument('--outfile', type=str, default='ascii_art.txt', help='outoput file')
    parser.add_argument('--speed', type=float, default=0.0, help='speed of drawing ascii art')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG) 
    logging.debug(f'infile = {args.infile}, outfile = {args.outfile}')
    art = AsciiArt(scale_ratio_width = 1.8)
    art.image_to_ascii(args.infile, args.outfile) 
    art.draw_ascii_art(speed=args.speed)
    art.ascii_art_to_image('ascii_art.png')
    