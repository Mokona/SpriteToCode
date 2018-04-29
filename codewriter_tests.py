import unittest

from codewriter import apply_templates, split_low_high_number, get_data_type

test_template_h = r"""#pragma once

#include <cstdint>

const {data_type}* get{asset_name}Data();
"""

verify_template_h = r"""#pragma once

#include <cstdint>

const uint8_t* getAssetData();
"""

test_template_cpp = r"""#include "data_{asset_name_lower}.h"

const {data_type} data[] = {{
    {sprite_size[0]}, {sprite_size[1]},
    {frames_low}, {frames_high},
    {frame_loop},
    0x{transparent_color:X},
    {color_mode},
    {payload}
}};

const {data_type}* get{asset_name}Data()
{{
    return reinterpret_cast<const {data_type}*>(data);
}}"""

verify_template_cpp = r"""#include "data_asset.h"

const uint8_t data[] = {
    4, 2,
    1, 0,
    0,
    0x0,
    1,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00
};

const uint8_t* getAssetData()
{
    return reinterpret_cast<const uint8_t*>(data);
}"""


class CodeWriterCase(unittest.TestCase):
    def test_split_low_high_frames(self):
        low, high = split_low_high_number(0x4512)

        self.assertEqual(0x45, high)
        self.assertEqual(0x12, low)

    def test_choose_data_type_from_mode(self):
        data_type = get_data_type(color_mode=0)
        self.assertEqual("uint16_t", data_type)

        data_type = get_data_type(color_mode=1)
        self.assertEqual("uint8_t", data_type)

    def test_template_is_expanded(self):
        templates = (test_template_h, test_template_cpp)
        data = {
            "asset_name": "Asset",
            "sprite_size": (4, 2),
            "frames": 1,
            "frame_loop": 0,
            "transparent_color": 0,
            "color_mode": 1,
            "raw_payload": [0] * 8
        }
        files = apply_templates(templates, data)

        self.assertEqual(files[0], verify_template_h)
        self.assertEqual(files[1], verify_template_cpp)


if __name__ == '__main__':
    unittest.main()
