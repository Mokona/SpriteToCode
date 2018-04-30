import unittest
from array import array

from PIL import Image

from transformation import columnize

""" A fake picture data of one sprite of 2x2 """
test_data_no_change = [0x12, 0x34,
                       0x56, 0x78]

""" A fake picture data of two sprite of 2x2 side by side """
test_data_to_columnize = [0x12, 0x34, 0x9A, 0xBC,
                          0x56, 0x78, 0xDE, 0xF0]


def image_from_test_data(size, data_list):
    data = array('B', data_list).tobytes()
    image = Image.frombytes('P', size, data)
    return image


class TransformationCase(unittest.TestCase):
    def test_encoding_test_data_works(self):
        test_image = image_from_test_data((2, 2), test_data_no_change)

        self.assertEqual(0x12, test_image.getpixel((0, 0)))
        self.assertEqual(0x34, test_image.getpixel((1, 0)))

    def test_columnize_sprites_already_in_column(self):
        test_image = image_from_test_data((2, 2), test_data_no_change)
        column_image = columnize(test_image, (2, 2))

        self.assertEqual((2, 2), column_image.size)
        self.assertEqual(0x12, column_image.getpixel((0, 0)))
        self.assertEqual(0x34, column_image.getpixel((1, 0)))
        self.assertEqual(0x56, column_image.getpixel((0, 1)))
        self.assertEqual(0x78, column_image.getpixel((1, 1)))

    def test_columnize_sprites_not_in_column(self):
        test_image = image_from_test_data((4, 2), test_data_to_columnize)
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


if __name__ == '__main__':
    unittest.main()
