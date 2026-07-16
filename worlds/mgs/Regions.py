from BaseClasses import Region
from . import Locations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import MGSWorld

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
        Locations.MGSLocation(player, 'Ration 1', Locations.location_name_to_id_table['Ration 1'], docks),
        Locations.MGSLocation(player, 'Ration 2', Locations.location_name_to_id_table['Ration 2'], docks),
        Locations.MGSLocation(player, 'Ration 3', Locations.location_name_to_id_table['Ration 3'], docks),
        ]
    multiworld.regions.append(docks)
    menu.connect(docks)

    heliport = Region('Heliport', player, multiworld)
    heliport.locations += [
        Locations.MGSLocation(player, 'Chaff Grenade 1', Locations.location_name_to_id_table['Chaff Grenade 1'], heliport),
        Locations.MGSLocation(player, 'Stun Grenade 1', Locations.location_name_to_id_table['Stun Grenade 1'], heliport),
        Locations.MGSLocation(player, 'SOCOM 1', Locations.location_name_to_id_table['SOCOM 1'], heliport),
        Locations.MGSLocation(player, 'Ration 4', Locations.location_name_to_id_table['Ration 4'], heliport),
        ]
    multiworld.regions.append(heliport)
    docks.connect(heliport)

    tank_hangar = Region('Tank Hangar', player, multiworld)
    tank_hangar.locations += [
        Locations.MGSLocation(player, 'Chaff Grenade 2', Locations.location_name_to_id_table['Chaff Grenade 2'], tank_hangar),
        Locations.MGSLocation(player, 'Thermal Goggles', Locations.location_name_to_id_table['Thermal Goggles'], tank_hangar),
        Locations.MGSLocation(player, 'SOCOM 2', Locations.location_name_to_id_table['SOCOM 2'], tank_hangar),
        Locations.MGSLocation(player, 'Ration 5', Locations.location_name_to_id_table['Ration 5'], tank_hangar),
        Locations.MGSLocation(player, 'Suppressor', Locations.location_name_to_id_table['Suppressor'], tank_hangar),
        Locations.MGSLocation(player, 'Cardboard Box A', Locations.location_name_to_id_table['Cardboard Box A'], tank_hangar),
        Locations.MGSLocation(player, 'Mine Detector', Locations.location_name_to_id_table['Mine Detector'], tank_hangar),
        ]
    multiworld.regions.append(tank_hangar)
    heliport.connect(tank_hangar)

    armory = Region('Armory', player, multiworld)
    armory.locations += [
        Locations.MGSLocation(player, 'SOCOM 3', Locations.location_name_to_id_table['SOCOM 3'], armory),
        Locations.MGSLocation(player, 'SOCOM 4', Locations.location_name_to_id_table['SOCOM 4'], armory),
        ]
    multiworld.regions.append(armory)
    tank_hangar.connect(armory)

    armory_lvl1 = Region('Armory_lvl1', player, multiworld)
    armory_lvl1.locations += [
        Locations.MGSLocation(player, 'C4 1', Locations.location_name_to_id_table['C4 1'], armory_lvl1),
        Locations.MGSLocation(player, 'C4 2', Locations.location_name_to_id_table['C4 2'], armory_lvl1),
        Locations.MGSLocation(player, 'Grenade 1', Locations.location_name_to_id_table['Grenade 1'], armory_lvl1),
        Locations.MGSLocation(player, 'Grenade 2', Locations.location_name_to_id_table['Grenade 2'], armory_lvl1),
        ]
    multiworld.regions.append(armory_lvl1)
    armory.connect(armory_lvl1, 'armory_to_armory_lvl1')

    armory_lvl2 = Region('Armory_lvl2', player, multiworld)
    armory_lvl2.locations += [
        Locations.MGSLocation(player, 'FA-MAS 1', Locations.location_name_to_id_table['FA-MAS 1'], armory_lvl2),
        Locations.MGSLocation(player, 'FA-MAS 2', Locations.location_name_to_id_table['FA-MAS 2'], armory_lvl2),
        Locations.MGSLocation(player, 'FA-MAS 3', Locations.location_name_to_id_table['FA-MAS 3'], armory_lvl2),
        ]
    multiworld.regions.append(armory_lvl2)
    armory.connect(armory_lvl2, 'armory_to_armory_lvl2')

    armory_lvl3 = Region('Armory_lvl3', player, multiworld)
    armory_lvl3.locations += [
        Locations.MGSLocation(player, 'Nikita 1', Locations.location_name_to_id_table['Nikita 1'], armory_lvl3),
        Locations.MGSLocation(player, 'Nikita 2', Locations.location_name_to_id_table['Nikita 2'], armory_lvl3),
        ]
    multiworld.regions.append(armory_lvl3)
    armory.connect(armory_lvl3, 'armory_to_armory_lvl3')

    armory_lvl5 = Region('Armory_lvl5', player, multiworld)
    armory_lvl5.locations += [
        Locations.MGSLocation(player, 'PSG-1 1', Locations.location_name_to_id_table['PSG-1 1'], armory_lvl5),
        Locations.MGSLocation(player, 'PSG-1 2', Locations.location_name_to_id_table['PSG-1 2'], armory_lvl5),
        ]
    multiworld.regions.append(armory_lvl5)
    armory.connect(armory_lvl5, 'armory_to_armory_lvl5')

    cell = Region('Cell', player, multiworld)
    cell.locations += [
        Locations.MGSLocation(player, 'SOCOM 5', Locations.location_name_to_id_table['SOCOM 5'], cell),
        Locations.MGSLocation(player, 'SOCOM 6', Locations.location_name_to_id_table['SOCOM 6'], cell),
        Locations.MGSLocation(player, 'SOCOM 7', Locations.location_name_to_id_table['SOCOM 7'], cell),
        Locations.MGSLocation(player, 'SOCOM 8', Locations.location_name_to_id_table['SOCOM 8'], cell),
        Locations.MGSLocation(player, 'Ration 6', Locations.location_name_to_id_table['Ration 6'], cell),
        Locations.MGSLocation(player, 'Ration 7', Locations.location_name_to_id_table['Ration 7'], cell),
        Locations.MGSLocation(player, 'Key Card Level 1', Locations.location_name_to_id_table['Key Card Level 1'], cell),
        Locations.MGSLocation(player, 'BOSS: Heavily Armed Genome Soldiers', Locations.location_name_to_id_table['BOSS: Heavily Armed Genome Soldiers'], cell),
        ]
    multiworld.regions.append(cell)
    tank_hangar.connect(cell, 'hangar_to_cell')
    armory.connect(cell, 'armory_to_cell')
    cell.connect(armory)

    armory_sth = Region('Armory Sth', player, multiworld)
    armory_sth.locations += [
        Locations.MGSLocation(player, 'SOCOM 9', Locations.location_name_to_id_table['SOCOM 9'], armory_sth),
        Locations.MGSLocation(player, 'SOCOM 10', Locations.location_name_to_id_table['SOCOM 10'], armory_sth),
        Locations.MGSLocation(player, 'SOCOM 11', Locations.location_name_to_id_table['SOCOM 11'], armory_sth),
        Locations.MGSLocation(player, 'Key Card Level 2', Locations.location_name_to_id_table['Key Card Level 2'], armory_sth),
        Locations.MGSLocation(player, 'BOSS: Revolver Ocelot', Locations.location_name_to_id_table['BOSS: Revolver Ocelot'], armory_sth),
        Locations.MGSLocation(player, 'Ocelot Fight', None, armory_sth),
        ]
    multiworld.regions.append(armory_sth)
    armory.connect(armory_sth, 'armory_to_armory_sth')

    canyon = Region('Canyon', player, multiworld)
    canyon.locations += [
        Locations.MGSLocation(player, 'Ration 8', Locations.location_name_to_id_table['Ration 8'], canyon),
        Locations.MGSLocation(player, 'Grenade 3', Locations.location_name_to_id_table['Grenade 3'], canyon),
        Locations.MGSLocation(player, 'Grenade 10', Locations.location_name_to_id_table['Grenade 10'], canyon),
        Locations.MGSLocation(player, 'Grenade 11', Locations.location_name_to_id_table['Grenade 11'], canyon),
        Locations.MGSLocation(player, 'Chaff Grenade 3', Locations.location_name_to_id_table['Chaff Grenade 3'], canyon),
        Locations.MGSLocation(player, 'Claymore 1', Locations.location_name_to_id_table['Claymore 1'], canyon),
        Locations.MGSLocation(player, 'Claymore 2', Locations.location_name_to_id_table['Claymore 2'], canyon),
        Locations.MGSLocation(player, 'Claymore 3', Locations.location_name_to_id_table['Claymore 3'], canyon),
        Locations.MGSLocation(player, 'Key Card Level 3', Locations.location_name_to_id_table['Key Card Level 3'], canyon),
        Locations.MGSLocation(player, 'BOSS: M1 Tank', Locations.location_name_to_id_table['BOSS: M1 Tank'], canyon),
        ]
    multiworld.regions.append(canyon)
    tank_hangar.connect(canyon, 'hangar_to_canyon')

    nuke_building_1 = Region('Nuke Building 1', player, multiworld)
    nuke_building_1.locations += [
        Locations.MGSLocation(player, 'Ration 9', Locations.location_name_to_id_table['Ration 9'], nuke_building_1),
        Locations.MGSLocation(player, 'Grenade 4', Locations.location_name_to_id_table['Grenade 4'], nuke_building_1),
        Locations.MGSLocation(player, 'Chaff Grenade 4', Locations.location_name_to_id_table['Chaff Grenade 4'], nuke_building_1),
        Locations.MGSLocation(player, 'FA-MAS 4', Locations.location_name_to_id_table['FA-MAS 4'], nuke_building_1),
        Locations.MGSLocation(player, 'FA-MAS 5', Locations.location_name_to_id_table['FA-MAS 5'], nuke_building_1),
        Locations.MGSLocation(player, 'SOCOM 12', Locations.location_name_to_id_table['SOCOM 12'], nuke_building_1),
        ]
    multiworld.regions.append(nuke_building_1)
    canyon.connect(nuke_building_1, 'canyon_to_nuke_building_1')

    nuke_building_B1 = Region('Nuke Building B1', player, multiworld)
    nuke_building_B1.locations += [
        Locations.MGSLocation(player, 'Ration 10', Locations.location_name_to_id_table['Ration 10'], nuke_building_B1),
        Locations.MGSLocation(player, 'Ration 11', Locations.location_name_to_id_table['Ration 11'], nuke_building_B1),
        Locations.MGSLocation(player, 'Stun Grenade 2', Locations.location_name_to_id_table['Stun Grenade 2'], nuke_building_B1),
        Locations.MGSLocation(player, 'Nikita 3', Locations.location_name_to_id_table['Nikita 3'], nuke_building_B1),
        Locations.MGSLocation(player, 'Nikita 4', Locations.location_name_to_id_table['Nikita 4'], nuke_building_B1),
        Locations.MGSLocation(player, 'Nikita 5', Locations.location_name_to_id_table['Nikita 5'], nuke_building_B1),
        Locations.MGSLocation(player, 'SOCOM 13', Locations.location_name_to_id_table['SOCOM 13'], nuke_building_B1),
        Locations.MGSLocation(player, 'FA-MAS 6', Locations.location_name_to_id_table['FA-MAS 6'], nuke_building_B1),
        ]
    multiworld.regions.append(nuke_building_B1)
    nuke_building_1.connect(nuke_building_B1)

    nuke_building_B1_lvl4 = Region('Nuke Building B1 lvl4', player, multiworld)
    nuke_building_B1_lvl4.locations += [
        Locations.MGSLocation(player, 'Cardboard Box B', Locations.location_name_to_id_table['Cardboard Box B'], nuke_building_B1_lvl4),
        Locations.MGSLocation(player, 'SOCOM 14', Locations.location_name_to_id_table['SOCOM 14'], nuke_building_B1_lvl4),
        Locations.MGSLocation(player, 'FA-MAS 7', Locations.location_name_to_id_table['FA-MAS 7'], nuke_building_B1_lvl4),
        Locations.MGSLocation(player, 'Pal Key', Locations.location_name_to_id_table['Pal Key'], nuke_building_B1_lvl4),
        Locations.MGSLocation(player, 'Key Card Level 5', Locations.location_name_to_id_table['Key Card Level 5'], nuke_building_B1_lvl4),
        ]
    multiworld.regions.append(nuke_building_B1_lvl4)
    nuke_building_B1.connect(nuke_building_B1_lvl4, 'nuke_building_b1_to_nuke_bulding_b1_lvl4')

    nuke_building_B1_lvl5 = Region('Nuke Building B1 lvl5', player, multiworld)
    nuke_building_B1_lvl5.locations += [
        Locations.MGSLocation(player, 'Diazepam 1', Locations.location_name_to_id_table['Diazepam 1'], nuke_building_B1_lvl5),
        Locations.MGSLocation(player, 'FA-MAS 8', Locations.location_name_to_id_table['FA-MAS 8'], nuke_building_B1_lvl5),
        Locations.MGSLocation(player, 'FA-MAS 9', Locations.location_name_to_id_table['FA-MAS 9'], nuke_building_B1_lvl5),
        Locations.MGSLocation(player, 'FA-MAS 10', Locations.location_name_to_id_table['FA-MAS 10'], nuke_building_B1_lvl5),
        ]
    multiworld.regions.append(nuke_building_B1_lvl5)
    nuke_building_B1.connect(nuke_building_B1_lvl5, 'nuke_building_b1_to_nuke_bulding_b1_lvl5')

    nuke_building_B2 = Region('Nuke Building B2', player, multiworld)
    nuke_building_B2.locations += [
        Locations.MGSLocation(player, 'Ration 12', Locations.location_name_to_id_table['Ration 12'], nuke_building_B2),
        Locations.MGSLocation(player, 'Gas Mask', Locations.location_name_to_id_table['Gas Mask'], nuke_building_B2),
        Locations.MGSLocation(player, 'C4 3', Locations.location_name_to_id_table['C4 3'], nuke_building_B2),
        Locations.MGSLocation(player, 'Grenade 5', Locations.location_name_to_id_table['Grenade 5'], nuke_building_B2),
        Locations.MGSLocation(player, 'Grenade 6', Locations.location_name_to_id_table['Grenade 6'], nuke_building_B2),
        Locations.MGSLocation(player, 'Chaff Grenade 5', Locations.location_name_to_id_table['Chaff Grenade 5'], nuke_building_B2),
        Locations.MGSLocation(player, 'FA-MAS 11', Locations.location_name_to_id_table['FA-MAS 11'], nuke_building_B2),
        Locations.MGSLocation(player, 'Nikita 6', Locations.location_name_to_id_table['Nikita 6'], nuke_building_B2),
        Locations.MGSLocation(player, 'Nikita 7', Locations.location_name_to_id_table['Nikita 7'], nuke_building_B2),
        ]
    multiworld.regions.append(nuke_building_B2)
    nuke_building_1.connect(nuke_building_B2, 'nuke_building_1_to_nuke_building_b2')
    nuke_building_B1.connect(nuke_building_B2, 'nuke_building_b1_to_nuke_building_b2')

    nuke_building_B2_lvl4 = Region('Nuke Building B2 lvl4', player, multiworld)
    nuke_building_B2_lvl4.locations += [
        Locations.MGSLocation(player, 'Ration 13', Locations.location_name_to_id_table['Ration 13'], nuke_building_B2_lvl4),
        Locations.MGSLocation(player, 'Stun Grenade 3', Locations.location_name_to_id_table['Stun Grenade 3'], nuke_building_B2_lvl4),
        Locations.MGSLocation(player, 'Stun Grenade 4', Locations.location_name_to_id_table['Stun Grenade 4'], nuke_building_B2_lvl4),
        Locations.MGSLocation(player, 'Night Vision Goggles', Locations.location_name_to_id_table['Night Vision Goggles'], nuke_building_B2_lvl4),
        ]
    multiworld.regions.append(nuke_building_B2_lvl4)
    nuke_building_B2.connect(nuke_building_B2_lvl4, 'nuke_bulding_b2_to_nuke_building_b2_lvl4')

    nuke_building_B2_lvl6 = Region('Nuke Building B2 lvl6', player, multiworld)
    nuke_building_B2_lvl6.locations += [
        Locations.MGSLocation(player, 'Body Armor', Locations.location_name_to_id_table['Body Armor'], nuke_building_B2_lvl6),
        ]
    multiworld.regions.append(nuke_building_B2_lvl6)
    nuke_building_B2.connect(nuke_building_B2_lvl6, 'nuke_bulding_b2_to_nuke_building_b2_lvl6')

    lab = Region('Lab', player, multiworld)
    lab.locations += [
        Locations.MGSLocation(player, 'Ration 14', Locations.location_name_to_id_table['Ration 14'], lab),
        Locations.MGSLocation(player, 'SOCOM 15', Locations.location_name_to_id_table['SOCOM 15'], lab),
        Locations.MGSLocation(player, 'FA-MAS 12', Locations.location_name_to_id_table['FA-MAS 12'], lab),
        Locations.MGSLocation(player, 'FA-MAS 13', Locations.location_name_to_id_table['FA-MAS 13'], lab),
        Locations.MGSLocation(player, 'Chaff Grenade 6', Locations.location_name_to_id_table['Chaff Grenade 6'], lab),
        Locations.MGSLocation(player, 'Key Card Level 4', Locations.location_name_to_id_table['Key Card Level 4'], lab),
        Locations.MGSLocation(player, 'BOSS: Gray Fox', Locations.location_name_to_id_table['BOSS: Gray Fox'], lab),
        Locations.MGSLocation(player, 'Gray Fox Fight', None, lab),
        ]
    multiworld.regions.append(lab)
    nuke_building_B2.connect(lab)

    commander_room = Region('Commander Room', player, multiworld)
    commander_room.locations += [
        Locations.MGSLocation(player, 'Ration 15', Locations.location_name_to_id_table['Ration 15'], commander_room),
        Locations.MGSLocation(player, 'Ration 16', Locations.location_name_to_id_table['Ration 16'], commander_room),
        Locations.MGSLocation(player, 'SOCOM 16', Locations.location_name_to_id_table['SOCOM 16'], commander_room),
        Locations.MGSLocation(player, 'SOCOM 17', Locations.location_name_to_id_table['SOCOM 17'], commander_room),
        Locations.MGSLocation(player, 'FA-MAS 14', Locations.location_name_to_id_table['FA-MAS 14'], commander_room),
        Locations.MGSLocation(player, 'FA-MAS 15', Locations.location_name_to_id_table['FA-MAS 15'], commander_room),
        Locations.MGSLocation(player, 'FA-MAS 16', Locations.location_name_to_id_table['FA-MAS 16'], commander_room),
        Locations.MGSLocation(player, 'BOSS: Psycho Mantis', Locations.location_name_to_id_table['BOSS: Psycho Mantis'], commander_room),
        ]
    multiworld.regions.append(commander_room)
    nuke_building_B1.connect(commander_room, 'nuke_building_b1_to_commander_room')

    cave = Region('Cave', player, multiworld)
    cave.locations += [
        Locations.MGSLocation(player, 'Ration 17', Locations.location_name_to_id_table['Ration 17'], cave),
        Locations.MGSLocation(player, 'Ration 18', Locations.location_name_to_id_table['Ration 18'], cave),
        Locations.MGSLocation(player, 'Ration 19', Locations.location_name_to_id_table['Ration 19'], cave),
        Locations.MGSLocation(player, 'SOCOM 18', Locations.location_name_to_id_table['SOCOM 18'], cave),
        Locations.MGSLocation(player, 'SOCOM 19', Locations.location_name_to_id_table['SOCOM 19'], cave),
        Locations.MGSLocation(player, 'FA-MAS 17', Locations.location_name_to_id_table['FA-MAS 17'], cave),
        Locations.MGSLocation(player, 'FA-MAS 18', Locations.location_name_to_id_table['FA-MAS 18'], cave),
        Locations.MGSLocation(player, 'Diazepam 2', Locations.location_name_to_id_table['Diazepam 2'], cave),
        Locations.MGSLocation(player, 'PSG-1 3', Locations.location_name_to_id_table['PSG-1 3'], cave),
        Locations.MGSLocation(player, 'PSG-1 4', Locations.location_name_to_id_table['PSG-1 4'], cave),
        Locations.MGSLocation(player, 'PSG-1 5', Locations.location_name_to_id_table['PSG-1 5'], cave),
        ]
    multiworld.regions.append(cave)
    commander_room.connect(cave)

    underground_passage = Region('Underground Passage', player, multiworld)
    underground_passage.locations += [
        Locations.MGSLocation(player, 'Ration 20', Locations.location_name_to_id_table['Ration 20'], underground_passage),
        Locations.MGSLocation(player, 'SOCOM 20', Locations.location_name_to_id_table['SOCOM 20'], underground_passage),
        Locations.MGSLocation(player, 'FA-MAS 19', Locations.location_name_to_id_table['FA-MAS 19'], underground_passage),
        Locations.MGSLocation(player, 'PSG-1 6', Locations.location_name_to_id_table['PSG-1 6'], underground_passage),
        Locations.MGSLocation(player, 'PSG-1 7', Locations.location_name_to_id_table['PSG-1 7'], underground_passage),
        Locations.MGSLocation(player, 'PSG-1 8', Locations.location_name_to_id_table['PSG-1 8'], underground_passage),
        Locations.MGSLocation(player, 'PSG-1 9', Locations.location_name_to_id_table['PSG-1 9'], underground_passage),
        Locations.MGSLocation(player, 'BOSS: Sniper Wolf I', Locations.location_name_to_id_table['BOSS: Sniper Wolf I'], underground_passage),
        ]
    multiworld.regions.append(underground_passage)
    cave.connect(underground_passage, 'cave_to_underground_passage')

    medi_room = Region('Medi Room', player, multiworld)
    medi_room.locations += [
        Locations.MGSLocation(player, 'Ration 21', Locations.location_name_to_id_table['Ration 21'], medi_room),
        Locations.MGSLocation(player, 'Ration 22', Locations.location_name_to_id_table['Ration 22'], medi_room),
        Locations.MGSLocation(player, 'Handkerchief', Locations.location_name_to_id_table['Handkerchief'], medi_room),
        # Locations.MGSLocation(player, 'Ketchup', Locations.location_name_to_id_table['Ketchup'], medi_room),
        Locations.MGSLocation(player, 'Key Card Level 6', Locations.location_name_to_id_table['Key Card Level 6'], medi_room),
        # Locations.MGSLocation(player, 'Time Bomb 1', Locations.location_name_to_id_table['Time Bomb 1'], medi_room),
        ]
    multiworld.regions.append(medi_room)
    underground_passage.connect(medi_room)

    comm_tower_a = Region('Comm Tower A', player, multiworld)
    comm_tower_a.locations += [
        Locations.MGSLocation(player, 'Ration 23', Locations.location_name_to_id_table['Ration 23'], comm_tower_a),
        Locations.MGSLocation(player, 'Ration 24', Locations.location_name_to_id_table['Ration 24'], comm_tower_a),
        Locations.MGSLocation(player, 'SOCOM 21', Locations.location_name_to_id_table['SOCOM 21'], comm_tower_a),
        Locations.MGSLocation(player, 'SOCOM 22', Locations.location_name_to_id_table['SOCOM 22'], comm_tower_a),
        Locations.MGSLocation(player, 'SOCOM 23', Locations.location_name_to_id_table['SOCOM 23'], comm_tower_a),
        Locations.MGSLocation(player, 'SOCOM 24', Locations.location_name_to_id_table['SOCOM 24'], comm_tower_a),
        Locations.MGSLocation(player, 'SOCOM 25', Locations.location_name_to_id_table['SOCOM 25'], comm_tower_a),
        Locations.MGSLocation(player, 'FA-MAS 20', Locations.location_name_to_id_table['FA-MAS 20'], comm_tower_a),
        Locations.MGSLocation(player, 'FA-MAS 21', Locations.location_name_to_id_table['FA-MAS 21'], comm_tower_a),
        Locations.MGSLocation(player, 'FA-MAS 22', Locations.location_name_to_id_table['FA-MAS 22'], comm_tower_a),
        Locations.MGSLocation(player, 'FA-MAS 23', Locations.location_name_to_id_table['FA-MAS 23'], comm_tower_a),
        Locations.MGSLocation(player, 'FA-MAS 24', Locations.location_name_to_id_table['FA-MAS 24'], comm_tower_a),
        Locations.MGSLocation(player, 'Stun Grenade 5', Locations.location_name_to_id_table['Stun Grenade 5'], comm_tower_a),
        Locations.MGSLocation(player, 'Rope', Locations.location_name_to_id_table['Rope'], comm_tower_a),
        Locations.MGSLocation(player, 'BOSS: Black-outfitted Genome Soldiers I', Locations.location_name_to_id_table['BOSS: Black-outfitted Genome Soldiers I'], comm_tower_a),
        ]
    multiworld.regions.append(comm_tower_a)
    medi_room.connect(comm_tower_a, 'medi_room_to_comm_tower_a')

    walkway = Region('Walkway', player, multiworld)
    walkway.locations += [
        Locations.MGSLocation(player, 'Ration 25', Locations.location_name_to_id_table['Ration 25'], walkway),
        Locations.MGSLocation(player, 'C4 4', Locations.location_name_to_id_table['C4 4'], walkway),
        Locations.MGSLocation(player, 'Stinger 1', Locations.location_name_to_id_table['Stinger 1'], walkway),
        Locations.MGSLocation(player, 'Stinger 2', Locations.location_name_to_id_table['Stinger 2'], walkway),
        ]
    multiworld.regions.append(walkway)
    comm_tower_a.connect(walkway, 'comm_tower_a_to_walkway')

    comm_tower_b = Region('Comm Tower B', player, multiworld)
    comm_tower_b.locations += [
        Locations.MGSLocation(player, 'Ration 26', Locations.location_name_to_id_table['Ration 26'], comm_tower_b),
        Locations.MGSLocation(player, 'SOCOM 26', Locations.location_name_to_id_table['SOCOM 26'], comm_tower_b),
        Locations.MGSLocation(player, 'FA-MAS 25', Locations.location_name_to_id_table['FA-MAS 25'], comm_tower_b),
        Locations.MGSLocation(player, 'FA-MAS 26', Locations.location_name_to_id_table['FA-MAS 26'], comm_tower_b),
        Locations.MGSLocation(player, 'Grenade 7', Locations.location_name_to_id_table['Grenade 7'], comm_tower_b),
        Locations.MGSLocation(player, 'Chaff Grenade 7', Locations.location_name_to_id_table['Chaff Grenade 7'], comm_tower_b),
        Locations.MGSLocation(player, 'Stinger 3', Locations.location_name_to_id_table['Stinger 3'], comm_tower_b),
        Locations.MGSLocation(player, 'Stinger 4', Locations.location_name_to_id_table['Stinger 4'], comm_tower_b),
        Locations.MGSLocation(player, 'Stinger 5', Locations.location_name_to_id_table['Stinger 5'], comm_tower_b),
        ]
    multiworld.regions.append(comm_tower_b)
    walkway.connect(comm_tower_b)

    comm_tower_b_after_hind = Region('Comm Tower B (Hind D[efeated])', player, multiworld)
    comm_tower_b_after_hind.locations += [
        Locations.MGSLocation(player, 'Ration 27', Locations.location_name_to_id_table['Ration 27'], comm_tower_b),
        Locations.MGSLocation(player, 'Ration 28', Locations.location_name_to_id_table['Ration 28'], comm_tower_b),
        Locations.MGSLocation(player, 'SOCOM 27', Locations.location_name_to_id_table['SOCOM 27'], comm_tower_b),
        Locations.MGSLocation(player, 'SOCOM 28', Locations.location_name_to_id_table['SOCOM 28'], comm_tower_b),
        Locations.MGSLocation(player, 'FA-MAS 27', Locations.location_name_to_id_table['FA-MAS 27'], comm_tower_b),
        Locations.MGSLocation(player, 'FA-MAS 28', Locations.location_name_to_id_table['FA-MAS 28'], comm_tower_b),
        Locations.MGSLocation(player, 'FA-MAS 29', Locations.location_name_to_id_table['FA-MAS 29'], comm_tower_b),
        Locations.MGSLocation(player, 'FA-MAS 30', Locations.location_name_to_id_table['FA-MAS 30'], comm_tower_b),
        Locations.MGSLocation(player, 'Chaff Grenade 8', Locations.location_name_to_id_table['Chaff Grenade 8'], comm_tower_b_after_hind),
        Locations.MGSLocation(player, 'PSG-1 10', Locations.location_name_to_id_table['PSG-1 10'], comm_tower_b_after_hind),
        Locations.MGSLocation(player, 'PSG-1 11', Locations.location_name_to_id_table['PSG-1 11'], comm_tower_b_after_hind),
        Locations.MGSLocation(player, 'PSG-1 12', Locations.location_name_to_id_table['PSG-1 12'], comm_tower_b_after_hind),
        Locations.MGSLocation(player, 'BOSS: Stealth Camouflaged Genome Soldiers', Locations.location_name_to_id_table['BOSS: Stealth Camouflaged Genome Soldiers'], comm_tower_b_after_hind),
        ]
    multiworld.regions.append(comm_tower_b_after_hind)
    comm_tower_b.connect(comm_tower_b_after_hind, 'comm_tower_b_to_comm_tower_b_after_hind')

    comm_tower_b_roof = Region('Comm Tower B Roof', player, multiworld)
    hind_d_event = Locations.MGSLocation(player, 'A Hind D?', None, comm_tower_b_roof)
    hind_d_event.place_locked_item(world.create_event('A Hind D[efeated]'))
    comm_tower_b_roof.locations += [
        Locations.MGSLocation(player, 'Ration 29', Locations.location_name_to_id_table['Ration 29'], comm_tower_b_roof),
        Locations.MGSLocation(player, 'Stinger 6', Locations.location_name_to_id_table['Stinger 6'], comm_tower_b_roof),
        Locations.MGSLocation(player, 'BOSS: A Hind D?', Locations.location_name_to_id_table['BOSS: A Hind D?'], comm_tower_b_roof),
        hind_d_event
        ]
    multiworld.regions.append(comm_tower_b_roof)
    comm_tower_b.connect(comm_tower_b_roof, 'comm_tower_b_to_comm_tower_b_roof')

    snowfield = Region('Snow Field', player, multiworld)
    snowfield.locations += [
        Locations.MGSLocation(player, 'PSG-1 13', Locations.location_name_to_id_table['PSG-1 13'], snowfield),
        Locations.MGSLocation(player, 'PSG-1 14', Locations.location_name_to_id_table['PSG-1 14'], snowfield),
        Locations.MGSLocation(player, 'Ration 30', Locations.location_name_to_id_table['Ration 30'], snowfield),
        Locations.MGSLocation(player, 'BOSS: Sniper Wolf II', Locations.location_name_to_id_table['BOSS: Sniper Wolf II'], snowfield),
        ]
    multiworld.regions.append(snowfield)
    comm_tower_b.connect(snowfield, 'comm_tower_b_to_snowfield')

    snowfield_sans_wolf = Region('Snow Field (sans Wolf)', player, multiworld)
    snowfield_sans_wolf.locations += [
        Locations.MGSLocation(player, 'Cardboard Box C', Locations.location_name_to_id_table['Cardboard Box C'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Ration 31', Locations.location_name_to_id_table['Ration 31'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Ration 32', Locations.location_name_to_id_table['Ration 32'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Ration 33', Locations.location_name_to_id_table['Ration 33'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Diazepam 3', Locations.location_name_to_id_table['Diazepam 3'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'SOCOM 29', Locations.location_name_to_id_table['SOCOM 29'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'SOCOM 30', Locations.location_name_to_id_table['SOCOM 30'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'FA-MAS 31', Locations.location_name_to_id_table['FA-MAS 31'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'FA-MAS 32', Locations.location_name_to_id_table['FA-MAS 32'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'FA-MAS 33', Locations.location_name_to_id_table['FA-MAS 33'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Grenade 8', Locations.location_name_to_id_table['Grenade 8'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Grenade 9', Locations.location_name_to_id_table['Grenade 9'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Stun Grenade 6', Locations.location_name_to_id_table['Stun Grenade 6'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Chaff Grenade 9', Locations.location_name_to_id_table['Chaff Grenade 9'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Chaff Grenade 10', Locations.location_name_to_id_table['Chaff Grenade 10'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Claymore 4', Locations.location_name_to_id_table['Claymore 4'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Claymore 5', Locations.location_name_to_id_table['Claymore 5'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Claymore 6', Locations.location_name_to_id_table['Claymore 6'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Nikita 8', Locations.location_name_to_id_table['Nikita 8'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Nikita 9', Locations.location_name_to_id_table['Nikita 9'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Nikita 10', Locations.location_name_to_id_table['Nikita 10'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'Nikita 11', Locations.location_name_to_id_table['Nikita 11'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'PSG-1 15', Locations.location_name_to_id_table['PSG-1 15'], snowfield_sans_wolf),
        Locations.MGSLocation(player, 'PSG-1 16', Locations.location_name_to_id_table['PSG-1 16'], snowfield_sans_wolf),
        ]
    multiworld.regions.append(snowfield_sans_wolf)
    snowfield.connect(snowfield_sans_wolf, 'snowfield_to_snowfield_sans_wolf')

    blast_furnace = Region('Blast Furnace', player, multiworld)
    blast_furnace.locations += [
        Locations.MGSLocation(player, 'Ration 34', Locations.location_name_to_id_table['Ration 34'], blast_furnace),
        Locations.MGSLocation(player, 'Ration 35', Locations.location_name_to_id_table['Ration 35'], blast_furnace),
        Locations.MGSLocation(player, 'SOCOM 31', Locations.location_name_to_id_table['SOCOM 31'], blast_furnace),
        Locations.MGSLocation(player, 'SOCOM 32', Locations.location_name_to_id_table['SOCOM 32'], blast_furnace),
        Locations.MGSLocation(player, 'SOCOM 33', Locations.location_name_to_id_table['SOCOM 33'], blast_furnace),
        Locations.MGSLocation(player, 'FA-MAS 34', Locations.location_name_to_id_table['FA-MAS 34'], blast_furnace),
        Locations.MGSLocation(player, 'C4 5', Locations.location_name_to_id_table['C4 5'], blast_furnace),
        Locations.MGSLocation(player, 'Stun Grenade 7', Locations.location_name_to_id_table['Stun Grenade 7'], blast_furnace),
        Locations.MGSLocation(player, 'Stun Grenade 8', Locations.location_name_to_id_table['Stun Grenade 8'], blast_furnace),
        Locations.MGSLocation(player, 'Nikita 12', Locations.location_name_to_id_table['Nikita 12'], blast_furnace),
        Locations.MGSLocation(player, 'Nikita 13', Locations.location_name_to_id_table['Nikita 13'], blast_furnace),
        Locations.MGSLocation(player, 'PSG-1 17', Locations.location_name_to_id_table['PSG-1 17'], blast_furnace),
        Locations.MGSLocation(player, 'PSG-1 18', Locations.location_name_to_id_table['PSG-1 18'], blast_furnace),
        ]
    multiworld.regions.append(blast_furnace)
    snowfield_sans_wolf.connect(blast_furnace)

    cargo_elevator = Region('Cargo Elevator', player, multiworld)
    cargo_elevator.locations += [
        Locations.MGSLocation(player, 'Ration 36', Locations.location_name_to_id_table['Ration 36'], cargo_elevator),
        Locations.MGSLocation(player, 'FA-MAS 35', Locations.location_name_to_id_table['FA-MAS 35'], cargo_elevator),
        Locations.MGSLocation(player, 'FA-MAS 36', Locations.location_name_to_id_table['FA-MAS 36'], cargo_elevator),
        Locations.MGSLocation(player, 'FA-MAS 37', Locations.location_name_to_id_table['FA-MAS 37'], cargo_elevator),
        Locations.MGSLocation(player, 'FA-MAS 38', Locations.location_name_to_id_table['FA-MAS 38'], cargo_elevator),
        Locations.MGSLocation(player, 'FA-MAS 39', Locations.location_name_to_id_table['FA-MAS 39'], cargo_elevator),
        Locations.MGSLocation(player, 'FA-MAS 40', Locations.location_name_to_id_table['FA-MAS 40'], cargo_elevator),
        Locations.MGSLocation(player, 'FA-MAS 41', Locations.location_name_to_id_table['FA-MAS 41'], cargo_elevator),
        Locations.MGSLocation(player, 'FA-MAS 42', Locations.location_name_to_id_table['FA-MAS 42'], cargo_elevator),
        Locations.MGSLocation(player, 'SOCOM 34', Locations.location_name_to_id_table['SOCOM 34'], cargo_elevator),
        Locations.MGSLocation(player, 'SOCOM 35', Locations.location_name_to_id_table['SOCOM 35'], cargo_elevator),
        Locations.MGSLocation(player, 'Claymore 7', Locations.location_name_to_id_table['Claymore 7'], cargo_elevator),
        Locations.MGSLocation(player, 'Claymore 8', Locations.location_name_to_id_table['Claymore 8'], cargo_elevator),
        Locations.MGSLocation(player, 'Claymore 9', Locations.location_name_to_id_table['Claymore 9'], cargo_elevator),
        Locations.MGSLocation(player, 'BOSS: Black-outfitted Genome Soldiers II', Locations.location_name_to_id_table['BOSS: Black-outfitted Genome Soldiers II'], cargo_elevator),
        ]
    multiworld.regions.append(cargo_elevator)
    blast_furnace.connect(cargo_elevator)

    warehouse = Region('Warehouse', player, multiworld)
    warehouse.locations += [
        Locations.MGSLocation(player, 'Ration 37', Locations.location_name_to_id_table['Ration 37'], warehouse),
        Locations.MGSLocation(player, 'Stinger 7', Locations.location_name_to_id_table['Stinger 7'], warehouse),
        Locations.MGSLocation(player, 'Stinger 8', Locations.location_name_to_id_table['Stinger 8'], warehouse),
        Locations.MGSLocation(player, 'Nikita 14', Locations.location_name_to_id_table['Nikita 14'], warehouse),
        Locations.MGSLocation(player, 'BOSS: Vulcan Raven', Locations.location_name_to_id_table['BOSS: Vulcan Raven'], warehouse),
        ]
    multiworld.regions.append(warehouse)
    cargo_elevator.connect(warehouse)

    warehouse_nt = Region('Warehouse North', player, multiworld)
    warehouse_nt.locations += [
        Locations.MGSLocation(player, 'Ration 38', Locations.location_name_to_id_table['Ration 38'], warehouse_nt),
        Locations.MGSLocation(player, 'Chaff Grenade 11', Locations.location_name_to_id_table['Chaff Grenade 11'], warehouse_nt),
        Locations.MGSLocation(player, 'Stinger 9', Locations.location_name_to_id_table['Stinger 9'], warehouse_nt),
        Locations.MGSLocation(player, 'Stinger 10', Locations.location_name_to_id_table['Stinger 10'], warehouse_nt),
        Locations.MGSLocation(player, 'Stinger 11', Locations.location_name_to_id_table['Stinger 11'], warehouse_nt),
        Locations.MGSLocation(player, 'Stinger 12', Locations.location_name_to_id_table['Stinger 12'], warehouse_nt),
        ]
    multiworld.regions.append(warehouse_nt)
    warehouse.connect(warehouse_nt, 'warehouse_to_warehouse_nt')

    under_ground_base = Region('Underground Base', player, multiworld)
    under_ground_base.locations += [
        Locations.MGSLocation(player, 'Ration 39', Locations.location_name_to_id_table['Ration 39'], under_ground_base),
        Locations.MGSLocation(player, 'SOCOM 36', Locations.location_name_to_id_table['SOCOM 36'], under_ground_base),
        Locations.MGSLocation(player, 'SOCOM 37', Locations.location_name_to_id_table['SOCOM 37'], under_ground_base),
        Locations.MGSLocation(player, 'SOCOM 38', Locations.location_name_to_id_table['SOCOM 38'], under_ground_base),
        Locations.MGSLocation(player, 'FA-MAS 43', Locations.location_name_to_id_table['FA-MAS 43'], under_ground_base),
        Locations.MGSLocation(player, 'FA-MAS 44', Locations.location_name_to_id_table['FA-MAS 44'], under_ground_base),
        Locations.MGSLocation(player, 'FA-MAS 45', Locations.location_name_to_id_table['FA-MAS 45'], under_ground_base),
        Locations.MGSLocation(player, 'FA-MAS 46', Locations.location_name_to_id_table['FA-MAS 46'], under_ground_base),
        Locations.MGSLocation(player, 'Chaff Grenade 12', Locations.location_name_to_id_table['Chaff Grenade 12'], under_ground_base),
        Locations.MGSLocation(player, 'Chaff Grenade 13', Locations.location_name_to_id_table['Chaff Grenade 13'], under_ground_base),
        Locations.MGSLocation(player, 'Chaff Grenade 14', Locations.location_name_to_id_table['Chaff Grenade 14'], under_ground_base),
        Locations.MGSLocation(player, 'Stinger 13', Locations.location_name_to_id_table['Stinger 13'], under_ground_base),
        Locations.MGSLocation(player, 'Stinger 14', Locations.location_name_to_id_table['Stinger 14'], under_ground_base),
        # Locations.MGSLocation(player, 'Pal Key (Found)', Locations.location_name_to_id_table['Pal Key (Found)'], under_ground_base),
        ]
    multiworld.regions.append(under_ground_base)
    warehouse_nt.connect(under_ground_base)

    command_room = Region('Command Room', player, multiworld)
    command_room.locations += [
        Locations.MGSLocation(player, 'Ration 40', Locations.location_name_to_id_table['Ration 40'], command_room),
        ]
    multiworld.regions.append(command_room)
    under_ground_base.connect(command_room, 'underground_base_to_command_room')

    rex_battle = Region('Metal Gear REX - Battle', player, multiworld)
    rex_battle.locations += [
        Locations.MGSLocation(player, 'Ration 42', Locations.location_name_to_id_table['Ration 42'], rex_battle),
        Locations.MGSLocation(player, 'Ration 43', Locations.location_name_to_id_table['Ration 43'], rex_battle),
        Locations.MGSLocation(player, 'Stinger 15', Locations.location_name_to_id_table['Stinger 15'], rex_battle),
        Locations.MGSLocation(player, 'Stinger 16', Locations.location_name_to_id_table['Stinger 16'], rex_battle),
        Locations.MGSLocation(player, 'Stinger 17', Locations.location_name_to_id_table['Stinger 17'], rex_battle),
        Locations.MGSLocation(player, 'Chaff Grenade 15', Locations.location_name_to_id_table['Chaff Grenade 15'], rex_battle),
        Locations.MGSLocation(player, 'Stun Grenade 9', Locations.location_name_to_id_table['Stun Grenade 9'], rex_battle),
        Locations.MGSLocation(player, 'BOSS: Metal Gear REX', Locations.location_name_to_id_table['BOSS: Metal Gear REX'], rex_battle),
        Locations.MGSLocation(player, 'BOSS: Liquid Snake', Locations.location_name_to_id_table['BOSS: Liquid Snake'], rex_battle),
        ]
    multiworld.regions.append(rex_battle)
    under_ground_base.connect(rex_battle, 'under_ground_base_to_rex_battle')

    escape_route = Region('Escape Route', player, multiworld)
    escape_route.locations += [
        Locations.MGSLocation(player, 'Ration 41', Locations.location_name_to_id_table['Ration 41'], escape_route),
        Locations.MGSLocation(player, 'The Best is Yet to Come', Locations.location_name_to_id_table['The Best is Yet to Come'], escape_route),
        ]
    multiworld.regions.append(escape_route)
    rex_battle.connect(escape_route)
