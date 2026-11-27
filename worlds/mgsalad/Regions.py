from BaseClasses import ItemClassification
from . import Items
from BaseClasses import Region
from . import Locations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import MGSWorld

# Disliked the old locations scheme without any regions.. so here we go

def full_location_name(region_name: str, location_name: str) -> str:
    return f"{region_name} - {location_name}"

def get_location_region_name(region_name: str) -> str:
    return region_name

REPEATED_LOCATION_PREFIXES = (
    "Ration",
    "Medicine",
    "Diazepam",
    "SOCOM",
    "FA-MAS",
    "Grenade",
    "Nikita",
    "Stinger",
    "Claymore",
    "C4",
    "Stun Grenade",
    "Chaff Grenade",
    "PSG-1",
)

ORIGINAL_LOCATION_PAIRS = [
        ('Docks', 'Ration 1'),
        ('Docks', 'Ration 2'),
        ('Docks', 'Ration 3'),
        ('Heliport', 'Chaff Grenade 1'),
        ('Heliport', 'Stun Grenade 1'),
        ('Heliport', 'SOCOM 1'),
        ('Heliport', 'Ration 4'),
        ('Tank Hangar', 'Chaff Grenade 2'),
        ('Tank Hangar', 'Thermal Goggles'),
        ('Tank Hangar', 'SOCOM 2'),
        ('Tank Hangar', 'Ration 5'),
        ('Tank Hangar_lvl1', 'Suppressor'),
        ('Tank Hangar_lvl1', 'Cardboard Box A'),
        ('Tank Hangar_lvl2', 'Mine Detector'),
        ('Armory', 'SOCOM 3'),
        ('Armory', 'SOCOM 4'),
        ('Armory_lvl1', 'C4 1'),
        ('Armory_lvl1', 'C4 2'),
        ('Armory_lvl1', 'Grenade 1'),
        ('Armory_lvl1', 'Grenade 2'),
        ('Armory_lvl2', 'FA-MAS 1'),
        ('Armory_lvl2', 'FA-MAS 2'),
        ('Armory_lvl2', 'FA-MAS 3'),
        ('Armory_lvl3', 'Nikita 1'),
        ('Armory_lvl3', 'Nikita 2'),
        ('Armory_lvl5', 'PSG-1 1'),
        ('Armory_lvl5', 'PSG-1 2'),
        ('Armory_lvl5', 'PSG-1 3'),
        ('Cell', 'Key Card Level 1'),
        ('Cell', 'SOCOM 5'),
        ('Cell', 'SOCOM 6'),
        ('Cell', 'SOCOM 7'),
        ('Cell', 'SOCOM 8'),
        ('Cell', 'SOCOM 9'),
        ('Cell', 'SOCOM 10'),
        ('Cell', 'Ration 6'),
        ('Cell', 'Ration 7'),
        ('Cell', 'Ration 8'),
        ('Cell', 'Ration 9'),
        ('Cell', 'BOSS: Heavily Armed Genome Soldiers'),
        ('Armory Sth', 'SOCOM 11'),
        ('Armory Sth', 'SOCOM 12'),
        ('Armory Sth', 'SOCOM 13'),
        ('Armory Sth', 'Key Card Level 2'),
        ('Armory Sth', 'BOSS: Revolver Ocelot'),
        ('Armory Sth_C4', 'Ration 10'),
        ('Armory Sth_C4', 'C4 3'),
        ('Armory Sth_C4_lvl4', 'Stinger 1'),
        ('Armory Sth_C4_lvl4', 'Camera'),
        ('Armory Sth_C4_lvl6', 'Stinger 2'),
        ('Armory Sth_C4_lvl6', 'Stinger 3'),
        ('Armory Sth_C4_lvl6', 'Stinger 4'),
        ('Armory Sth_C4_lvl6', 'Stun Grenade 2'),
        ('Armory Sth_C4_lvl6', 'Chaff Grenade 3'),
        ('Canyon', 'Ration 11'),
        ('Canyon', 'Grenade 3'),
        ('Canyon', 'Grenade 4'),
        ('Canyon', 'Grenade 5'),
        ('Canyon', 'Chaff Grenade 4'),
        ('Canyon', 'Claymore 1'),
        ('Canyon', 'Claymore 2'),
        ('Canyon', 'Claymore 3'),
        ('Canyon', 'BOSS: M1 Tank'),
        ('Canyon', 'Key Card Level 3'),
        ('Nuke Building 1', 'Ration 12'),
        ('Nuke Building 1', 'Grenade 6'),
        ('Nuke Building 1', 'Chaff Grenade 5'),
        ('Nuke Building 1', 'FA-MAS 4'),
        ('Nuke Building 1', 'FA-MAS 5'),
        ('Nuke Building 1', 'SOCOM 14'),
        ('Nuke Building B1', 'Stun Grenade 3'),
        ('Nuke Building B1', 'Nikita 3'),
        ('Nuke Building B1', 'Nikita 4'),
        ('Nuke Building B1', 'Nikita 5'),
        ('Nuke Building B1', 'SOCOM 15'),
        ('Nuke Building B1', 'FA-MAS 6'),
        ('Nuke Building B1 lvl4', 'Cardboard Box B'),
        ('Nuke Building B1 lvl4', 'Ration 13'),
        ('Nuke Building B1 lvl4', 'SOCOM 16'),
        ('Nuke Building B1 lvl4', 'FA-MAS 7'),
        ('Nuke Building B1 lvl4', 'Pal Key'),
        ('Nuke Building B1 lvl4', 'Key Card Level 5'),
        ('Nuke Building B1 lvl5', 'Diazepam 1'),
        ('Nuke Building B1 lvl5', 'FA-MAS 8'),
        ('Nuke Building B1 lvl5', 'FA-MAS 9'),
        ('Nuke Building B1 lvl5', 'FA-MAS 10'),
        ('Nuke Building B2', 'Ration 14'),
        ('Nuke Building B2', 'Ration 15'),
        ('Nuke Building B2', 'Gas Mask'),
        ('Nuke Building B2', 'C4 4'),
        ('Nuke Building B2', 'Grenade 7'),
        ('Nuke Building B2', 'Grenade 8'),
        ('Nuke Building B2', 'Chaff Grenade 6'),
        ('Nuke Building B2', 'FA-MAS 11'),
        ('Nuke Building B2', 'Nikita 6'),
        ('Nuke Building B2', 'Nikita 7'),
        ('Nuke Building B2 lvl4', 'Stun Grenade 4'),
        ('Nuke Building B2 lvl4', 'Stun Grenade 5'),
        ('Nuke Building B2 lvl4', 'Night Vision Goggles'),
        ('Lab', 'Ration 16'),
        ('Lab', 'SOCOM 17'),
        ('Lab', 'FA-MAS 12'),
        ('Lab', 'FA-MAS 13'),
        ('Lab', 'Chaff Grenade 7'),
        ('Lab', 'Key Card Level 4'),
        ('Lab', 'BOSS: Gray Fox'),
        ('Commander Room', 'Ration 17'),
        ('Commander Room', 'Ration 18'),
        ('Commander Room', 'SOCOM 18'),
        ('Commander Room', 'SOCOM 19'),
        ('Commander Room', 'FA-MAS 14'),
        ('Commander Room', 'FA-MAS 15'),
        ('Commander Room', 'FA-MAS 16'),
        ('Commander Room', 'BOSS: Psycho Mantis'),
        ('Cave', 'Ration 19'),
        ('Cave', 'Ration 20'),
        ('Cave', 'Ration 21'),
        ('Cave', 'SOCOM 20'),
        ('Cave', 'FA-MAS 17'),
        ('Cave', 'FA-MAS 18'),
        ('Cave', 'Diazepam 2'),
        ('Cave', 'PSG-1 4'),
        ('Cave', 'PSG-1 5'),
        ('Cave', 'PSG-1 6'),
        ('Underground Passage', 'Ration 22'),
        ('Underground Passage', 'SOCOM 21'),
        ('Underground Passage', 'FA-MAS 19'),
        ('Underground Passage', 'PSG-1 7'),
        ('Underground Passage', 'PSG-1 8'),
        ('Underground Passage', 'PSG-1 9'),
        ('Underground Passage', 'PSG-1 10'),
        ('Underground Passage', 'BOSS: Sniper Wolf I'),
        ('Medi Room', 'Ration 23'),
        ('Medi Room', 'Handkerchief'),
        ('Medi Room', 'Key Card Level 6'),
        ('Comm Tower A', 'Ration 24'),
        ('Comm Tower A', 'Ration 25'),
        ('Comm Tower A', 'Ration 26'),
        ('Comm Tower A', 'SOCOM 22'),
        ('Comm Tower A', 'SOCOM 23'),
        ('Comm Tower A', 'SOCOM 24'),
        ('Comm Tower A', 'SOCOM 25'),
        ('Comm Tower A', 'SOCOM 26'),
        ('Comm Tower A', 'SOCOM 27'),
        ('Comm Tower A', 'SOCOM 28'),
        ('Comm Tower A', 'FA-MAS 20'),
        ('Comm Tower A', 'FA-MAS 21'),
        ('Comm Tower A', 'FA-MAS 22'),
        ('Comm Tower A', 'FA-MAS 23'),
        ('Comm Tower A', 'FA-MAS 24'),
        ('Comm Tower A', 'FA-MAS 25'),
        ('Comm Tower A', 'FA-MAS 26'),
        ('Comm Tower A', 'FA-MAS 27'),
        ('Comm Tower A', 'FA-MAS 28'),
        ('Comm Tower A', 'Stun Grenade 6'),
        ('Comm Tower A', 'Rope'),
        ('Comm Tower A', 'BOSS: Black-outfitted Genome Soldiers I'),
        ('Walkway', 'Ration 27'),
        ('Walkway', 'Ration 28'),
        ('Walkway', 'C4 5'),
        ('Walkway', 'Stinger 5'),
        ('Comm Tower B', 'Ration 29'),
        ('Comm Tower B', 'SOCOM 29'),
        ('Comm Tower B', 'FA-MAS 29'),
        ('Comm Tower B', 'FA-MAS 30'),
        ('Comm Tower B', 'Grenade 9'),
        ('Comm Tower B', 'Chaff Grenade 8'),
        ('Comm Tower B', 'Stinger 6'),
        ('Comm Tower B', 'Stinger 7'),
        ('Comm Tower B', 'Stinger 8'),
        ('Comm Tower B (Hind D[efeated])', 'Ration 30'),
        ('Comm Tower B (Hind D[efeated])', 'Ration 49'),
        ('Comm Tower B (Hind D[efeated])', 'SOCOM 30'),
        ('Comm Tower B (Hind D[efeated])', 'SOCOM 31'),
        ('Comm Tower B (Hind D[efeated])', 'FA-MAS 31'),
        ('Comm Tower B (Hind D[efeated])', 'FA-MAS 32'),
        ('Comm Tower B (Hind D[efeated])', 'FA-MAS 33'),
        ('Comm Tower B (Hind D[efeated])', 'FA-MAS 34'),
        ('Comm Tower B (Hind D[efeated])', 'FA-MAS 35'),
        ('Comm Tower B (Hind D[efeated])', 'FA-MAS 36'),
        ('Comm Tower B (Hind D[efeated])', 'Chaff Grenade 9'),
        ('Comm Tower B (Hind D[efeated])', 'PSG-1 11'),
        ('Comm Tower B (Hind D[efeated])', 'PSG-1 12'),
        ('Comm Tower B (Hind D[efeated])', 'PSG-1 13'),
        ('Comm Tower B (Hind D[efeated])', 'BOSS: Stealth Camouflaged Genome Soldiers'),
        ('Comm Tower B Roof', 'Ration 31'),
        ('Comm Tower B Roof', 'Stinger 9'),
        ('Comm Tower B Roof', 'BOSS: A Hind D?'),
        ('Snow Field', 'PSG-1 14'),
        ('Snow Field', 'PSG-1 15'),
        ('Snow Field', 'Ration 32'),
        ('Snow Field', 'BOSS: Sniper Wolf II'),
        ('Snow Field (sans Wolf)', 'Cardboard Box C'),
        ('Snow Field (sans Wolf)', 'Ration 33'),
        ('Snow Field (sans Wolf)', 'Ration 34'),
        ('Snow Field (sans Wolf)', 'Ration 35'),
        ('Snow Field (sans Wolf)', 'Diazepam 3'),
        ('Snow Field (sans Wolf)', 'SOCOM 32'),
        ('Snow Field (sans Wolf)', 'SOCOM 33'),
        ('Snow Field (sans Wolf)', 'SOCOM 34'),
        ('Snow Field (sans Wolf)', 'FA-MAS 37'),
        ('Snow Field (sans Wolf)', 'FA-MAS 38'),
        ('Snow Field (sans Wolf)', 'FA-MAS 39'),
        ('Snow Field (sans Wolf)', 'Grenade 10'),
        ('Snow Field (sans Wolf)', 'Grenade 11'),
        ('Snow Field (sans Wolf)', 'Stun Grenade 7'),
        ('Snow Field (sans Wolf)', 'Chaff Grenade 10'),
        ('Snow Field (sans Wolf)', 'Chaff Grenade 11'),
        ('Snow Field (sans Wolf)', 'Claymore 4'),
        ('Snow Field (sans Wolf)', 'Claymore 5'),
        ('Snow Field (sans Wolf)', 'Claymore 6'),
        ('Snow Field (sans Wolf)', 'Claymore 7'),
        ('Snow Field (sans Wolf)', 'Claymore 8'),
        ('Snow Field (sans Wolf)', 'Stinger 10'),
        ('Snow Field (sans Wolf)', 'Stinger 11'),
        ('Snow Field (sans Wolf)', 'Stinger 12'),
        ('Snow Field (sans Wolf)', 'Stinger 13'),
        ('Snow Field (sans Wolf)', 'Nikita 8'),
        ('Snow Field (sans Wolf)', 'Nikita 9'),
        ('Snow Field (sans Wolf)', 'Nikita 10'),
        ('Snow Field (sans Wolf)', 'Nikita 11'),
        ('Snow Field (sans Wolf)', 'PSG-1 16'),
        ('Snow Field (sans Wolf)', 'PSG-1 17'),
        ('Blast Furnace', 'Ration 36'),
        ('Blast Furnace', 'Ration 37'),
        ('Blast Furnace', 'SOCOM 35'),
        ('Blast Furnace', 'SOCOM 36'),
        ('Blast Furnace', 'SOCOM 37'),
        ('Blast Furnace', 'FA-MAS 40'),
        ('Blast Furnace', 'C4 6'),
        ('Blast Furnace', 'Stun Grenade 8'),
        ('Blast Furnace', 'Stun Grenade 9'),
        ('Blast Furnace', 'Nikita 12'),
        ('Blast Furnace', 'Nikita 13'),
        ('Blast Furnace', 'PSG-1 18'),
        ('Blast Furnace', 'PSG-1 19'),
        ('Blast Furnace', 'Stinger 14'),
        ('Blast Furnace', 'Stinger 15'),
        ('Blast Furnace', 'Chaff Grenade 12'),
        ('Blast Furnace', 'Body Armor'),
        ('Cargo Elevator', 'Ration 38'),
        ('Cargo Elevator', 'Ration 48'),
        ('Cargo Elevator', 'Nikita 16'),
        ('Cargo Elevator', 'Nikita 17'),
        ('Cargo Elevator', 'C4 7'),
        ('Cargo Elevator', 'FA-MAS 41'),
        ('Cargo Elevator', 'FA-MAS 42'),
        ('Cargo Elevator', 'FA-MAS 43'),
        ('Cargo Elevator', 'FA-MAS 44'),
        ('Cargo Elevator', 'FA-MAS 45'),
        ('Cargo Elevator', 'FA-MAS 46'),
        ('Cargo Elevator', 'SOCOM 38'),
        ('Cargo Elevator', 'SOCOM 39'),
        ('Cargo Elevator', 'SOCOM 40'),
        ('Cargo Elevator', 'Claymore 9'),
        ('Cargo Elevator', 'Claymore 10'),
        ('Cargo Elevator', 'Claymore 11'),
        ('Cargo Elevator', 'Claymore 12'),
        ('Cargo Elevator', 'Claymore 13'),
        ('Cargo Elevator', 'BOSS: Black-outfitted Genome Soldiers II'),
        ('Warehouse', 'Ration 39'),
        ('Warehouse', 'Stinger 16'),
        ('Warehouse', 'Stinger 17'),
        ('Warehouse', 'Nikita 14'),
        ('Warehouse', 'Nikita 15'),
        ('Warehouse', 'BOSS: Vulcan Raven'),
        ('Warehouse', 'Key Card Level 7'),
        ('Warehouse North', 'Ration 40'),
        ('Warehouse North', 'Chaff Grenade 13'),
        ('Warehouse North', 'Stinger 18'),
        ('Warehouse North', 'Stinger 19'),
        ('Warehouse North', 'Stinger 20'),
        ('Warehouse North', 'Stinger 21'),
        ('Underground Base', 'Ration 41'),
        ('Underground Base', 'Ration 42'),
        ('Underground Base', 'SOCOM 41'),
        ('Underground Base', 'SOCOM 42'),
        ('Underground Base', 'SOCOM 43'),
        ('Underground Base', 'FA-MAS 47'),
        ('Underground Base', 'FA-MAS 48'),
        ('Underground Base', 'FA-MAS 49'),
        ('Underground Base', 'FA-MAS 50'),
        ('Underground Base', 'FA-MAS 51'),
        ('Underground Base', 'Chaff Grenade 14'),
        ('Underground Base', 'Chaff Grenade 15'),
        ('Underground Base', 'Chaff Grenade 16'),
        ('Underground Base', 'Stinger 22'),
        ('Underground Base', 'Stinger 23'),
        ('Command Room', 'Ration 43'),
        ('Command Room', 'Ration 44'),
        ('Metal Gear REX', 'Ration 45'),
        ('Metal Gear REX', 'Ration 46'),
        ('Metal Gear REX', 'Stinger 24'),
        ('Metal Gear REX', 'Stinger 25'),
        ('Metal Gear REX', 'Stinger 26'),
        ('Metal Gear REX', 'Chaff Grenade 17'),
        ('Metal Gear REX', 'Stun Grenade 10'),
        ('Metal Gear REX', 'BOSS: Metal Gear REX'),
        ('Metal Gear REX', 'BOSS: Liquid Snake'),
        ('Escape Route', 'Ration 47'),
        ('Escape Route', 'The Best is Yet to Come'),
    ]

