#include "data_{asset_name_lower}.h"

namespace
{{
    const {data_type} data[] = {{
        {sprite_size[0]}, {sprite_size[1]},
        {frames_low}, {frames_high},
        {frame_loop},
        0x{transparent_color:X},
        {color_mode},
        {payload}
    }};
}}

const {data_type}* get{asset_name}Data()
{{
    return reinterpret_cast<const {data_type}*>(data);
}}
