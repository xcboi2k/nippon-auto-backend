VEHICLE_TYPES = [
    {"key": "sedan", "label": "Sedan"},
    {"key": "suv", "label": "SUV"},
    {"key": "hatchback", "label": "Hatchback"},
    {"key": "pickup", "label": "Pickup"},
    {"key": "van", "label": "Van"},
    {"key": "truck", "label": "Truck"},
    {"key": "bus", "label": "Bus"},
    {"key": "motorcycle", "label": "Motorcycle"},
]

ENGINE_TYPES = [
    {"key": "gasoline", "label": "Gasoline"},
    {"key": "diesel", "label": "Diesel"},
    {"key": "electric", "label": "Electric"},
    {"key": "hybrid", "label": "Hybrid"},
    {"key": "plug_in_hybrid", "label": "Plug-in Hybrid"},
]

DRIVE_TRAINS = [
    {"key": "fwd", "label": "Front-Wheel Drive (FWD)", "applicable_to": ["sedan", "suv", "hatchback", "pickup", "van", "truck", "bus"]},
    {"key": "rwd", "label": "Rear-Wheel Drive (RWD)", "applicable_to": ["sedan", "suv", "pickup", "truck", "bus"]},
    {"key": "awd", "label": "All-Wheel Drive (AWD)", "applicable_to": ["suv", "pickup"]},
    {"key": "4wd", "label": "Four-Wheel Drive (4WD)", "applicable_to": ["pickup", "truck"]},
    {"key": "chain_drive", "label": "Chain Drive", "applicable_to": ["motorcycle"]},
    {"key": "belt_drive", "label": "Belt Drive", "applicable_to": ["motorcycle"]},
    {"key": "shaft_drive", "label": "Shaft Drive", "applicable_to": ["motorcycle"]},
]

TRANSMISSIONS = [
    {"key": "manual", "label": "Manual", "applicable_to": ["sedan", "suv", "hatchback", "pickup", "van", "truck", "bus", "motorcycle"]},
    {"key": "automatic", "label": "Automatic", "applicable_to": ["sedan", "suv", "hatchback", "pickup", "van", "truck", "bus", "motorcycle"]},
    {"key": "cvt", "label": "CVT", "applicable_to": ["sedan", "suv", "hatchback"]},
    {"key": "e_cvt", "label": "Electronic CVT", "applicable_to": ["sedan", "suv", "hatchback"]},
    {"key": "dual_clutch", "label": "Dual-Clutch", "applicable_to": ["sedan", "suv", "pickup"]},
    {"key": "amt", "label": "Automated Manual", "applicable_to": ["sedan", "hatchback"]},
    {"key": "semi_automatic", "label": "Semi-Automatic", "applicable_to": ["motorcycle"]},
]
