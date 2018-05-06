""" Convert picture files to an Image data usable for the Gamebuino.
"""
import argparse
import os.path

from PIL import Image

import transformation
from extractinfo import extract_info_from_image, extract_info_from_filename, WrongFormat
from transformation_tests import palette_mapping


def convert_file(filename, to_palette):
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

    try:
        image = Image.open(filename)
    except FileNotFoundError as e:
        print("Cannot open file {}".format(filename))
        print(e)
        return

    image_information = extract_info_from_image(image)
    image_information.update(filename_information)

    print("Image has a size of {image_size}".format(**image_information))

    if image_information["palette"]:
        print("It has a palette")
    else:
        print("It has no palette")

    image = transformation.columnize(image, (image_information["sprite_size"]))

    print("Image has been transformed to a {} image".format(image.size))

    if to_palette and image.mode != 'P':
        image = transformation.palettize(image)
        image_information["palette"] = image.getpalette()
        print("It now has a palette (--to_palette)")

    if image_information["palette"]:
        image_information["color_mode"] = 0
        image_information["palette_mapping"] = palette_mapping(image.getpalette())
    else:
        image_information["color_mode"] = 1

        # Read the templates
        # Send to codewriter
        # Write the files


def convert():
    parser = argparse.ArgumentParser(description="Convert images to code for Gamebuino")
    parser.add_argument("--to_palette", action='store_true', default=False,
                        help="output image will have a palette if possible")
    parser.add_argument("file", nargs="+", help="list of files to convert")

    args = vars(parser.parse_args())
    files = args["file"]

    for f in files:
        convert_file(f, args["to_palette"])


if __name__ == '__main__':
    convert()
