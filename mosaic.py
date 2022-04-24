from PIL import Image
import sys
import os


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



block_size = int(sys.argv[1])

directory = os.listdir(os.getcwd())

im = Image.open(list(filter( lambda f: f.endswith(".jpg") or f.endswith(".jpeg"), directory))[0])
rgb_im = im.convert('RGB')

target = do_moasic(rgb_im, block_size)
target.save("result_" + str(block_size) + ".png")