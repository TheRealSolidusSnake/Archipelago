from BaseClasses import Item

class MGSItems(Item):
    game: str = 'Metal Gear Solid'

base_mgs_item_id = 69 # nice.

item_names = [
    # 'Cigarettes',
    # 'Scope',
    'Cardboard Box A',
    'Cardboard Box B',
    'Cardboard Box C',
    'Night Vision Goggles',
    'Thermal Goggles',
    'Gas Mask',
    'Body Armor',
    'Ketchup',
    # 'Stealth',
    # 'Bandana',
    # 'Camera',
    'Ration',
    'Medicine',
    'Diazepam',
    'Pal Key',
    'Key Card',
    # 'Time Bomb',
    'Mine Detector',
    # 'Disc',
    'Rope',
    'Handkerchief',
    'Suppressor',
    'SOCOM',
    'FA-MAS',
    'Grenade',
    'Nikita',
    'Stinger',
    'Claymore',
    'C4',
    'Stun Grenade',
    'Chaff Grenade',
    'PSG-1',
    'Dogtag',
    'Boss Dogtag',
    'Victory',
]

item_name_to_id_table = dict([(name, i+base_mgs_item_id) for (i, name) in enumerate(item_names)])