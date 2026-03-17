from BaseClasses import Region
from . import Locations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import MGSWorld

def full_location_name(region_name: str, location_name: str) -> str:
    return f"{region_name} - {location_name}"

def build_location_name_to_id_table() -> dict[str, int]:
    pairs = [
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
        ('Tank Hangar', 'Suppressor'),
        ('Tank Hangar', 'Cardboard Box A'),
        ('Tank Hangar', 'Mine Detector'),
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
        ('Cell', 'SOCOM 5'),
        ('Cell', 'SOCOM 6'),
        ('Cell', 'SOCOM 7'),
        ('Cell', 'SOCOM 8'),
        ('Cell', 'Ration 6'),
        ('Cell', 'Ration 7'),
        ('Cell', 'Key Card Level 1'),
        ('Cell', 'BOSS: Heavily Armed Genome Soldiers'),
        ('Armory Sth', 'SOCOM 9'),
        ('Armory Sth', 'SOCOM 10'),
        ('Armory Sth', 'SOCOM 11'),
        ('Armory Sth', 'Key Card Level 2'),
        ('Armory Sth', 'BOSS: Revolver Ocelot'),
        ('Canyon', 'Ration 8'),
        ('Canyon', 'Grenade 3'),
        ('Canyon', 'Grenade 10'),
        ('Canyon', 'Grenade 11'),
        ('Canyon', 'Chaff Grenade 3'),
        ('Canyon', 'Claymore 1'),
        ('Canyon', 'Claymore 2'),
        ('Canyon', 'Claymore 3'),
        ('Canyon', 'Key Card Level 3'),
        ('Canyon', 'BOSS: M1 Tank'),
        ('Nuke Building 1', 'Ration 9'),
        ('Nuke Building 1', 'Grenade 4'),
        ('Nuke Building 1', 'Chaff Grenade 4'),
        ('Nuke Building 1', 'FA-MAS 4'),
        ('Nuke Building 1', 'FA-MAS 5'),
        ('Nuke Building 1', 'SOCOM 12'),
        ('Nuke Building B1', 'Ration 10'),
        ('Nuke Building B1', 'Ration 11'),
        ('Nuke Building B1', 'Stun Grenade 2'),
        ('Nuke Building B1', 'Nikita 3'),
        ('Nuke Building B1', 'Nikita 4'),
        ('Nuke Building B1', 'Nikita 5'),
        ('Nuke Building B1', 'SOCOM 13'),
        ('Nuke Building B1', 'FA-MAS 6'),
        ('Nuke Building B1 lvl4', 'Cardboard Box B'),
        ('Nuke Building B1 lvl4', 'SOCOM 14'),
        ('Nuke Building B1 lvl4', 'FA-MAS 7'),
        ('Nuke Building B1 lvl4', 'Pal Key'),
        ('Nuke Building B1 lvl4', 'Key Card Level 5'),
        ('Nuke Building B1 lvl5', 'Diazepam 1'),
        ('Nuke Building B1 lvl5', 'FA-MAS 8'),
        ('Nuke Building B1 lvl5', 'FA-MAS 9'),
        ('Nuke Building B1 lvl5', 'FA-MAS 10'),
        ('Nuke Building B2', 'Ration 12'),
        ('Nuke Building B2', 'Gas Mask'),
        ('Nuke Building B2', 'C4 3'),
        ('Nuke Building B2', 'Grenade 5'),
        ('Nuke Building B2', 'Grenade 6'),
        ('Nuke Building B2', 'Chaff Grenade 5'),
        ('Nuke Building B2', 'FA-MAS 11'),
        ('Nuke Building B2', 'Nikita 6'),
        ('Nuke Building B2', 'Nikita 7'),
        ('Nuke Building B2 lvl4', 'Ration 13'),
        ('Nuke Building B2 lvl4', 'Stun Grenade 3'),
        ('Nuke Building B2 lvl4', 'Stun Grenade 4'),
        ('Nuke Building B2 lvl4', 'Night Vision Goggles'),
        ('Nuke Building B2 lvl6', 'Body Armor'),
        ('Lab', 'Ration 14'),
        ('Lab', 'SOCOM 15'),
        ('Lab', 'FA-MAS 12'),
        ('Lab', 'FA-MAS 13'),
        ('Lab', 'Chaff Grenade 6'),
        ('Lab', 'Key Card Level 4'),
        ('Lab', 'BOSS: Gray Fox'),
        ('Commander Room', 'Ration 15'),
        ('Commander Room', 'Ration 16'),
        ('Commander Room', 'SOCOM 16'),
        ('Commander Room', 'SOCOM 17'),
        ('Commander Room', 'FA-MAS 14'),
        ('Commander Room', 'FA-MAS 15'),
        ('Commander Room', 'FA-MAS 16'),
        ('Commander Room', 'BOSS: Psycho Mantis'),
        ('Cave', 'Ration 17'),
        ('Cave', 'Ration 18'),
        ('Cave', 'Ration 19'),
        ('Cave', 'SOCOM 18'),
        ('Cave', 'SOCOM 19'),
        ('Cave', 'FA-MAS 17'),
        ('Cave', 'FA-MAS 18'),
        ('Cave', 'Diazepam 2'),
        ('Cave', 'PSG-1 3'),
        ('Cave', 'PSG-1 4'),
        ('Cave', 'PSG-1 5'),
        ('Underground Passage', 'Ration 20'),
        ('Underground Passage', 'SOCOM 20'),
        ('Underground Passage', 'FA-MAS 19'),
        ('Underground Passage', 'PSG-1 6'),
        ('Underground Passage', 'PSG-1 7'),
        ('Underground Passage', 'PSG-1 8'),
        ('Underground Passage', 'PSG-1 9'),
        ('Underground Passage', 'BOSS: Sniper Wolf I'),
        ('Medi Room', 'Ration 21'),
        ('Medi Room', 'Ration 22'),
        ('Medi Room', 'Handkerchief'),
        ('Medi Room', 'Ketchup'),
        ('Medi Room', 'Key Card Level 6'),
        ('Medi Room', 'Time Bomb 1'),
        ('Comm Tower A', 'Ration 23'),
        ('Comm Tower A', 'Ration 24'),
        ('Comm Tower A', 'SOCOM 21'),
        ('Comm Tower A', 'SOCOM 22'),
        ('Comm Tower A', 'SOCOM 23'),
        ('Comm Tower A', 'SOCOM 24'),
        ('Comm Tower A', 'SOCOM 25'),
        ('Comm Tower A', 'FA-MAS 20'),
        ('Comm Tower A', 'FA-MAS 21'),
        ('Comm Tower A', 'FA-MAS 22'),
        ('Comm Tower A', 'FA-MAS 23'),
        ('Comm Tower A', 'FA-MAS 24'),
        ('Comm Tower A', 'Stun Grenade 5'),
        ('Comm Tower A', 'Rope'),
        ('Comm Tower A', 'BOSS: Black-outfitted Genome Soldiers I'),
        ('Walkway', 'Ration 25'),
        ('Walkway', 'C4 4'),
        ('Walkway', 'Stinger 1'),
        ('Walkway', 'Stinger 2'),
        ('Comm Tower B', 'Ration 26'),
        ('Comm Tower B', 'SOCOM 26'),
        ('Comm Tower B', 'FA-MAS 25'),
        ('Comm Tower B', 'FA-MAS 26'),
        ('Comm Tower B', 'Grenade 7'),
        ('Comm Tower B', 'Chaff Grenade 7'),
        ('Comm Tower B', 'Stinger 3'),
        ('Comm Tower B', 'Stinger 4'),
        ('Comm Tower B', 'Stinger 5'),
        ('Comm Tower B', 'Ration 27'),
        ('Comm Tower B', 'Ration 28'),
        ('Comm Tower B', 'SOCOM 27'),
        ('Comm Tower B', 'SOCOM 28'),
        ('Comm Tower B', 'FA-MAS 27'),
        ('Comm Tower B', 'FA-MAS 28'),
        ('Comm Tower B', 'FA-MAS 29'),
        ('Comm Tower B', 'FA-MAS 30'),
        ('Comm Tower B (Hind D[efeated])', 'Chaff Grenade 8'),
        ('Comm Tower B (Hind D[efeated])', 'PSG-1 10'),
        ('Comm Tower B (Hind D[efeated])', 'PSG-1 11'),
        ('Comm Tower B (Hind D[efeated])', 'PSG-1 12'),
        ('Comm Tower B (Hind D[efeated])', 'BOSS: Stealth Camouflaged Genome Soldiers'),
        ('Comm Tower B Roof', 'Ration 29'),
        ('Comm Tower B Roof', 'Stinger 6'),
        ('Comm Tower B Roof', 'BOSS: A Hind D?'),
        ('Snow Field', 'PSG-1 13'),
        ('Snow Field', 'PSG-1 14'),
        ('Snow Field', 'Ration 30'),
        ('Snow Field', 'BOSS: Sniper Wolf II'),
        ('Snow Field (sans Wolf)', 'Cardboard Box C'),
        ('Snow Field (sans Wolf)', 'Ration 31'),
        ('Snow Field (sans Wolf)', 'Ration 32'),
        ('Snow Field (sans Wolf)', 'Ration 33'),
        ('Snow Field (sans Wolf)', 'Diazepam 3'),
        ('Snow Field (sans Wolf)', 'SOCOM 29'),
        ('Snow Field (sans Wolf)', 'SOCOM 30'),
        ('Snow Field (sans Wolf)', 'FA-MAS 31'),
        ('Snow Field (sans Wolf)', 'FA-MAS 32'),
        ('Snow Field (sans Wolf)', 'FA-MAS 33'),
        ('Snow Field (sans Wolf)', 'Grenade 8'),
        ('Snow Field (sans Wolf)', 'Grenade 9'),
        ('Snow Field (sans Wolf)', 'Stun Grenade 6'),
        ('Snow Field (sans Wolf)', 'Chaff Grenade 9'),
        ('Snow Field (sans Wolf)', 'Chaff Grenade 10'),
        ('Snow Field (sans Wolf)', 'Claymore 4'),
        ('Snow Field (sans Wolf)', 'Claymore 5'),
        ('Snow Field (sans Wolf)', 'Claymore 6'),
        ('Snow Field (sans Wolf)', 'Nikita 8'),
        ('Snow Field (sans Wolf)', 'Nikita 9'),
        ('Snow Field (sans Wolf)', 'Nikita 10'),
        ('Snow Field (sans Wolf)', 'Nikita 11'),
        ('Snow Field (sans Wolf)', 'PSG-1 15'),
        ('Snow Field (sans Wolf)', 'PSG-1 16'),
        ('Blast Furnace', 'Ration 34'),
        ('Blast Furnace', 'Ration 35'),
        ('Blast Furnace', 'SOCOM 31'),
        ('Blast Furnace', 'SOCOM 32'),
        ('Blast Furnace', 'SOCOM 33'),
        ('Blast Furnace', 'FA-MAS 34'),
        ('Blast Furnace', 'C4 5'),
        ('Blast Furnace', 'Stun Grenade 7'),
        ('Blast Furnace', 'Stun Grenade 8'),
        ('Blast Furnace', 'Nikita 12'),
        ('Blast Furnace', 'Nikita 13'),
        ('Blast Furnace', 'PSG-1 17'),
        ('Blast Furnace', 'PSG-1 18'),
        ('Cargo Elevator', 'Ration 36'),
        ('Cargo Elevator', 'FA-MAS 35'),
        ('Cargo Elevator', 'FA-MAS 36'),
        ('Cargo Elevator', 'FA-MAS 37'),
        ('Cargo Elevator', 'FA-MAS 38'),
        ('Cargo Elevator', 'FA-MAS 39'),
        ('Cargo Elevator', 'FA-MAS 40'),
        ('Cargo Elevator', 'FA-MAS 41'),
        ('Cargo Elevator', 'FA-MAS 42'),
        ('Cargo Elevator', 'SOCOM 34'),
        ('Cargo Elevator', 'SOCOM 35'),
        ('Cargo Elevator', 'Claymore 7'),
        ('Cargo Elevator', 'Claymore 8'),
        ('Cargo Elevator', 'Claymore 9'),
        ('Cargo Elevator', 'BOSS: Black-outfitted Genome Soldiers II'),
        ('Warehouse', 'Ration 37'),
        ('Warehouse', 'Stinger 7'),
        ('Warehouse', 'Stinger 8'),
        ('Warehouse', 'Nikita 14'),
        ('Warehouse', 'BOSS: Vulcan Raven'),
        ('Warehouse North', 'Ration 38'),
        ('Warehouse North', 'Chaff Grenade 11'),
        ('Warehouse North', 'Stinger 9'),
        ('Warehouse North', 'Stinger 10'),
        ('Warehouse North', 'Stinger 11'),
        ('Warehouse North', 'Stinger 12'),
        ('Underground Base', 'Ration 39'),
        ('Underground Base', 'SOCOM 36'),
        ('Underground Base', 'SOCOM 37'),
        ('Underground Base', 'SOCOM 38'),
        ('Underground Base', 'FA-MAS 43'),
        ('Underground Base', 'FA-MAS 44'),
        ('Underground Base', 'FA-MAS 45'),
        ('Underground Base', 'FA-MAS 46'),
        ('Underground Base', 'Chaff Grenade 12'),
        ('Underground Base', 'Chaff Grenade 13'),
        ('Underground Base', 'Chaff Grenade 14'),
        ('Underground Base', 'Stinger 13'),
        ('Underground Base', 'Stinger 14'),
        ('Underground Base', 'Pal Key (Found)'),
        ('Command Room', 'Ration 40'),
        ('Metal Gear REX - Battle', 'Ration 42'),
        ('Metal Gear REX - Battle', 'Ration 43'),
        ('Metal Gear REX - Battle', 'Stinger 15'),
        ('Metal Gear REX - Battle', 'Stinger 16'),
        ('Metal Gear REX - Battle', 'Stinger 17'),
        ('Metal Gear REX - Battle', 'Chaff Grenade 15'),
        ('Metal Gear REX - Battle', 'Stun Grenade 9'),
        ('Metal Gear REX - Battle', 'BOSS: Metal Gear REX'),
        ('Metal Gear REX - Battle', 'BOSS: Liquid Snake'),
        ('Escape Route', 'Ration 41'),
        ('Escape Route', 'The Best is Yet to Come'),
    ]

    return {
        full_location_name(region_name, location_name): Locations.location_name_to_id_table[location_name]
        for region_name, location_name in pairs
        if location_name in Locations.location_name_to_id_table
    }