# Without doing a complete rewrite of how this apworld was handled in the client (which would have been a nightmare)
# Instead I'm opting to use another list to pair old names up with the newer ones.
# A location in this list is stored as:
# (region name shown in AP, location name shown in AP, old location name from Locations.py, old region name)
LocationNamePair = tuple[str, str, str, str]


def get_numbered_pickup_type(location_name: str) -> str | None:
    """Return the pickup type for names like 'Ration 15' or 'SOCOM 3'."""
    for pickup_type in REPEATED_LOCATION_PREFIXES:
        prefix = f"{pickup_type} "

        if not location_name.startswith(prefix):
            continue

        number_text = location_name[len(prefix):]
        if number_text.isdigit():
            return pickup_type

    return None


def build_region_location_pairs() -> list[LocationNamePair]:
    pickup_counts: dict[tuple[str, str], int] = {}
    renamed_locations: list[LocationNamePair] = []

    for old_region_name, old_location_name in ORIGINAL_LOCATION_PAIRS:
        ap_region_name = get_location_region_name(old_region_name)
        ap_location_name = old_location_name

        pickup_type = get_numbered_pickup_type(old_location_name)
        if pickup_type is not None:
            count_key = (ap_region_name, pickup_type)
            pickup_counts[count_key] = pickup_counts.get(count_key, 0) + 1
            ap_location_name = f"{pickup_type} {pickup_counts[count_key]}"

        renamed_locations.append((ap_region_name, ap_location_name, old_location_name, old_region_name))

    return renamed_locations


