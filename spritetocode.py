""" Convert picture files to an Image data usable for the Gamebuino.
"""
import argparse
import os.path

from PIL import Image

from codewriter import apply_templates
from extractinfo import extract_info_from_image, extract_info_from_filename, WrongFormat, compute_frame_count
from transformation import columnize, palette_mapping, palettize, pack_data

VERSION = "0.9"


class ApplicationError(Exception):
    pass


def read_templates(template_path):
    template_names = {"cpp": "data_template.cpp",
                      "h": "data_template.h"}

    template_content = {}

    for kind, filename in template_names.items():
        try:
            complete_filename = os.path.join(template_path, filename)
            with open(complete_filename, "rt") as f:
                content = f.read()
                template_content[kind] = content
        except FileNotFoundError as e:
            raise ApplicationError("Template was not found: {}".format(filename))

    return template_content


def write_files(output_path, asset_name, content):
    asset_name = asset_name.lower()
    filename = "data_" + asset_name

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    output_data_header = os.path.join(output_path, filename + ".h")
    with open(output_data_header, "wt") as f:
        f.write(content[0])

    output_data_body = os.path.join(output_path, filename + ".cpp")
    with open(output_data_body, "wt") as f:
        f.write(content[1])


def convert_file(filename, to_palette, template_path, output_path):
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
        image_information["color_mode"] = 1
        image_information["palette_mapping"] = palette_mapping(image.getpalette())
    else:
        image_information["color_mode"] = 0

    if image_information["palette"]:
        image_information["raw_payload"] = pack_data(image.getdata(), image_information["palette_mapping"])
        image_information["transparent_color"] = 0x00
    else:
        print("FATAL ERROR, RGB565 mode (mode 0) not yet supported.")
        print()
        return

    try:
        templates = read_templates(template_path)
    except ApplicationError as e:
        print("FATAL ERROR reading the templates.")
        print(e)
        print()
        return

    template_tuple = templates["h"], templates["cpp"]
    output_content = apply_templates(template_tuple, image_information)

    write_files(output_path, filename_information["asset_name"], output_content)

    print()


def convert():
    parser = argparse.ArgumentParser(description="Convert images to code for Gamebuino")
    parser.add_argument("--to_palette", action='store_true', default=False,
                        help="output image will have a palette if possible")
    parser.add_argument("--template_path", default=".",
                        help="path to find the file templates")
    parser.add_argument("--output_path", default=".",
                        help="path where the generate files are written to.")
    parser.add_argument('--version', action='version', version="%(prog)s " + VERSION)
    parser.add_argument("file", nargs="+", help="list of files to convert")

    args = vars(parser.parse_args())
    files = args["file"]

    for f in files:
        convert_file(f, args["to_palette"], args["template_path"], args["output_path"])


if __name__ == '__main__':
    convert()
