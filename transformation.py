from PIL import Image


def columnize(image, sprite_size):
    sprite_width, _ = sprite_size
    image_width, image_height = image.size

    vertical_bands_count = int(image_width / sprite_width)

    new_image_width = sprite_width
    new_image_height = int(image_height * vertical_bands_count)
    new_size = new_image_width, new_image_height

    new_image = Image.new(image.mode, new_size)

    palette = image.getpalette()
    if palette:
        new_image.putpalette(palette)

    for count in range(vertical_bands_count):
        band_x_coordinates = count * sprite_width, ((count + 1) * sprite_width)
        band = image.crop((band_x_coordinates[0], 0, band_x_coordinates[1], image_height))

        new_image.paste(band, (0, count * image_height))

    return new_image


gb_palette = [
    0x000000, 0x004385, 0x960040, 0x008B50, 0xCF8E44, 0x544D43, 0xA89987,
    0xFFFFFF, 0xDB1D23, 0xFFA811, 0xF5E700, 0x85CF44, 0x7DBBFF, 0x4485CF,
    0xCF4485, 0xFFD690
]


def rgb_to_gamebuino_palette_index(rgb):
    return gb_palette.index(rgb)


def palettize(source_image):
    palette_image = source_image.convert('P', palette=Image.ADAPTIVE)
    return palette_image
