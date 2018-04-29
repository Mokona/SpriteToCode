import unittest

from extractinfo import WrongFormat, extract_info_from_filename


class SpriteToCodeCase(unittest.TestCase):
    def test_filename_gives_information(self):
        filename = "Asset_8x4_fixed.png"
        information = extract_info_from_filename(filename)

        self.assertEqual("Asset", information["asset_name"])
        self.assertEqual((8, 4), information["sprite_size"])
        self.assertEqual(0, information["frame_loop"])
        self.assertNotIn("width", information)
        self.assertNotIn("height", information)
        self.assertNotIn("attribute", information)

    def test_filename_with_wrong_attribute(self):
        filename = "Asset_8x4_nothing.png"
        try:
            extract_info_from_filename(filename)
        except WrongFormat:
            pass
        else:
            self.assertFalse("Wrong attribute should raise")

    def test_filename_with_wrong_format(self):
        filename = "filename.png"
        try:
            extract_info_from_filename(filename)
        except WrongFormat:
            pass
        else:
            self.assertFalse("Wrong attribute should raise")

    def test_filename_with_looping(self):
        filename = "Asset_8x4_2.png"
        information = extract_info_from_filename(filename)
        self.assertEqual(2, information["frame_loop"])


if __name__ == '__main__':
    unittest.main()