REGION_LOCATION_PAIRS = build_region_location_pairs()

FULL_LOCATION_NAME_TO_ID: dict[str, int] = {}
for ap_region_name, ap_location_name, old_location_name, _ in REGION_LOCATION_PAIRS:
    if old_location_name not in Locations.location_name_to_id_table:
        continue

    ap_full_name = full_location_name(ap_region_name, ap_location_name)
    FULL_LOCATION_NAME_TO_ID[ap_full_name] = Locations.location_name_to_id_table[old_location_name]


def get_ap_location_name(region_name: str, location_name: str) -> str:
    ap_region_name = get_location_region_name(region_name)

    for pair_region_name, ap_location_name, old_location_name, old_region_name in REGION_LOCATION_PAIRS:
        if pair_region_name != ap_region_name:
            continue
        if old_region_name != region_name:
            continue
        if old_location_name == location_name:
            return ap_location_name

    return location_name


def build_location_name_to_id_table() -> dict[str, int]:
    return dict(FULL_LOCATION_NAME_TO_ID)


def remember_location_name(world: "MGSWorld", short_name: str, full_name: str) -> None:
    world.short_location_name_to_full.setdefault(short_name, full_name)

def make_location(world: "MGSWorld", region: Region, location_name: str) -> Locations.MGSLocation:
    ap_region_name = get_location_region_name(region.name)
    ap_location_name = get_ap_location_name(region.name, location_name)
    ap_full_name = full_location_name(ap_region_name, ap_location_name)

    remember_location_name(world, ap_location_name, ap_full_name)
    remember_location_name(world, location_name, ap_full_name)

    return Locations.MGSLocation(world.player, ap_full_name, FULL_LOCATION_NAME_TO_ID[ap_full_name], region)


