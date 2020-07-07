def mask_to_json(mask):

    if mask.no_mask:
        return { 'no_mask': True }

    return {
        'feather': mask.feather,
        'mode': mask.mode,
        'band': mask.band,
        'fill_value': mask.fill_value,
        'threshold': mask.threshold,
        'hole_size': mask.hole_size,
        'white_fill': mask.white_fill,
        'no_data': mask.no_data
    }