def make_location(world: "MGSWorld", region: Region, location_name: str) -> Locations.MGSLocation:
    full_name = full_location_name(region.name, location_name)
    world.short_location_name_to_full[location_name] = full_name
    return Locations.MGSLocation(world.player, full_name, Locations.location_name_to_id_table[location_name], region)

def make_event_location(world: "MGSWorld", region: Region, location_name: str, event_name: str | None = None) -> Locations.MGSLocation:
    full_name = full_location_name(region.name, location_name)
    world.short_location_name_to_full[location_name] = full_name
    location = Locations.MGSLocation(world.player, full_name, None, region)
    if event_name is not None:
        location.place_locked_item(world.create_event(event_name))
    return location

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
        make_location(world, tank_hangar, 'Suppressor'),
        make_location(world, tank_hangar, 'Cardboard Box A'),
        make_location(world, tank_hangar, 'Mine Detector'),
        ]
    multiworld.regions.append(tank_hangar)
    heliport.connect(tank_hangar)

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
        ]
    multiworld.regions.append(armory_lvl5)
    armory.connect(armory_lvl5, 'armory_to_armory_lvl5')

    cell = Region('Cell', player, multiworld)
    cell.locations += [
        make_location(world, cell, 'SOCOM 5'),
        make_location(world, cell, 'SOCOM 6'),
        make_location(world, cell, 'SOCOM 7'),
        make_location(world, cell, 'SOCOM 8'),
        make_location(world, cell, 'Ration 6'),
        make_location(world, cell, 'Ration 7'),
        make_location(world, cell, 'Key Card Level 1'),
        make_location(world, cell, 'BOSS: Heavily Armed Genome Soldiers'),
        ]
    multiworld.regions.append(cell)
    tank_hangar.connect(cell, 'hangar_to_cell')
    armory.connect(cell, 'armory_to_cell')
    cell.connect(armory)

    armory_sth = Region('Armory Sth', player, multiworld)
    armory_sth.locations += [
        make_location(world, armory_sth, 'SOCOM 9'),
        make_location(world, armory_sth, 'SOCOM 10'),
        make_location(world, armory_sth, 'SOCOM 11'),
        make_location(world, armory_sth, 'Key Card Level 2'),
        make_location(world, armory_sth, 'BOSS: Revolver Ocelot'),
        make_event_location(world, armory_sth, 'Ocelot Fight'),
        ]
    multiworld.regions.append(armory_sth)
    armory.connect(armory_sth, 'armory_to_armory_sth')

    canyon = Region('Canyon', player, multiworld)
    canyon.locations += [
        make_location(world, canyon, 'Ration 8'),
        make_location(world, canyon, 'Grenade 3'),
        make_location(world, canyon, 'Grenade 10'),
        make_location(world, canyon, 'Grenade 11'),
        make_location(world, canyon, 'Chaff Grenade 3'),
        make_location(world, canyon, 'Claymore 1'),
        make_location(world, canyon, 'Claymore 2'),
        make_location(world, canyon, 'Claymore 3'),
        make_location(world, canyon, 'Key Card Level 3'),
        make_location(world, canyon, 'BOSS: M1 Tank'),
        ]
    multiworld.regions.append(canyon)
    tank_hangar.connect(canyon, 'hangar_to_canyon')

    nuke_building_1 = Region('Nuke Building 1', player, multiworld)
    nuke_building_1.locations += [
        make_location(world, nuke_building_1, 'Ration 9'),
        make_location(world, nuke_building_1, 'Grenade 4'),
        make_location(world, nuke_building_1, 'Chaff Grenade 4'),
        make_location(world, nuke_building_1, 'FA-MAS 4'),
        make_location(world, nuke_building_1, 'FA-MAS 5'),
        make_location(world, nuke_building_1, 'SOCOM 12'),
        ]
    multiworld.regions.append(nuke_building_1)
    canyon.connect(nuke_building_1, 'canyon_to_nuke_building_1')

    nuke_building_B1 = Region('Nuke Building B1', player, multiworld)
    nuke_building_B1.locations += [
        make_location(world, nuke_building_B1, 'Ration 10'),
        make_location(world, nuke_building_B1, 'Ration 11'),
        make_location(world, nuke_building_B1, 'Stun Grenade 2'),
        make_location(world, nuke_building_B1, 'Nikita 3'),
        make_location(world, nuke_building_B1, 'Nikita 4'),
        make_location(world, nuke_building_B1, 'Nikita 5'),
        make_location(world, nuke_building_B1, 'SOCOM 13'),
        make_location(world, nuke_building_B1, 'FA-MAS 6'),
        ]
    multiworld.regions.append(nuke_building_B1)
    nuke_building_1.connect(nuke_building_B1)

    nuke_building_B1_lvl4 = Region('Nuke Building B1 lvl4', player, multiworld)
    nuke_building_B1_lvl4.locations += [
        make_location(world, nuke_building_B1_lvl4, 'Cardboard Box B'),
        make_location(world, nuke_building_B1_lvl4, 'SOCOM 14'),
        make_location(world, nuke_building_B1_lvl4, 'FA-MAS 7'),
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
        make_location(world, nuke_building_B2, 'Ration 12'),
        make_location(world, nuke_building_B2, 'Gas Mask'),
        make_location(world, nuke_building_B2, 'C4 3'),
        make_location(world, nuke_building_B2, 'Grenade 5'),
        make_location(world, nuke_building_B2, 'Grenade 6'),
        make_location(world, nuke_building_B2, 'Chaff Grenade 5'),
        make_location(world, nuke_building_B2, 'FA-MAS 11'),
        make_location(world, nuke_building_B2, 'Nikita 6'),
        make_location(world, nuke_building_B2, 'Nikita 7'),
        ]
    multiworld.regions.append(nuke_building_B2)
    nuke_building_1.connect(nuke_building_B2, 'nuke_building_1_to_nuke_building_b2')
    nuke_building_B1.connect(nuke_building_B2, 'nuke_building_b1_to_nuke_building_b2')

    nuke_building_B2_lvl4 = Region('Nuke Building B2 lvl4', player, multiworld)
    nuke_building_B2_lvl4.locations += [
        make_location(world, nuke_building_B2_lvl4, 'Ration 13'),
        make_location(world, nuke_building_B2_lvl4, 'Stun Grenade 3'),
        make_location(world, nuke_building_B2_lvl4, 'Stun Grenade 4'),
        make_location(world, nuke_building_B2_lvl4, 'Night Vision Goggles'),
        ]
    multiworld.regions.append(nuke_building_B2_lvl4)
    nuke_building_B2.connect(nuke_building_B2_lvl4, 'nuke_bulding_b2_to_nuke_building_b2_lvl4')

    nuke_building_B2_lvl6 = Region('Nuke Building B2 lvl6', player, multiworld)
    nuke_building_B2_lvl6.locations += [
        make_location(world, nuke_building_B2_lvl6, 'Body Armor'),
        ]
    multiworld.regions.append(nuke_building_B2_lvl6)
    nuke_building_B2.connect(nuke_building_B2_lvl6, 'nuke_bulding_b2_to_nuke_building_b2_lvl6')

    lab = Region('Lab', player, multiworld)
    lab.locations += [
        make_location(world, lab, 'Ration 14'),
        make_location(world, lab, 'SOCOM 15'),
        make_location(world, lab, 'FA-MAS 12'),
        make_location(world, lab, 'FA-MAS 13'),
        make_location(world, lab, 'Chaff Grenade 6'),
        make_location(world, lab, 'Key Card Level 4'),
        make_location(world, lab, 'BOSS: Gray Fox'),
        make_event_location(world, lab, 'Gray Fox Fight'),
        ]
    multiworld.regions.append(lab)
    nuke_building_B2.connect(lab)

    commander_room = Region('Commander Room', player, multiworld)
    commander_room.locations += [
        make_location(world, commander_room, 'Ration 15'),
        make_location(world, commander_room, 'Ration 16'),
        make_location(world, commander_room, 'SOCOM 16'),
        make_location(world, commander_room, 'SOCOM 17'),
        make_location(world, commander_room, 'FA-MAS 14'),
        make_location(world, commander_room, 'FA-MAS 15'),
        make_location(world, commander_room, 'FA-MAS 16'),
        make_location(world, commander_room, 'BOSS: Psycho Mantis'),
        ]
    multiworld.regions.append(commander_room)
    nuke_building_B1.connect(commander_room, 'nuke_building_b1_to_commander_room')

    cave = Region('Cave', player, multiworld)
    cave.locations += [
        make_location(world, cave, 'Ration 17'),
        make_location(world, cave, 'Ration 18'),
        make_location(world, cave, 'Ration 19'),
        make_location(world, cave, 'SOCOM 18'),
        make_location(world, cave, 'SOCOM 19'),
        make_location(world, cave, 'FA-MAS 17'),
        make_location(world, cave, 'FA-MAS 18'),
        make_location(world, cave, 'Diazepam 2'),
        make_location(world, cave, 'PSG-1 3'),
        make_location(world, cave, 'PSG-1 4'),
        make_location(world, cave, 'PSG-1 5'),
        ]
    multiworld.regions.append(cave)
    commander_room.connect(cave)

    underground_passage = Region('Underground Passage', player, multiworld)
    underground_passage.locations += [
        make_location(world, underground_passage, 'Ration 20'),
        make_location(world, underground_passage, 'SOCOM 20'),
        make_location(world, underground_passage, 'FA-MAS 19'),
        make_location(world, underground_passage, 'PSG-1 6'),
        make_location(world, underground_passage, 'PSG-1 7'),
        make_location(world, underground_passage, 'PSG-1 8'),
        make_location(world, underground_passage, 'PSG-1 9'),
        make_location(world, underground_passage, 'BOSS: Sniper Wolf I'),
        ]
    multiworld.regions.append(underground_passage)
    cave.connect(underground_passage, 'cave_to_underground_passage')

    medi_room = Region('Medi Room', player, multiworld)
    medi_room.locations += [
        make_location(world, medi_room, 'Ration 21'),
        make_location(world, medi_room, 'Ration 22'),
        make_location(world, medi_room, 'Handkerchief'),
        # make_location(world, medi_room, 'Ketchup'),
        make_location(world, medi_room, 'Key Card Level 6'),
        # make_location(world, medi_room, 'Time Bomb 1'),
        ]
    multiworld.regions.append(medi_room)
    underground_passage.connect(medi_room)

    comm_tower_a = Region('Comm Tower A', player, multiworld)
    comm_tower_a.locations += [
        make_location(world, comm_tower_a, 'Ration 23'),
        make_location(world, comm_tower_a, 'Ration 24'),
        make_location(world, comm_tower_a, 'SOCOM 21'),
        make_location(world, comm_tower_a, 'SOCOM 22'),
        make_location(world, comm_tower_a, 'SOCOM 23'),
        make_location(world, comm_tower_a, 'SOCOM 24'),
        make_location(world, comm_tower_a, 'SOCOM 25'),
        make_location(world, comm_tower_a, 'FA-MAS 20'),
        make_location(world, comm_tower_a, 'FA-MAS 21'),
        make_location(world, comm_tower_a, 'FA-MAS 22'),
        make_location(world, comm_tower_a, 'FA-MAS 23'),
        make_location(world, comm_tower_a, 'FA-MAS 24'),
        make_location(world, comm_tower_a, 'Stun Grenade 5'),
        make_location(world, comm_tower_a, 'Rope'),
        make_location(world, comm_tower_a, 'BOSS: Black-outfitted Genome Soldiers I'),
        ]
    multiworld.regions.append(comm_tower_a)
    medi_room.connect(comm_tower_a, 'medi_room_to_comm_tower_a')

    walkway = Region('Walkway', player, multiworld)
    walkway.locations += [
        make_location(world, walkway, 'Ration 25'),
        make_location(world, walkway, 'C4 4'),
        make_location(world, walkway, 'Stinger 1'),
        make_location(world, walkway, 'Stinger 2'),
        ]
    multiworld.regions.append(walkway)
    comm_tower_a.connect(walkway, 'comm_tower_a_to_walkway')

    comm_tower_b = Region('Comm Tower B', player, multiworld)
    comm_tower_b.locations += [
        make_location(world, comm_tower_b, 'Ration 26'),
        make_location(world, comm_tower_b, 'SOCOM 26'),
        make_location(world, comm_tower_b, 'FA-MAS 25'),
        make_location(world, comm_tower_b, 'FA-MAS 26'),
        make_location(world, comm_tower_b, 'Grenade 7'),
        make_location(world, comm_tower_b, 'Chaff Grenade 7'),
        make_location(world, comm_tower_b, 'Stinger 3'),
        make_location(world, comm_tower_b, 'Stinger 4'),
        make_location(world, comm_tower_b, 'Stinger 5'),
        ]
    multiworld.regions.append(comm_tower_b)
    walkway.connect(comm_tower_b)

    comm_tower_b_after_hind = Region('Comm Tower B (Hind D[efeated])', player, multiworld)
    comm_tower_b_after_hind.locations += [
        make_location(world, comm_tower_b, 'Ration 27'),
        make_location(world, comm_tower_b, 'Ration 28'),
        make_location(world, comm_tower_b, 'SOCOM 27'),
        make_location(world, comm_tower_b, 'SOCOM 28'),
        make_location(world, comm_tower_b, 'FA-MAS 27'),
        make_location(world, comm_tower_b, 'FA-MAS 28'),
        make_location(world, comm_tower_b, 'FA-MAS 29'),
        make_location(world, comm_tower_b, 'FA-MAS 30'),
        make_location(world, comm_tower_b_after_hind, 'Chaff Grenade 8'),
        make_location(world, comm_tower_b_after_hind, 'PSG-1 10'),
        make_location(world, comm_tower_b_after_hind, 'PSG-1 11'),
        make_location(world, comm_tower_b_after_hind, 'PSG-1 12'),
        make_location(world, comm_tower_b_after_hind, 'BOSS: Stealth Camouflaged Genome Soldiers'),
        ]
    multiworld.regions.append(comm_tower_b_after_hind)
    comm_tower_b.connect(comm_tower_b_after_hind, 'comm_tower_b_to_comm_tower_b_after_hind')

    comm_tower_b_roof = Region('Comm Tower B Roof', player, multiworld)
    hind_d_event = make_event_location(world, comm_tower_b_roof, 'A Hind D?', 'A Hind D[efeated]')
    comm_tower_b_roof.locations += [
        make_location(world, comm_tower_b_roof, 'Ration 29'),
        make_location(world, comm_tower_b_roof, 'Stinger 6'),
        make_location(world, comm_tower_b_roof, 'BOSS: A Hind D?'),
        hind_d_event
        ]
    multiworld.regions.append(comm_tower_b_roof)
    comm_tower_b.connect(comm_tower_b_roof, 'comm_tower_b_to_comm_tower_b_roof')

    snowfield = Region('Snow Field', player, multiworld)
    snowfield.locations += [
        make_location(world, snowfield, 'PSG-1 13'),
        make_location(world, snowfield, 'PSG-1 14'),
        make_location(world, snowfield, 'Ration 30'),
        make_location(world, snowfield, 'BOSS: Sniper Wolf II'),
        ]
    multiworld.regions.append(snowfield)
    comm_tower_b.connect(snowfield, 'comm_tower_b_to_snowfield')

    snowfield_sans_wolf = Region('Snow Field (sans Wolf)', player, multiworld)
    snowfield_sans_wolf.locations += [
        make_location(world, snowfield_sans_wolf, 'Cardboard Box C'),
        make_location(world, snowfield_sans_wolf, 'Ration 31'),
        make_location(world, snowfield_sans_wolf, 'Ration 32'),
        make_location(world, snowfield_sans_wolf, 'Ration 33'),
        make_location(world, snowfield_sans_wolf, 'Diazepam 3'),
        make_location(world, snowfield_sans_wolf, 'SOCOM 29'),
        make_location(world, snowfield_sans_wolf, 'SOCOM 30'),
        make_location(world, snowfield_sans_wolf, 'FA-MAS 31'),
        make_location(world, snowfield_sans_wolf, 'FA-MAS 32'),
        make_location(world, snowfield_sans_wolf, 'FA-MAS 33'),
        make_location(world, snowfield_sans_wolf, 'Grenade 8'),
        make_location(world, snowfield_sans_wolf, 'Grenade 9'),
        make_location(world, snowfield_sans_wolf, 'Stun Grenade 6'),
        make_location(world, snowfield_sans_wolf, 'Chaff Grenade 9'),
        make_location(world, snowfield_sans_wolf, 'Chaff Grenade 10'),
        make_location(world, snowfield_sans_wolf, 'Claymore 4'),
        make_location(world, snowfield_sans_wolf, 'Claymore 5'),
        make_location(world, snowfield_sans_wolf, 'Claymore 6'),
        make_location(world, snowfield_sans_wolf, 'Nikita 8'),
        make_location(world, snowfield_sans_wolf, 'Nikita 9'),
        make_location(world, snowfield_sans_wolf, 'Nikita 10'),
        make_location(world, snowfield_sans_wolf, 'Nikita 11'),
        make_location(world, snowfield_sans_wolf, 'PSG-1 15'),
        make_location(world, snowfield_sans_wolf, 'PSG-1 16'),
        ]
    multiworld.regions.append(snowfield_sans_wolf)
    snowfield.connect(snowfield_sans_wolf, 'snowfield_to_snowfield_sans_wolf')

    blast_furnace = Region('Blast Furnace', player, multiworld)
    blast_furnace.locations += [
        make_location(world, blast_furnace, 'Ration 34'),
        make_location(world, blast_furnace, 'Ration 35'),
        make_location(world, blast_furnace, 'SOCOM 31'),
        make_location(world, blast_furnace, 'SOCOM 32'),
        make_location(world, blast_furnace, 'SOCOM 33'),
        make_location(world, blast_furnace, 'FA-MAS 34'),
        make_location(world, blast_furnace, 'C4 5'),
        make_location(world, blast_furnace, 'Stun Grenade 7'),
        make_location(world, blast_furnace, 'Stun Grenade 8'),
        make_location(world, blast_furnace, 'Nikita 12'),
        make_location(world, blast_furnace, 'Nikita 13'),
        make_location(world, blast_furnace, 'PSG-1 17'),
        make_location(world, blast_furnace, 'PSG-1 18'),
        ]
    multiworld.regions.append(blast_furnace)
    snowfield_sans_wolf.connect(blast_furnace)

    cargo_elevator = Region('Cargo Elevator', player, multiworld)
    cargo_elevator.locations += [
        make_location(world, cargo_elevator, 'Ration 36'),
        make_location(world, cargo_elevator, 'FA-MAS 35'),
        make_location(world, cargo_elevator, 'FA-MAS 36'),
        make_location(world, cargo_elevator, 'FA-MAS 37'),
        make_location(world, cargo_elevator, 'FA-MAS 38'),
        make_location(world, cargo_elevator, 'FA-MAS 39'),
        make_location(world, cargo_elevator, 'FA-MAS 40'),
        make_location(world, cargo_elevator, 'FA-MAS 41'),
        make_location(world, cargo_elevator, 'FA-MAS 42'),
        make_location(world, cargo_elevator, 'SOCOM 34'),
        make_location(world, cargo_elevator, 'SOCOM 35'),
        make_location(world, cargo_elevator, 'Claymore 7'),
        make_location(world, cargo_elevator, 'Claymore 8'),
        make_location(world, cargo_elevator, 'Claymore 9'),
        make_location(world, cargo_elevator, 'BOSS: Black-outfitted Genome Soldiers II'),
        ]
    multiworld.regions.append(cargo_elevator)
    blast_furnace.connect(cargo_elevator)

    warehouse = Region('Warehouse', player, multiworld)
    warehouse.locations += [
        make_location(world, warehouse, 'Ration 37'),
        make_location(world, warehouse, 'Stinger 7'),
        make_location(world, warehouse, 'Stinger 8'),
        make_location(world, warehouse, 'Nikita 14'),
        make_location(world, warehouse, 'BOSS: Vulcan Raven'),
        ]
    multiworld.regions.append(warehouse)
    cargo_elevator.connect(warehouse)

    warehouse_nt = Region('Warehouse North', player, multiworld)
    warehouse_nt.locations += [
        make_location(world, warehouse_nt, 'Ration 38'),
        make_location(world, warehouse_nt, 'Chaff Grenade 11'),
        make_location(world, warehouse_nt, 'Stinger 9'),
        make_location(world, warehouse_nt, 'Stinger 10'),
        make_location(world, warehouse_nt, 'Stinger 11'),
        make_location(world, warehouse_nt, 'Stinger 12'),
        ]
    multiworld.regions.append(warehouse_nt)
    warehouse.connect(warehouse_nt, 'warehouse_to_warehouse_nt')

    under_ground_base = Region('Underground Base', player, multiworld)
    under_ground_base.locations += [
        make_location(world, under_ground_base, 'Ration 39'),
        make_location(world, under_ground_base, 'SOCOM 36'),
        make_location(world, under_ground_base, 'SOCOM 37'),
        make_location(world, under_ground_base, 'SOCOM 38'),
        make_location(world, under_ground_base, 'FA-MAS 43'),
        make_location(world, under_ground_base, 'FA-MAS 44'),
        make_location(world, under_ground_base, 'FA-MAS 45'),
        make_location(world, under_ground_base, 'FA-MAS 46'),
        make_location(world, under_ground_base, 'Chaff Grenade 12'),
        make_location(world, under_ground_base, 'Chaff Grenade 13'),
        make_location(world, under_ground_base, 'Chaff Grenade 14'),
        make_location(world, under_ground_base, 'Stinger 13'),
        make_location(world, under_ground_base, 'Stinger 14'),
        # make_location(world, under_ground_base, 'Pal Key (Found)'),
        ]
    multiworld.regions.append(under_ground_base)
    warehouse_nt.connect(under_ground_base)

    command_room = Region('Command Room', player, multiworld)
    command_room.locations += [
        make_location(world, command_room, 'Ration 40'),
        ]
    multiworld.regions.append(command_room)
    under_ground_base.connect(command_room, 'underground_base_to_command_room')

    rex_battle = Region('Metal Gear REX - Battle', player, multiworld)
    rex_battle.locations += [
        make_location(world, rex_battle, 'Ration 42'),
        make_location(world, rex_battle, 'Ration 43'),
        make_location(world, rex_battle, 'Stinger 15'),
        make_location(world, rex_battle, 'Stinger 16'),
        make_location(world, rex_battle, 'Stinger 17'),
        make_location(world, rex_battle, 'Chaff Grenade 15'),
        make_location(world, rex_battle, 'Stun Grenade 9'),
        make_location(world, rex_battle, 'BOSS: Metal Gear REX'),
        make_location(world, rex_battle, 'BOSS: Liquid Snake'),
        ]
    multiworld.regions.append(rex_battle)
    under_ground_base.connect(rex_battle, 'under_ground_base_to_rex_battle')

    escape_route = Region('Escape Route', player, multiworld)
    escape_route.locations += [
        make_location(world, escape_route, 'Ration 41'),
        make_location(world, escape_route, 'The Best is Yet to Come'),
        ]
    multiworld.regions.append(escape_route)
    rex_battle.connect(escape_route)
