""" Convert picture files to an Image data usable for the Gamebuino.
"""
import argparse
import os.path

from PIL import Image

from codewriter import apply_templates
from extractinfo import extract_info_from_image, extract_info_from_filename, WrongFormat, compute_frame_count
from transformation import columnize, palette_mapping, palettize


class ApplicationError(Exception):
    pass


def read_templates(template_path):
    template_names = {"cpp": "data_template.cpp",
                      "h": "data_template.h"}

    template_content = {}

    for kind, filename in template_names.items():
        try:
            with open(filename, "rt") as f:
                content = f.readlines()
                template_content[kind] = content
        except FileNotFoundError as e:
            raise ApplicationError("Template was not found: {}".format(filename))

    return template_content


def convert_file(filename, to_palette, template_path):
    basename = os.path.basename(filename)
    try:
        filename_information = extract_info_from_filename(basename)
    except WrongFormat as e:
        print("Error in filename {}:".format(basename))
        print(e)
        print()
        return

    print(
        "{filename} is seen as '{asset_name}' of size {sprite_size} with frame loop {frame_loop}".format(
            filename=filename, **filename_information))

    try:
        image = Image.open(filename)
    except FileNotFoundError as e:
        print("Cannot open file {}".format(filename))
        print(e)
        print()
        return

    image_information = extract_info_from_image(image)
    image_information.update(filename_information)

    print("Image has a size of {image_size}".format(**image_information))

    image_information["frames"] = compute_frame_count(image_information["image_size"],
                                                      image_information["sprite_size"])

    print("Image contains {} frame(s)".format(image_information["frames"]))

    if image_information["palette"]:
        print("It has a palette")
    else:
        print("It has no palette")

    image = columnize(image, (image_information["sprite_size"]))

    print("Image has been transformed to a {} image".format(image.size))

    if to_palette and image.mode != 'P':
        image = palettize(image)
        image_information["palette"] = image.getpalette()
        print("It now has a palette (--to_palette)")

    if image_information["palette"]:
        image_information["color_mode"] = 0
        image_information["palette_mapping"] = palette_mapping(image.getpalette())
    else:
        image_information["color_mode"] = 1

    try:
        templates = read_templates(template_path)
    except ApplicationError as e:
        print("FATAL ERROR reading the templates.")
        print(e)
        print()
        return
    print()


def convert():
    parser = argparse.ArgumentParser(description="Convert images to code for Gamebuino")
    parser.add_argument("--to_palette", action='store_true', default=False,
                        help="output image will have a palette if possible")
    parser.add_argument("--template_path", default=".",
                        help="path to find the file templates")
    parser.add_argument("file", nargs="+", help="list of files to convert")

    args = vars(parser.parse_args())
    files = args["file"]

    for f in files:
        convert_file(f, args["to_palette"], args["template_path"])


if __name__ == '__main__':
    convert()
