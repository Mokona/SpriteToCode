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
