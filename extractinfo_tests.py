import unittest

from extractinfo import extract_info_from_filename, WrongFormat, compute_frame_count


class ExtractInfoFromFilenameTestCase(unittest.TestCase):
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
        with self.assertRaises(WrongFormat):
            extract_info_from_filename(filename)

    def test_filename_with_wrong_format(self):
        filename = "filename.png"
        with self.assertRaises(WrongFormat):
            extract_info_from_filename(filename)

    def test_filename_with_looping(self):
        filename = "Asset_8x4_2.png"
        information = extract_info_from_filename(filename)
        self.assertEqual(2, information["frame_loop"])


class ComputeFramesTestCase(unittest.TestCase):
    def test_compute_frames(self):
        image_size = (32, 16)
        sprite_size = (16, 8)

        frame_count = compute_frame_count(image_size, sprite_size)

        self.assertEqual(4, frame_count)


if __name__ == '__main__':
    unittest.main()
