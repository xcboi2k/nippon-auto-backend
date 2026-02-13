def filter_by_vehicle_type(options, vehicle_type):
    if not vehicle_type:
        return options

    return [
        item for item in options
        if "applicable_to" not in item
        or vehicle_type in item["applicable_to"]
    ]