# This tells the Archipelago run generator where location checks can be found so it can generate paths to them
# Paths can have rules for crossing them, added by the Rules.py file
def create_regions(world: "MGSWorld"):
    player = world.player
    multiworld = world.multiworld

    # default Archipelago stating region
    menu = Region('Menu', player, multiworld)
    multiworld.regions.append(menu)

    docks = Region('Docks', player, multiworld)
    docks.locations += [
        make_location(world, docks, 'Ration 1'),
        make_location(world, docks, 'Ration 2'),
        make_location(world, docks, 'Ration 3'),
        ]
    multiworld.regions.append(docks)
    menu.connect(docks)

    heliport = Region('Heliport', player, multiworld)
    heliport.locations += [
        make_location(world, heliport, 'Chaff Grenade 1'),
        make_location(world, heliport, 'Stun Grenade 1'),
        make_location(world, heliport, 'SOCOM 1'),
        make_location(world, heliport, 'Ration 4'),
        ]
    multiworld.regions.append(heliport)
    docks.connect(heliport)

    tank_hangar = Region('Tank Hangar', player, multiworld)
    tank_hangar.locations += [
        make_location(world, tank_hangar, 'Chaff Grenade 2'),
        make_location(world, tank_hangar, 'Thermal Goggles'),
        make_location(world, tank_hangar, 'SOCOM 2'),
        make_location(world, tank_hangar, 'Ration 5'),
    ]
    multiworld.regions.append(tank_hangar)
    heliport.connect(tank_hangar)

    tank_hangar_lvl1 = Region('Tank Hangar_lvl1', player, multiworld)
    tank_hangar_lvl1.locations += [
        make_location(world, tank_hangar_lvl1, 'Suppressor'),
        make_location(world, tank_hangar_lvl1, 'Cardboard Box A'),
    ]
    multiworld.regions.append(tank_hangar_lvl1)
    tank_hangar.connect(tank_hangar_lvl1, 'hangar_to_hangar_lvl1')

    tank_hangar_lvl2 = Region('Tank Hangar_lvl2', player, multiworld)
    tank_hangar_lvl2.locations += [
        make_location(world, tank_hangar_lvl2, 'Mine Detector'),
    ]
    multiworld.regions.append(tank_hangar_lvl2)
    tank_hangar.connect(tank_hangar_lvl2, 'hangar_to_hangar_lvl2')

    armory = Region('Armory', player, multiworld)
    armory.locations += [
        make_location(world, armory, 'SOCOM 3'),
        make_location(world, armory, 'SOCOM 4'),
        ]
    multiworld.regions.append(armory)
    tank_hangar.connect(armory)

    armory_lvl1 = Region('Armory_lvl1', player, multiworld)
    armory_lvl1.locations += [
        make_location(world, armory_lvl1, 'C4 1'),
        make_location(world, armory_lvl1, 'C4 2'),
        make_location(world, armory_lvl1, 'Grenade 1'),
        make_location(world, armory_lvl1, 'Grenade 2'),
        ]
    multiworld.regions.append(armory_lvl1)
    armory.connect(armory_lvl1, 'armory_to_armory_lvl1')

    armory_lvl2 = Region('Armory_lvl2', player, multiworld)
    armory_lvl2.locations += [
        make_location(world, armory_lvl2, 'FA-MAS 1'),
        make_location(world, armory_lvl2, 'FA-MAS 2'),
        make_location(world, armory_lvl2, 'FA-MAS 3'),
        ]
    multiworld.regions.append(armory_lvl2)
    armory.connect(armory_lvl2, 'armory_to_armory_lvl2')

    armory_lvl3 = Region('Armory_lvl3', player, multiworld)
    armory_lvl3.locations += [
        make_location(world, armory_lvl3, 'Nikita 1'),
        make_location(world, armory_lvl3, 'Nikita 2'),
        ]
    multiworld.regions.append(armory_lvl3)
    armory.connect(armory_lvl3, 'armory_to_armory_lvl3')

    armory_lvl5 = Region('Armory_lvl5', player, multiworld)
    armory_lvl5.locations += [
        make_location(world, armory_lvl5, 'PSG-1 1'),
        make_location(world, armory_lvl5, 'PSG-1 2'),
        make_location(world, armory_lvl5, 'PSG-1 3'),
        ]
    multiworld.regions.append(armory_lvl5)
    armory.connect(armory_lvl5, 'armory_to_armory_lvl5')

    cell = Region('Cell', player, multiworld)
    cell.locations += [
        make_location(world, cell, 'Key Card Level 1'),
        make_location(world, cell, 'SOCOM 5'),
        make_location(world, cell, 'SOCOM 6'),
        make_location(world, cell, 'SOCOM 7'),
        make_location(world, cell, 'SOCOM 8'),
        make_location(world, cell, 'SOCOM 9'),
        make_location(world, cell, 'SOCOM 10'),
        make_location(world, cell, 'Ration 6'),
        make_location(world, cell, 'Ration 7'),
        make_location(world, cell, 'Ration 8'),
        make_location(world, cell, 'Ration 9'),
        make_location(world, cell, 'BOSS: Heavily Armed Genome Soldiers'),
        ]
    multiworld.regions.append(cell)
    tank_hangar.connect(cell, 'hangar_to_cell')
    armory.connect(cell, 'armory_to_cell')
    cell.connect(armory)

    armory_sth = Region('Armory Sth', player, multiworld)
    armory_sth.locations += [
        make_location(world, armory_sth, 'SOCOM 11'),
        make_location(world, armory_sth, 'SOCOM 12'),
        make_location(world, armory_sth, 'SOCOM 13'),
        make_location(world, armory_sth, 'Key Card Level 2'),
        make_location(world, armory_sth, 'BOSS: Revolver Ocelot'),
        ]
    multiworld.regions.append(armory_sth)
    armory.connect(armory_sth, 'armory_to_armory_sth')

    armory_sth_c4 = Region('Armory Sth_C4', player, multiworld)
    armory_sth_c4.locations += [
        make_location(world, armory_sth_c4, 'Ration 10'),
        make_location(world, armory_sth_c4, 'C4 3'),
        ]
    multiworld.regions.append(armory_sth_c4)
    armory.connect(armory_sth_c4, 'armory_to_armory_sth_c4')

    armory_sth_c4_lvl4 = Region('Armory Sth_C4_lvl4', player, multiworld)
    armory_sth_c4_lvl4.locations += [
        make_location(world, armory_sth_c4_lvl4, 'Stinger 1'),
        make_location(world, armory_sth_c4_lvl4, 'Camera'),
        ]
    multiworld.regions.append(armory_sth_c4_lvl4)
    armory_sth_c4.connect(armory_sth_c4_lvl4, 'armory_sth_c4_to_armory_sth_c4_lvl4')

    armory_sth_c4_lvl6 = Region('Armory Sth_C4_lvl6', player, multiworld)
    armory_sth_c4_lvl6.locations += [
        make_location(world, armory_sth_c4_lvl6, 'Stinger 2'),
        make_location(world, armory_sth_c4_lvl6, 'Stinger 3'),
        make_location(world, armory_sth_c4_lvl6, 'Stinger 4'),
        make_location(world, armory_sth_c4_lvl6, 'Stun Grenade 2'),
        make_location(world, armory_sth_c4_lvl6, 'Chaff Grenade 3'),
        ]
    multiworld.regions.append(armory_sth_c4_lvl6)
    armory_sth_c4.connect(armory_sth_c4_lvl6, 'armory_sth_c4_to_armory_sth_c4_lvl6')

    canyon = Region('Canyon', player, multiworld)
    canyon.locations += [
        make_location(world, canyon, 'Ration 11'),
        make_location(world, canyon, 'Grenade 3'),
        make_location(world, canyon, 'Grenade 4'),
        make_location(world, canyon, 'Grenade 5'),
        make_location(world, canyon, 'Chaff Grenade 4'),
        make_location(world, canyon, 'Claymore 1'),
        make_location(world, canyon, 'Claymore 2'),
        make_location(world, canyon, 'Claymore 3'),
        make_location(world, canyon, 'BOSS: M1 Tank'),
        make_location(world, canyon, 'Key Card Level 3'),
        ]
    multiworld.regions.append(canyon)
    tank_hangar.connect(canyon, 'hangar_to_canyon')

    nuke_building_1 = Region('Nuke Building 1', player, multiworld)
    nuke_building_1.locations += [
        make_location(world, nuke_building_1, 'Ration 12'),
        make_location(world, nuke_building_1, 'Grenade 6'),
        make_location(world, nuke_building_1, 'Chaff Grenade 5'),
        make_location(world, nuke_building_1, 'FA-MAS 4'),
        make_location(world, nuke_building_1, 'FA-MAS 5'),
        make_location(world, nuke_building_1, 'SOCOM 14'),
        ]
    multiworld.regions.append(nuke_building_1)
    canyon.connect(nuke_building_1, 'canyon_to_nuke_building_1')

    nuke_building_B1 = Region('Nuke Building B1', player, multiworld)
    nuke_building_B1.locations += [
        make_location(world, nuke_building_B1, 'Stun Grenade 3'),
        make_location(world, nuke_building_B1, 'Nikita 3'),
        make_location(world, nuke_building_B1, 'Nikita 4'),
        make_location(world, nuke_building_B1, 'Nikita 5'),
        make_location(world, nuke_building_B1, 'SOCOM 15'),
        make_location(world, nuke_building_B1, 'FA-MAS 6'),
        ]
    multiworld.regions.append(nuke_building_B1)
    nuke_building_1.connect(nuke_building_B1)

    nuke_building_B1_lvl4 = Region('Nuke Building B1 lvl4', player, multiworld)
    nuke_building_B1_lvl4.locations += [
        make_location(world, nuke_building_B1_lvl4, 'Cardboard Box B'),
        make_location(world, nuke_building_B1_lvl4, 'SOCOM 16'),
        make_location(world, nuke_building_B1_lvl4, 'FA-MAS 7'),
        make_location(world, nuke_building_B1_lvl4, 'Ration 13'),
        make_location(world, nuke_building_B1_lvl4, 'Pal Key'),
        make_location(world, nuke_building_B1_lvl4, 'Key Card Level 5'),
        ]
    multiworld.regions.append(nuke_building_B1_lvl4)
    nuke_building_B1.connect(nuke_building_B1_lvl4, 'nuke_building_b1_to_nuke_bulding_b1_lvl4')

    nuke_building_B1_lvl5 = Region('Nuke Building B1 lvl5', player, multiworld)
    nuke_building_B1_lvl5.locations += [
        make_location(world, nuke_building_B1_lvl5, 'Diazepam 1'),
        make_location(world, nuke_building_B1_lvl5, 'FA-MAS 8'),
        make_location(world, nuke_building_B1_lvl5, 'FA-MAS 9'),
        make_location(world, nuke_building_B1_lvl5, 'FA-MAS 10'),
        ]
    multiworld.regions.append(nuke_building_B1_lvl5)
    nuke_building_B1.connect(nuke_building_B1_lvl5, 'nuke_building_b1_to_nuke_bulding_b1_lvl5')

    nuke_building_B2 = Region('Nuke Building B2', player, multiworld)
    nuke_building_B2.locations += [
        make_location(world, nuke_building_B2, 'Ration 14'),
        make_location(world, nuke_building_B2, 'Ration 15'),
        make_location(world, nuke_building_B2, 'Gas Mask'),
        make_location(world, nuke_building_B2, 'C4 4'),
        make_location(world, nuke_building_B2, 'Grenade 7'),
        make_location(world, nuke_building_B2, 'Grenade 8'),
        make_location(world, nuke_building_B2, 'Chaff Grenade 6'),
        make_location(world, nuke_building_B2, 'FA-MAS 11'),
        make_location(world, nuke_building_B2, 'Nikita 6'),
        make_location(world, nuke_building_B2, 'Nikita 7'),
        ]
    multiworld.regions.append(nuke_building_B2)
    nuke_building_1.connect(nuke_building_B2, 'nuke_building_1_to_nuke_building_b2')
    nuke_building_B1.connect(nuke_building_B2, 'nuke_building_b1_to_nuke_building_b2')

    nuke_building_B2_lvl4 = Region('Nuke Building B2 lvl4', player, multiworld)
    nuke_building_B2_lvl4.locations += [
        make_location(world, nuke_building_B2_lvl4, 'Stun Grenade 4'),
        make_location(world, nuke_building_B2_lvl4, 'Stun Grenade 5'),
        make_location(world, nuke_building_B2_lvl4, 'Night Vision Goggles'),
        ]
    multiworld.regions.append(nuke_building_B2_lvl4)
    nuke_building_B2.connect(nuke_building_B2_lvl4, 'nuke_bulding_b2_to_nuke_building_b2_lvl4')

    nuke_building_B2_lvl6 = Region('Nuke Building B2 lvl6', player, multiworld)
    nuke_building_B2_lvl6.locations += [
        ]
    multiworld.regions.append(nuke_building_B2_lvl6)
    nuke_building_B2.connect(nuke_building_B2_lvl6, 'nuke_bulding_b2_to_nuke_building_b2_lvl6')

    lab = Region('Lab', player, multiworld)
    lab.locations += [
        make_location(world, lab, 'Ration 16'),
        make_location(world, lab, 'SOCOM 17'),
        make_location(world, lab, 'FA-MAS 12'),
        make_location(world, lab, 'FA-MAS 13'),
        make_location(world, lab, 'Chaff Grenade 7'),
        make_location(world, lab, 'Key Card Level 4'),
        make_location(world, lab, 'BOSS: Gray Fox'),
        ]
    multiworld.regions.append(lab)
    nuke_building_B2.connect(lab)

    commander_room = Region('Commander Room', player, multiworld)
    commander_room.locations += [
        make_location(world, commander_room, 'Ration 17'),
        make_location(world, commander_room, 'Ration 18'),
        make_location(world, commander_room, 'SOCOM 18'),
        make_location(world, commander_room, 'SOCOM 19'),
        make_location(world, commander_room, 'FA-MAS 14'),
        make_location(world, commander_room, 'FA-MAS 15'),
        make_location(world, commander_room, 'FA-MAS 16'),
        make_location(world, commander_room, 'BOSS: Psycho Mantis'),
        ]
    multiworld.regions.append(commander_room)
    nuke_building_B1.connect(commander_room, 'nuke_building_b1_to_commander_room')

    cave = Region('Cave', player, multiworld)
    cave.locations += [
        make_location(world, cave, 'Ration 19'),
        make_location(world, cave, 'Ration 20'),
        make_location(world, cave, 'Ration 21'),
        make_location(world, cave, 'SOCOM 20'),
        make_location(world, cave, 'FA-MAS 17'),
        make_location(world, cave, 'FA-MAS 18'),
        make_location(world, cave, 'Diazepam 2'),
        make_location(world, cave, 'PSG-1 4'),
        make_location(world, cave, 'PSG-1 5'),
        make_location(world, cave, 'PSG-1 6'),
        ]
    multiworld.regions.append(cave)
    commander_room.connect(cave, 'commander_room_to_cave')

    underground_passage = Region('Underground Passage', player, multiworld)
    underground_passage.locations += [
        make_location(world, underground_passage, 'Ration 22'),
        make_location(world, underground_passage, 'SOCOM 21'),
        make_location(world, underground_passage, 'FA-MAS 19'),
        make_location(world, underground_passage, 'PSG-1 7'),
        make_location(world, underground_passage, 'PSG-1 8'),
        make_location(world, underground_passage, 'PSG-1 9'),
        make_location(world, underground_passage, 'PSG-1 10'),
        make_location(world, underground_passage, 'BOSS: Sniper Wolf I'),
        ]
    multiworld.regions.append(underground_passage)
    cave.connect(underground_passage, 'cave_to_underground_passage')

    medi_room = Region('Medi Room', player, multiworld)
    medi_room.locations += [
        make_location(world, medi_room, 'Ration 23'),
        make_location(world, medi_room, 'Handkerchief'),
        # make_location(world, medi_room, 'Ketchup'),
        make_location(world, medi_room, 'Key Card Level 6'),
        # make_location(world, medi_room, 'Time Bomb 1'),
        ]
    multiworld.regions.append(medi_room)
    underground_passage.connect(medi_room, 'underground_passage_to_medi_room')

    comm_tower_a = Region('Comm Tower A', player, multiworld)
    comm_tower_a.locations += [
        make_location(world, comm_tower_a, 'Ration 24'),
        make_location(world, comm_tower_a, 'Ration 25'),
        make_location(world, comm_tower_a, 'Ration 26'),
        make_location(world, comm_tower_a, 'SOCOM 22'),
        make_location(world, comm_tower_a, 'SOCOM 23'),
        make_location(world, comm_tower_a, 'SOCOM 24'),
        make_location(world, comm_tower_a, 'SOCOM 25'),
        make_location(world, comm_tower_a, 'SOCOM 26'),
        make_location(world, comm_tower_a, 'SOCOM 27'),
        make_location(world, comm_tower_a, 'SOCOM 28'),
        make_location(world, comm_tower_a, 'FA-MAS 20'),
        make_location(world, comm_tower_a, 'FA-MAS 21'),
        make_location(world, comm_tower_a, 'FA-MAS 22'),
        make_location(world, comm_tower_a, 'FA-MAS 23'),
        make_location(world, comm_tower_a, 'FA-MAS 24'),
        make_location(world, comm_tower_a, 'FA-MAS 25'),
        make_location(world, comm_tower_a, 'FA-MAS 26'),
        make_location(world, comm_tower_a, 'FA-MAS 27'),
        make_location(world, comm_tower_a, 'FA-MAS 28'),
        make_location(world, comm_tower_a, 'Stun Grenade 6'),
        make_location(world, comm_tower_a, 'Rope'),
        make_location(world, comm_tower_a, 'BOSS: Black-outfitted Genome Soldiers I'),
        ]
    multiworld.regions.append(comm_tower_a)
    medi_room.connect(comm_tower_a, 'medi_room_to_comm_tower_a')

    walkway = Region('Walkway', player, multiworld)
    walkway.locations += [
        make_location(world, walkway, 'Ration 27'),
        make_location(world, walkway, 'Ration 28'),
        make_location(world, walkway, 'C4 5'),
        make_location(world, walkway, 'Stinger 5'),
        ]
    multiworld.regions.append(walkway)
    comm_tower_a.connect(walkway, 'comm_tower_a_to_walkway')

    comm_tower_b = Region('Comm Tower B', player, multiworld)
    comm_tower_b.locations += [
        make_location(world, comm_tower_b, 'Ration 29'),
        make_location(world, comm_tower_b, 'SOCOM 29'),
        make_location(world, comm_tower_b, 'FA-MAS 29'),
        make_location(world, comm_tower_b, 'FA-MAS 30'),
        make_location(world, comm_tower_b, 'Grenade 9'),
        make_location(world, comm_tower_b, 'Chaff Grenade 8'),
        make_location(world, comm_tower_b, 'Stinger 6'),
        make_location(world, comm_tower_b, 'Stinger 7'),
        make_location(world, comm_tower_b, 'Stinger 8'),
        ]
    multiworld.regions.append(comm_tower_b)
    walkway.connect(comm_tower_b)

    comm_tower_b_after_hind = Region('Comm Tower B (Hind D[efeated])', player, multiworld)
    comm_tower_b_after_hind.locations += [
        make_location(world, comm_tower_b_after_hind, 'Ration 30'),
        make_location(world, comm_tower_b_after_hind, 'Ration 49'),
        make_location(world, comm_tower_b_after_hind, 'SOCOM 30'),
        make_location(world, comm_tower_b_after_hind, 'SOCOM 31'),
        make_location(world, comm_tower_b_after_hind, 'FA-MAS 31'),
        make_location(world, comm_tower_b_after_hind, 'FA-MAS 32'),
        make_location(world, comm_tower_b_after_hind, 'FA-MAS 33'),
        make_location(world, comm_tower_b_after_hind, 'FA-MAS 34'),
        make_location(world, comm_tower_b_after_hind, 'FA-MAS 35'),
        make_location(world, comm_tower_b_after_hind, 'FA-MAS 36'),
        make_location(world, comm_tower_b_after_hind, 'Chaff Grenade 9'),
        make_location(world, comm_tower_b_after_hind, 'PSG-1 11'),
        make_location(world, comm_tower_b_after_hind, 'PSG-1 12'),
        make_location(world, comm_tower_b_after_hind, 'PSG-1 13'),
        make_location(world, comm_tower_b_after_hind, 'BOSS: Stealth Camouflaged Genome Soldiers'),
        ]
    multiworld.regions.append(comm_tower_b_after_hind)
    comm_tower_b.connect(comm_tower_b_after_hind, 'comm_tower_b_to_comm_tower_b_after_hind')

    comm_tower_b_roof = Region('Comm Tower B Roof', player, multiworld)
    comm_tower_b_roof.locations += [
        make_location(world, comm_tower_b_roof, 'Ration 31'),
        make_location(world, comm_tower_b_roof, 'Stinger 9'),
        make_location(world, comm_tower_b_roof, 'BOSS: A Hind D?'),
        ]
    multiworld.regions.append(comm_tower_b_roof)
    comm_tower_b.connect(comm_tower_b_roof, 'comm_tower_b_to_comm_tower_b_roof')

    snowfield = Region('Snow Field', player, multiworld)
    snowfield.locations += [
        make_location(world, snowfield, 'PSG-1 14'),
        make_location(world, snowfield, 'PSG-1 15'),
        make_location(world, snowfield, 'Ration 32'),
        make_location(world, snowfield, 'BOSS: Sniper Wolf II'),
        ]
    multiworld.regions.append(snowfield)
    comm_tower_b.connect(snowfield, 'comm_tower_b_to_snowfield')

    snowfield_sans_wolf = Region('Snow Field (sans Wolf)', player, multiworld)
    snowfield_sans_wolf.locations += [
        make_location(world, snowfield_sans_wolf, 'Cardboard Box C'),
        make_location(world, snowfield_sans_wolf, 'Ration 33'),
        make_location(world, snowfield_sans_wolf, 'Ration 34'),
        make_location(world, snowfield_sans_wolf, 'Ration 35'),
        make_location(world, snowfield_sans_wolf, 'Diazepam 3'),
        make_location(world, snowfield_sans_wolf, 'SOCOM 32'),
        make_location(world, snowfield_sans_wolf, 'SOCOM 33'),
        make_location(world, snowfield_sans_wolf, 'SOCOM 34'),
        make_location(world, snowfield_sans_wolf, 'FA-MAS 37'),
        make_location(world, snowfield_sans_wolf, 'FA-MAS 38'),
        make_location(world, snowfield_sans_wolf, 'FA-MAS 39'),
        make_location(world, snowfield_sans_wolf, 'Grenade 10'),
        make_location(world, snowfield_sans_wolf, 'Grenade 11'),
        make_location(world, snowfield_sans_wolf, 'Stun Grenade 7'),
        make_location(world, snowfield_sans_wolf, 'Chaff Grenade 10'),
        make_location(world, snowfield_sans_wolf, 'Chaff Grenade 11'),
        make_location(world, snowfield_sans_wolf, 'Claymore 4'),
        make_location(world, snowfield_sans_wolf, 'Claymore 5'),
        make_location(world, snowfield_sans_wolf, 'Claymore 6'),
        make_location(world, snowfield_sans_wolf, 'Claymore 7'),
        make_location(world, snowfield_sans_wolf, 'Claymore 8'),
        make_location(world, snowfield_sans_wolf, 'Stinger 10'),
        make_location(world, snowfield_sans_wolf, 'Stinger 11'),
        make_location(world, snowfield_sans_wolf, 'Stinger 12'),
        make_location(world, snowfield_sans_wolf, 'Stinger 13'),
        make_location(world, snowfield_sans_wolf, 'Nikita 8'),
        make_location(world, snowfield_sans_wolf, 'Nikita 9'),
        make_location(world, snowfield_sans_wolf, 'Nikita 10'),
        make_location(world, snowfield_sans_wolf, 'Nikita 11'),
        make_location(world, snowfield_sans_wolf, 'PSG-1 16'),
        make_location(world, snowfield_sans_wolf, 'PSG-1 17'),
        ]
    multiworld.regions.append(snowfield_sans_wolf)
    snowfield.connect(snowfield_sans_wolf, 'snowfield_to_snowfield_sans_wolf')

    blast_furnace = Region('Blast Furnace', player, multiworld)
    blast_furnace.locations += [
        make_location(world, blast_furnace, 'Ration 36'),
        make_location(world, blast_furnace, 'Ration 37'),
        make_location(world, blast_furnace, 'SOCOM 35'),
        make_location(world, blast_furnace, 'SOCOM 36'),
        make_location(world, blast_furnace, 'SOCOM 37'),
        make_location(world, blast_furnace, 'FA-MAS 40'),
        make_location(world, blast_furnace, 'C4 6'),
        make_location(world, blast_furnace, 'Stun Grenade 8'),
        make_location(world, blast_furnace, 'Stun Grenade 9'),
        make_location(world, blast_furnace, 'Nikita 12'),
        make_location(world, blast_furnace, 'Nikita 13'),
        make_location(world, blast_furnace, 'PSG-1 18'),
        make_location(world, blast_furnace, 'PSG-1 19'),
        make_location(world, blast_furnace, 'Stinger 14'),
        make_location(world, blast_furnace, 'Stinger 15'),
        make_location(world, blast_furnace, 'Chaff Grenade 12'),
        make_location(world, blast_furnace, 'Body Armor'),
        ]
    multiworld.regions.append(blast_furnace)
    snowfield_sans_wolf.connect(blast_furnace)

    cargo_elevator = Region('Cargo Elevator', player, multiworld)
    cargo_elevator.locations += [
        make_location(world, cargo_elevator, 'Ration 38'),
        make_location(world, cargo_elevator, 'Ration 48'),
        make_location(world, cargo_elevator, 'Nikita 16'),
        make_location(world, cargo_elevator, 'Nikita 17'),
        make_location(world, cargo_elevator, 'C4 7'),
        make_location(world, cargo_elevator, 'FA-MAS 41'),
        make_location(world, cargo_elevator, 'FA-MAS 42'),
        make_location(world, cargo_elevator, 'FA-MAS 43'),
        make_location(world, cargo_elevator, 'FA-MAS 44'),
        make_location(world, cargo_elevator, 'FA-MAS 45'),
        make_location(world, cargo_elevator, 'FA-MAS 46'),
        make_location(world, cargo_elevator, 'SOCOM 38'),
        make_location(world, cargo_elevator, 'SOCOM 39'),
        make_location(world, cargo_elevator, 'SOCOM 40'),
        make_location(world, cargo_elevator, 'Claymore 9'),
        make_location(world, cargo_elevator, 'Claymore 10'),
        make_location(world, cargo_elevator, 'Claymore 11'),
        make_location(world, cargo_elevator, 'Claymore 12'),
        make_location(world, cargo_elevator, 'Claymore 13'),
        make_location(world, cargo_elevator, 'BOSS: Black-outfitted Genome Soldiers II'),
        ]
    multiworld.regions.append(cargo_elevator)
    blast_furnace.connect(cargo_elevator)

    warehouse = Region('Warehouse', player, multiworld)
    warehouse.locations += [
        make_location(world, warehouse, 'Ration 39'),
        make_location(world, warehouse, 'Stinger 16'),
        make_location(world, warehouse, 'Stinger 17'),
        make_location(world, warehouse, 'Nikita 14'),
        make_location(world, warehouse, 'Nikita 15'),
        make_location(world, warehouse, 'BOSS: Vulcan Raven'),
        make_location(world, warehouse, 'Key Card Level 7'),
        ]
    multiworld.regions.append(warehouse)
    cargo_elevator.connect(warehouse, 'cargo_elevator_to_warehouse')

    warehouse_nt = Region('Warehouse North', player, multiworld)
    warehouse_nt.locations += [
        make_location(world, warehouse_nt, 'Ration 40'),
        make_location(world, warehouse_nt, 'Chaff Grenade 13'),
        make_location(world, warehouse_nt, 'Stinger 18'),
        make_location(world, warehouse_nt, 'Stinger 19'),
        make_location(world, warehouse_nt, 'Stinger 20'),
        make_location(world, warehouse_nt, 'Stinger 21'),
        ]
    multiworld.regions.append(warehouse_nt)
    warehouse.connect(warehouse_nt, 'warehouse_to_warehouse_nt')

    under_ground_base = Region('Underground Base', player, multiworld)
    under_ground_base.locations += [
        make_location(world, under_ground_base, 'Ration 41'),
        make_location(world, under_ground_base, 'Ration 42'),
        make_location(world, under_ground_base, 'SOCOM 41'),
        make_location(world, under_ground_base, 'SOCOM 42'),
        make_location(world, under_ground_base, 'SOCOM 43'),
        make_location(world, under_ground_base, 'FA-MAS 47'),
        make_location(world, under_ground_base, 'FA-MAS 48'),
        make_location(world, under_ground_base, 'FA-MAS 49'),
        make_location(world, under_ground_base, 'FA-MAS 50'),
        make_location(world, under_ground_base, 'FA-MAS 51'),
        make_location(world, under_ground_base, 'Chaff Grenade 14'),
        make_location(world, under_ground_base, 'Chaff Grenade 15'),
        make_location(world, under_ground_base, 'Chaff Grenade 16'),
        make_location(world, under_ground_base, 'Stinger 22'),
        make_location(world, under_ground_base, 'Stinger 23'),
        # make_location(world, under_ground_base, 'Pal Key (Found)'),
        ]
    multiworld.regions.append(under_ground_base)
    warehouse_nt.connect(under_ground_base)

    command_room = Region('Command Room', player, multiworld)
    command_room.locations += [
        make_location(world, command_room, 'Ration 43'),
        make_location(world, command_room, 'Ration 44'),
        ]
    multiworld.regions.append(command_room)
    under_ground_base.connect(command_room, 'underground_base_to_command_room')

    rex_battle = Region('Metal Gear REX', player, multiworld)
    rex_battle.locations += [
        make_location(world, rex_battle, 'Ration 45'),
        make_location(world, rex_battle, 'Ration 46'),
        make_location(world, rex_battle, 'Stinger 24'),
        make_location(world, rex_battle, 'Stinger 25'),
        make_location(world, rex_battle, 'Stinger 26'),
        make_location(world, rex_battle, 'Chaff Grenade 17'),
        make_location(world, rex_battle, 'Stun Grenade 10'),
        make_location(world, rex_battle, 'BOSS: Metal Gear REX'),
        make_location(world, rex_battle, 'BOSS: Liquid Snake'),
        ]
    multiworld.regions.append(rex_battle)
    under_ground_base.connect(rex_battle, 'under_ground_base_to_rex_battle')

    escape_route = Region('Escape Route', player, multiworld)
    escape_route.locations += [
        make_location(world, escape_route, 'Ration 47'),
        make_location(world, escape_route, 'The Best is Yet to Come'),
        ]
    multiworld.regions.append(escape_route)
    rex_battle.connect(escape_route, 'rex_battle_to_escape_route')


    # Addressless events mirror boss reachability for generation and Universal Tracker.
    for boss_name, event_name, item_name in BOSS_ORDER:
        boss_full_name = world.get_full_location_name(boss_name)
        region = next(region for region in multiworld.regions if region.player == player
                      and any(loc.name == boss_full_name for loc in region.locations))
        event = Locations.MGSLocation(player, event_name, None, region)
        region.locations.append(event)
        event.place_locked_item(Items.MGSItems(item_name, ItemClassification.progression, None, player))


