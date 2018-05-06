import re


class WrongFormat(Exception):
    pass


file_re = re.compile(r"(?P<asset_name>[a-zA-Z0-9]+)_(?P<width>\d+)x(?P<height>\d+)_(?P<attribute>\w+)\..*")


def extract_info_from_filename(filename):
    extract = file_re.search(filename)

    if not extract:
        raise WrongFormat("The filename should respect the format {AssetName}_{Width}x{Height}_{fixed|loop frame}")

    information = extract.groupdict()
    size = int(information["width"]), int(information["height"])
    information["sprite_size"] = size

    attribute = information["attribute"]
    if attribute == "fixed":
        information["frame_loop"] = 0
    else:
        try:
            information["frame_loop"] = int(attribute)
        except ValueError:
            raise WrongFormat("Attribute should be 'fixed' or the frame loop number")

    del information["width"]
    del information["height"]
    del information["attribute"]

    return information


def extract_info_from_image(image):
    return {"image_size": image.size,
            "palette": image.getpalette()}


def compute_frame_count(image_size, sprite_size):
    width = image_size[0] / sprite_size[0]
    height = image_size[1] / sprite_size[1]
    return int(width * height)