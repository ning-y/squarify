import sys
from PIL import Image, ImageChops, ImageFilter

def squarify(filename):
    content = Image.open(filename)
    background = get_background(content)
    print(background.size)
    return paste_center(content, background)

def get_background(content):
    r'''
    Returns a square PIL.Image of length max(*content.size), containing a
    gaussian blurred background.

    Does not mutate the input content.
    '''
    # Scale content, preserving aspect ratio, s.t. a square of length
    #   max(*content.size) can be covered.
    content_w, content_h = content.size
    content_aspect = content_w / content_h
    target_length = max(*content.size)

    background = content.copy()
    if content_aspect > 1:
        # Wide. Set height = target_length, and find width.
        background = background.resize(
                (int(target_length*content_aspect)+1, target_length),
                Image.ANTIALIAS)
    else:
        # Tall. Set width = target_length, and find height.
        background = background.resize(
                (target_length, int(target_length/content_aspect)+1),
                Image.ANTIALIAS)

    # Crop out from background a target_length * target_length square.
    bg_w, bg_h = background.size
    crop_x, crop_y = (bg_w - target_length) // 2, (bg_h - target_length) // 2
    background = background.crop(
            (crop_x, crop_y, crop_x + target_length, crop_y + target_length))
    background = background.filter(ImageFilter.GaussianBlur(target_length//100))

    return background

def paste_center(src, dest):
    r'''
    Pre-condition: src.size < dest.size for all dimensions. Paste the src
    PIL.Image onto the center of the dest PIL.Image.

    Does not mutate the input src, dest.
    '''
    src_w, src_h = src.size
    dest_w, dest_h = dest.size
    paste_x, paste_y = (dest_w - src_w) // 2, (dest_h - src_h) // 2

    to_return = dest.copy()
    to_return.paste(src, (paste_x, paste_y, paste_x+src_w, paste_y+src_h))
    return to_return

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ./image.py <input_image> <output_name>')
        sys.exit(1)
    with open(sys.argv[2], 'w') as outfile:
        squarify(sys.argv[1]).save(outfile, 'JPEG')
