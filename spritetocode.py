""" Convert picture files to an Image data usable for the Gamebuino.
"""
import argparse
import os.path
from extractinfo import extract_info_from_image, extract_info_from_filename, WrongFormat

from PIL import Image


def convert_file(filename):
    basename = os.path.basename(filename)
    try:
        filename_information = extract_info_from_filename(basename)
    except WrongFormat as e:
        print("Error in filename {}:".format(basename))
        print(e)
        return

    print(
        "{filename} is seen as '{asset_name}' of size {sprite_size} with frame loop {frame_loop}".format(
            filename=filename, **filename_information))

    image = Image.open(filename)

    image_information = extract_info_from_image(image)
    image_information.update(filename_information)

    print("Image has a size of {image_size}".format(**image_information))

    if image_information["palette"]:
        print("It has a palette")
    else:
        print("It has no palette")

        # Linearize the file
        # If it has a palette or if force_palette, color mode = 1
        # Else color mode = 0
        # If it has no palette and color mode == 1, transform to palette
        # Read the templates
        # Send to codewriter
        # Write the files


def convert():
    parser = argparse.ArgumentParser(description="Convert images to code for Gamebuino")
    parser.add_argument("file", nargs="+", help="list of files to convert")

    args = vars(parser.parse_args())
    files = args["file"]

    for f in files:
        convert_file(f)


if __name__ == '__main__':
    convert()
