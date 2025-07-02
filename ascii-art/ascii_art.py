from PIL import Image, ImageDraw, ImageFont
import math
import argparse
import logging
import time
import os

logging.basicConfig(format='[%(levelname)s] [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)

class AsciiArt:
    def __init__(self, scale_ratio_width:float=1.0, scale_ratio_height:float=1.0, max_width:int=90, max_height:int=90, ascii_chars:str=" %#*+=-:"):
        self.ascii_chars = ascii_chars
        self.ascii_art = [] # list of all ascii art strings of rows
        self.scale_ratio_width = scale_ratio_width # width scale ratio
        self.scale_ratio_height = scale_ratio_height # height scale ratio
        logging.info(f'scale_ratio_width = {self.scale_ratio_width}, scale_ratio_height = {self.scale_ratio_height}')
        self.max_width = max_width # max number of ascii characters of each row
        self.max_height = max_height # max number of ascii characters of each column
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

    # convert image into text of ascii art
    def image_to_ascii(self, img_path:str, outfile:str=None, save_digital_img:bool=None):
        outfile = 'ascii_art.txt' if outfile is None else outfile
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
        if save_digital_img == True:
            self.save_decimal_digits(outfile+'.mat')
        logging.info(f'outfile = {outfile}')
        return self.ascii_art
    
    # convert image into text of ascii art
    def image_to_ascii_batch(self, indir:str, outdir:str=None):
        outdir = 'ascii_arts' if outdir is None else outdir
        images = os.listdir(indir)
        images.sort()
        images = [os.path.join(indir, image) for image in images]
        os.makedirs(outdir, exist_ok=True)
        for image in images:
            path = os.path.join(outdir, image.split('/')[-1] + '.txt')
            self.image_to_ascii(image, path) 
            # pic_path = os.path.join(outdir_png, image.split('/')[-1] + '.png')
            # self.ascii_art_to_image(pic_path)
        logging.info(f'outdir = {outdir}')
        return outdir
    
    # save ascill art as a text file
    def save_ascii_art(self, outfile:str):
        logging.info(f'save ascii art to {outfile}')
        with open(outfile, 'w') as f:
            for art_str in self.ascii_art:
                f.write(art_str + '\n')
        return
    
    # save image as decimal digits text file
    def save_decimal_digits(self, outfile:str):
        logging.info(f'save digital matrix to {outfile}')
        max_pixels = max([max(row) for row in self.matrix])
        decimal_digits = math.ceil(math.log10(max_pixels))
        logging.debug(f'max_pixels = {max_pixels}, decimal_digits = {decimal_digits}')
        with open(outfile, 'w') as f:
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
    def ascii_art_to_image(self, outfile:str=None, font_size:int = 24, 
                            text_color=(0, 0, 0),
                            bgc=(255, 255, 255), # background color
                            line_spacing=1.2):
        outfile = 'ascii_art.png' if outfile is None else outfile
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
    
    # convert batch of ascii art texts into batch of images
    def ascii_art_to_image_batch(self, indir:str, outdir:str=None, font_size:int = 24, 
                            text_color=(0, 0, 0),
                            bgc=(255, 255, 255), # background color
                            line_spacing=1.2):
        outdir = 'ascii_art_png' if outdir is None else outdir
        ascii_arts = os.listdir(indir)
        ascii_arts.sort()
        ascii_arts = [os.path.join(indir, ascii_art) for ascii_art in ascii_arts]
        os.makedirs(outdir, exist_ok=True)
        for ascii_art in ascii_arts:
            self.load_ascii_art(ascii_art)
            path = os.path.join(outdir, ascii_art.split('/')[-1] + '.png')
            self.ascii_art_to_image(path, font_size, text_color, bgc, line_spacing)
        logging.info(f'outdir = {outdir}')
        return outdir

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a picture into ASCII art')
    subparsers = parser.add_subparsers(dest="command", title="available commands", metavar="command")
    parser_img2txt = subparsers.add_parser("img2txt", help="convert a picture into ascii art text", description="convert a picture into ascii art text")
    parser_img2txt.add_argument('--infile', type=str, help='path of your image', required=True)
    parser_img2txt.add_argument('--outfile', type=str, default=None, help='outoput file')
    parser_img2txt.add_argument('--speed', type=float, default=0.0, help='speed of drawing ascii art')
    
    parser_txt2img = subparsers.add_parser("txt2img", help="convert a ascii art txt into a picture", description="convert a ascii art txt into a picture")
    parser_txt2img.add_argument('--infile', type=str, help='path of your ascii art', required=True)
    parser_txt2img.add_argument('--outfile', type=str, default=None, help='outoput picture')

    parser_imgs2imgs = subparsers.add_parser("imgs2imgs", help="convert a batch of images into a batch of ascii-art images in ASCII art form")
    parser_imgs2imgs.add_argument('--indir', type=str, help='directory of the original images', required=True)
    parser_imgs2imgs.add_argument('--outdir', type=str, default=None, help='output directory')

    args = parser.parse_args()

    if not hasattr(args, "command") or args.command is None:
        parser.print_help()
    if args.command == 'img2txt':
        logging.basicConfig(level=logging.DEBUG) 
        logging.debug(f'infile = {args.infile}, outfile = {args.outfile}')
        art = AsciiArt(scale_ratio_width = 1.8)
        art.image_to_ascii(args.infile, args.outfile) 
        art.draw_ascii_art(speed=args.speed)
        art.ascii_art_to_image('ascii_art.png')
    elif args.command == 'txt2img':
        art = AsciiArt(scale_ratio_width = 1.8)
        art.load_ascii_art(args.infile)
        art.ascii_art_to_image(args.outfile)
    elif args.command == 'imgs2imgs':
        art = AsciiArt(scale_ratio_width = 1.8, max_width=240, ascii_chars=" %#*+=-:,.&$!^abcdfghjpqrstuvwxwzmn")
        ascii_txt_dir = 'ascii_txt'
        art.image_to_ascii_batch(args.indir, ascii_txt_dir)
        art.ascii_art_to_image_batch(ascii_txt_dir, args.outdir)