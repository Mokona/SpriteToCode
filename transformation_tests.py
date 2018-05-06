import unittest
from array import array

from PIL import Image

from transformation import columnize, rgb_to_gamebuino_palette_index, palettize, gb_palette, palette_mapping, pack_data

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


class PaletteMappingCase(unittest.TestCase):
    def test_map_only_black(self):
        black_palette = [0x00, 0x00, 0x00]
        mapping = palette_mapping(black_palette)

        self.assertEqual(gb_palette.index(0x000000), mapping[0])

    def test_map_black_and_white(self):
        palette = [0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00]
        mapping = palette_mapping(palette)

        self.assertEqual(gb_palette.index(0xFFFFFF), mapping[0])
        self.assertEqual(gb_palette.index(0x000000), mapping[1])

    def test_missing_colors_are_mapped_to_black(self):
        palette = [0xFF, 0xFF, 0xFF, 0x00, 0x43, 0x85, 0x12, 0x34, 0x45]
        mapping = palette_mapping(palette)

        self.assertEqual(gb_palette.index(0xFFFFFF), mapping[0])
        self.assertEqual(gb_palette.index(0x004385), mapping[1])
        self.assertEqual(gb_palette.index(0x000000), mapping[2])


class PackDataCase(unittest.TestCase):
    def test_pack_data_with_identity_mapping(self):
        image_data = [0x00, 0x08, 0x0F, 0x02]
        mapping = {x: x for x in range(16)}
        packed_data = pack_data(image_data, mapping)

        self.assertEqual([0x08, 0xF2], packed_data)

    def test_pack_data_with_mapping(self):
        image_data = [0x00, 0x08, 0x0F, 0x02]
        mapping = {x: x for x in range(16)}
        mapping[0x00] = 0x0F
        mapping[0x02] = 0x00
        mapping[0x08] = 0x02
        mapping[0x0F] = 0x08
        packed_data = pack_data(image_data, mapping)

        self.assertEqual([0xF2, 0x80], packed_data)

    def test_pack_data_with_out_of_bound_index_maps_to_0(self):
        image_data = [0x00, 0x08, 0x2F, 0x02]
        mapping = {x: x for x in range(16)}
        packed_data = pack_data(image_data, mapping)

        self.assertEqual([0x08, 0x02], packed_data)


if __name__ == '__main__':
    unittest.main()
