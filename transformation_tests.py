import unittest
from array import array

from PIL import Image

from transformation import columnize, rgb_to_gamebuino_palette_index, palettize, gb_palette

""" A fake picture data of one sprite of 2x2 """
test_data_no_change = [0x12, 0x34,
                       0x56, 0x78]

""" A fake picture data of two sprite of 2x2 side by side """
test_data_to_columnize = [0x12, 0x34, 0x9A, 0xBC,
                          0x56, 0x78, 0xDE, 0xF0]


def image_from_palette_data(size, data_list):
    data = array('B', data_list).tobytes()
    image = Image.frombytes('P', size, data)
    return image


def image_from_rgba_data(size, data_list):
    data = array('B', data_list).tobytes()
    image = Image.frombytes('RGBA', size, data)
    return image


class ColumnizeCase(unittest.TestCase):
    def test_encoding_test_data_works(self):
        test_image = image_from_palette_data((2, 2), test_data_no_change)

        self.assertEqual(0x12, test_image.getpixel((0, 0)))
        self.assertEqual(0x34, test_image.getpixel((1, 0)))

    def test_columnize_sprites_already_in_column(self):
        test_image = image_from_palette_data((2, 2), test_data_no_change)
        column_image = columnize(test_image, (2, 2))

        self.assertEqual((2, 2), column_image.size)
        self.assertEqual(0x12, column_image.getpixel((0, 0)))
        self.assertEqual(0x34, column_image.getpixel((1, 0)))
        self.assertEqual(0x56, column_image.getpixel((0, 1)))
        self.assertEqual(0x78, column_image.getpixel((1, 1)))

    def test_columnize_sprites_not_in_column(self):
        test_image = image_from_palette_data((4, 2), test_data_to_columnize)
        column_image = columnize(test_image, (2, 2))

        self.assertEqual((2, 4), column_image.size)
        self.assertEqual(0x12, column_image.getpixel((0, 0)))
        self.assertEqual(0x34, column_image.getpixel((1, 0)))
        self.assertEqual(0x56, column_image.getpixel((0, 1)))
        self.assertEqual(0x78, column_image.getpixel((1, 1)))
        self.assertEqual(0x9A, column_image.getpixel((0, 2)))
        self.assertEqual(0xBC, column_image.getpixel((1, 2)))
        self.assertEqual(0xDE, column_image.getpixel((0, 3)))
        self.assertEqual(0xF0, column_image.getpixel((1, 3)))


test_rgb_data = [0x00, 0x00, 0x00, 0xFF, 0xDB, 0x1D, 0x23, 0xFF,
                 0xF5, 0xE7, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]


def rgba_tuple_to_color(rgba):
    r, g, b, a = rgba
    return (r << 24) + (g << 16) + (b << 8) + a


def rgb_from_palette(palette, index):
    r, g, b = palette[index * 3:index * 3 + 3]

    return (r << 16) + (g << 8) + b


class PaletteCase(unittest.TestCase):
    def test_gamebuino_palette(self):
        self.assertEqual(0, rgb_to_gamebuino_palette_index(0x000000))
        self.assertEqual(7, rgb_to_gamebuino_palette_index(0xFFFFFF))

        with self.assertRaises(ValueError):
            rgb_to_gamebuino_palette_index(0xFFFFFE)


class PalettizeCase(unittest.TestCase):
    def test_encoding_rgb_data_works(self):
        test_image = image_from_rgba_data((2, 2), test_rgb_data)

        self.assertEqual(0x000000FF, rgba_tuple_to_color(test_image.getpixel((0, 0))))
        self.assertEqual(0xFFFFFFFF, rgba_tuple_to_color(test_image.getpixel((1, 1))))

    def test_use_gamebuino_palette(self):
        test_image = image_from_rgba_data((2, 2), test_rgb_data)
        palette_image = palettize(test_image)

        self.assertEqual(test_image.size, palette_image.size)
        self.assertEqual('P', palette_image.mode)

        palette = palette_image.getpalette()
        content = palette_image.tobytes()

        # Re-expand to color and transform to Gamebuino palette
        rgb_content = (rgb_from_palette(palette, int(b)) for b in content)
        gb_content = (rgb_to_gamebuino_palette_index(rgb) for rgb in rgb_content)

        self.assertEqual([0x00, 0x08, 0x0A, 0x07], list(gb_content))


def im_palette_as_rgb(im_palette):
    from itertools import islice

    reds = islice(im_palette, 0, None, 3)
    greens = islice(im_palette, 1, None, 3)
    blues = islice(im_palette, 2, None, 3)

    return enumerate(zip(reds, greens, blues))


def palette_mapping(im_palette):
    mapping = {}
    missing_colors = 0

    for i, (r, g, b) in im_palette_as_rgb(im_palette):
        color = (r << 16) + (g << 8) + b

        if color in gb_palette:
            mapping[i] = gb_palette.index(color)
        else:
            missing_colors += 1

    return mapping, missing_colors


class PaletteMappingCase(unittest.TestCase):
    def test_map_only_black(self):
        black_palette = [0x00, 0x00, 0x00]
        mapping, missing = palette_mapping(black_palette)

        self.assertEqual(gb_palette.index(0x000000), mapping[0])
        self.assertEqual(0, missing)

    def test_map_black_and_white(self):
        palette = [0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00]
        mapping, missing = palette_mapping(palette)

        self.assertEqual(gb_palette.index(0xFFFFFF), mapping[0])
        self.assertEqual(gb_palette.index(0x000000), mapping[1])
        self.assertEqual(0, missing)

    def test_missing_colors_are_counter(self):
        palette = [0xFF, 0xFF, 0xFF, 0x00, 0x43, 0x85, 0x12, 0x34, 0x45]
        mapping, missing = palette_mapping(palette)

        self.assertEqual(1, missing)
        self.assertEqual(gb_palette.index(0xFFFFFF), mapping[0])
        self.assertEqual(gb_palette.index(0x004385), mapping[1])


if __name__ == '__main__':
    unittest.main()