BOSS_ORDER = [
    ('BOSS: Heavily Armed Genome Soldiers', 'EVENT: Heavily Armed Genome Soldiers Defeated', 'Heavily Armed Genome Soldiers Fight'),
    ('BOSS: Revolver Ocelot', 'EVENT: Revolver Ocelot Defeated', 'Ocelot Fight'),
    ('BOSS: M1 Tank', 'EVENT: M1 Tank Defeated', 'M1 Tank Fight'),
    ('BOSS: Gray Fox', 'EVENT: Gray Fox Defeated', 'Gray Fox Fight'),
    ('BOSS: Psycho Mantis', 'EVENT: Psycho Mantis Defeated', 'Psycho Mantis Fight'),
    ('BOSS: Sniper Wolf I', 'EVENT: Sniper Wolf I Defeated', 'Sniper Wolf I Fight'),
    ('BOSS: Black-outfitted Genome Soldiers I', 'EVENT: Black-outfitted Genome Soldiers I Defeated', 'Black-outfitted Genome Soldiers I Fight'),
    ('BOSS: A Hind D?', 'EVENT: Hind D Defeated', 'A Hind D[efeated]'),
    ('BOSS: Stealth Camouflaged Genome Soldiers', 'EVENT: Stealth Camouflaged Genome Soldiers Defeated', 'Stealth Camouflaged Genome Soldiers Fight'),
    ('BOSS: Sniper Wolf II', 'EVENT: Sniper Wolf II Defeated', 'Sniper Wolf II Fight'),
    ('BOSS: Black-outfitted Genome Soldiers II', 'EVENT: Black-outfitted Genome Soldiers II Defeated', 'Black-outfitted Genome Soldiers II Fight'),
    ('BOSS: Vulcan Raven', 'EVENT: Vulcan Raven Defeated', 'Vulcan Raven Fight'),
    ('BOSS: Metal Gear REX', 'EVENT: Metal Gear REX Defeated', 'Metal Gear REX Fight'),
    ('BOSS: Liquid Snake', 'EVENT: Liquid Snake Defeated', 'Liquid Snake Fight'),
]
