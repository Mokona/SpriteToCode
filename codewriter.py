def format_payload(raw_payload, width, tabs):
    """ Not the most elegant way of formatting the data payload. """

    payload_chunks = [raw_payload[i:i + width]
                      for i in range(0, len(raw_payload), width)]

    full_payload_format = (r"0x{:02X}, " * width)[:-2]

    payload = ""
    for payload_line in payload_chunks:
        element_count = len(payload_line)
        if element_count == width:
            payload_format = full_payload_format
        else:
            payload_format = (r"0x{:02X}, " * element_count)[:-2]

        payload += payload_format.format(*payload_line)
        payload += ",\n" + " " * tabs

    payload = payload[:-6]

    return payload


def apply_templates(templates, data):
    if "asset_name_lower" not in data:
        data["asset_name_lower"] = data["asset_name"].lower()

    data["frames_low"], data["frames_high"] = split_low_high_number(data["frames"])
    data["data_type"] = get_data_type(data["color_mode"])

    width = data["sprite_size"][0]
    data["payload"] = format_payload(data["raw_payload"], width, 4)

    return templates[0].format(**data), templates[1].format(**data)


def split_low_high_number(number):
    low = number & 0x00FF
    high = (number & 0xFF00) >> 8

    return low, high


def get_data_type(color_mode):
    return ["uint16_t", "uint8_t"][color_mode]
