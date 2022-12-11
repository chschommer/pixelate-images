#!/usr/bin/env python3

from PIL import Image
import sys
import os
import multiprocessing as mp
from datetime import datetime


def avg_pixel_color_for_block(image, i_start, j_start, i_end, j_end):
    count = 0
    (r,g,b) = (0,0,0)

    if (i_end > image.width):
        i_end = image.width

    if (j_end > image.height):
        j_end = image.height
   
    for i in range(i_start, i_end):
        for j in range(j_start, j_end):
            (r_temp, g_temp, b_temp) = image.getpixel((i, j))
            (r,g,b) = (r+r_temp, g+g_temp, b+b_temp)
            count = count+1

    return (int(r/count), int(g/count), int(b/count))


def fill_block(image, color, i_start, j_start, i_end, j_end):
    if (i_end > image.width):
        i_end = image.width

    if (j_end > image.height):
        j_end = image.height

    for i in range(i_start, i_end):
        for j in range(j_start, j_end):
            image.putpixel((i,j), color)


def do_moasic(image, block_size):
    result = Image.new('RGB', (image.width, image.height), color = 'black')

    for i in range(0, image.width, block_size):
        for j in range(0, image.height, block_size):
            avg_color = avg_pixel_color_for_block(image, i, j, i + block_size, j + block_size)
            fill_block(result, avg_color, i,j, i+block_size, j+block_size)


    return result 


def do_Image(block_size):
    block_size = block_size

    directory = os.listdir(os.getcwd())

    im = Image.open(list(filter( lambda f: f.endswith(".JPG") or f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".webp"), directory))[0])
    rgb_im = im.convert('RGB')

    target = do_moasic(rgb_im, block_size)
    target.save("result_" + str(block_size) + ".png")

    print("Done with ", block_size, datetime.now() - start)

start = datetime.now()

if __name__ == '__main__':

    
    pool = mp.Pool(mp.cpu_count())

    for i in range(1, len(sys.argv)):
         #do_Image(int(sys.argv[i]))
         pool.apply_async(do_Image, (int(sys.argv[i]),))

    pool.close()
    pool.join()

    print("Took ", datetime.now() - start)

