from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule, add_item_rule
from BaseClasses import ItemClassification
if TYPE_CHECKING:
    from . import MGSWorld

def set_rules(world: 'MGSWorld') -> None:
    # These locations can be missed
    # Ensure the world generator doesn't put progression items at these locations
    missable_locations = [
        world.get_location(world.get_full_location_name('Ration 1')),
        world.get_location(world.get_full_location_name('Ration 2')),
        world.get_location(world.get_full_location_name('Ration 3')),
        world.get_location(world.get_full_location_name('Thermal Goggles')),
        world.get_location(world.get_full_location_name('Night Vision Goggles')),
        world.get_location(world.get_full_location_name('Cardboard Box A')),
        world.get_location(world.get_full_location_name('Cardboard Box B')),
        world.get_location(world.get_full_location_name('Cardboard Box C')),
        world.get_location(world.get_full_location_name('Body Armor')),
        world.get_location(world.get_full_location_name('Suppressor')),
        world.get_location(world.get_full_location_name('Mine Detector')),
        world.get_location(world.get_full_location_name('Gas Mask')),
        world.get_location(world.get_full_location_name('Rope')),
    ]

    for loc in missable_locations:
        add_item_rule(loc, 
                      lambda item: item.classification != ItemClassification.progression
                      )
    
    # Ensure 'Victory' item is always received at the end of the game
    world.get_location(world.get_full_location_name('The Best is Yet to Come')).place_locked_item(world.create_item('Victory'))
    # Used to prevent run generator from sending the player to fight the M1 Tank before fighting Ocelot
    world.get_location(world.get_full_location_name('Ocelot Fight')).place_locked_item(world.create_event('Ocelot Fight'))
    # Used to prevent run generator from sending the player to fight Psycho Mantis before fighting Gray Fox
    world.get_location(world.get_full_location_name('Gray Fox Fight')).place_locked_item(world.create_event('Gray Fox Fight'))

    # Ensure specific items have been received before certain points in the game.
    # Ex. C4 is required before fighting Ocelot
    set_rule(world.multiworld.get_entrance('hangar_to_cell', world.player),
            lambda state: state.has('SOCOM', world.player))
    set_rule(world.multiworld.get_entrance('armory_to_cell', world.player),
            lambda state: state.has('SOCOM', world.player))
    set_rule(world.multiworld.get_entrance('armory_to_armory_lvl1', world.player),
             lambda state: state.has('Key Card', world.player, 1))
    set_rule(world.multiworld.get_entrance('armory_to_armory_lvl2', world.player),
             lambda state: state.has('Key Card', world.player, 2))
    set_rule(world.multiworld.get_entrance('armory_to_armory_lvl3', world.player),
             lambda state: state.has('Key Card', world.player, 3))
    set_rule(world.multiworld.get_entrance('armory_to_armory_lvl5', world.player),
             lambda state: state.has('Key Card', world.player, 5))
    set_rule(world.multiworld.get_entrance('armory_to_armory_sth', world.player),
             lambda state: state.has('C4', world.player))
    set_rule(world.multiworld.get_entrance('hangar_to_canyon', world.player),
             lambda state: state.has('Key Card', world.player, 2)
             and state.has('Chaff Grenade', world.player)
             and state.has('Grenade', world.player)
             and state.has('Mine Detector', world.player)
             and state.has('Ocelot Fight', world.player))
    set_rule(world.multiworld.get_entrance('canyon_to_nuke_building_1', world.player),
             lambda state: state.has('Key Card', world.player, 3))
    set_rule(world.multiworld.get_entrance('nuke_building_1_to_nuke_building_b2', world.player),
             lambda state: state.has('Nikita', world.player))
    set_rule(world.multiworld.get_entrance('nuke_building_b1_to_nuke_building_b2', world.player),
             lambda state: state.has('Nikita', world.player))
    set_rule(world.multiworld.get_entrance('nuke_building_b1_to_nuke_bulding_b1_lvl4', world.player),
             lambda state: state.has('Key Card', world.player, 4))
    set_rule(world.multiworld.get_entrance('nuke_building_b1_to_nuke_bulding_b1_lvl5', world.player),
             lambda state: state.has('Key Card', world.player, 5))
    set_rule(world.multiworld.get_entrance('nuke_bulding_b2_to_nuke_building_b2_lvl4', world.player),
             lambda state: state.has('Key Card', world.player, 4))
    set_rule(world.multiworld.get_entrance('nuke_bulding_b2_to_nuke_building_b2_lvl6', world.player),
             lambda state: state.has('Key Card', world.player, 6))
    set_rule(world.multiworld.get_entrance('nuke_building_b1_to_commander_room', world.player),
             lambda state: state.has('Key Card', world.player, 5) and state.has('Gray Fox Fight', world.player))
    set_rule(world.multiworld.get_entrance('cave_to_underground_passage', world.player),
             lambda state: state.has('PSG-1', world.player, 2))
    set_rule(world.multiworld.get_entrance('medi_room_to_comm_tower_a', world.player),
             lambda state: state.has('Key Card', world.player, 6) and state.has('Medicine', world.player))
    set_rule(world.multiworld.get_entrance('comm_tower_a_to_walkway', world.player),
             lambda state: state.has('Rope', world.player))
    set_rule(world.multiworld.get_entrance('comm_tower_b_to_comm_tower_b_roof', world.player),
             lambda state: state.has('Stinger', world.player, 2))
    set_rule(world.multiworld.get_entrance('comm_tower_b_to_comm_tower_b_after_hind', world.player),
             lambda state: state.has('A Hind D[efeated]', world.player))
    set_rule(world.multiworld.get_entrance('comm_tower_b_to_snowfield', world.player),
             lambda state: state.has('PSG-1', world.player, 2))
    set_rule(world.multiworld.get_entrance('warehouse_to_warehouse_nt', world.player),
             lambda state: state.has('Key Card', world.player, 7))
    set_rule(world.multiworld.get_entrance('underground_base_to_command_room', world.player),
             lambda state: state.has('Pal Key', world.player))
    set_rule(world.multiworld.get_entrance('under_ground_base_to_rex_battle', world.player),
             lambda state: state.has('Stinger', world.player, 2))
    
    # Tell the run generator which items are required for victory
    match world.run_goal:
        case 0: # Game Completion
            world.multiworld.completion_condition[world.player] = lambda state: state.has('Victory', world.player)
        case 1: # Boss Blitz
            world.get_location(world.get_full_location_name('BOSS: Heavily Armed Genome Soldiers')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: Revolver Ocelot')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: M1 Tank')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: Gray Fox')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: Psycho Mantis')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: Sniper Wolf I')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: Black-outfitted Genome Soldiers I')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: A Hind D?')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: Stealth Camouflaged Genome Soldiers')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: Sniper Wolf II')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: Black-outfitted Genome Soldiers II')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: Vulcan Raven')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: Metal Gear REX')).place_locked_item(world.create_item('Boss Dogtag'))
            world.get_location(world.get_full_location_name('BOSS: Liquid Snake')).place_locked_item(world.create_item('Boss Dogtag'))
            world.multiworld.completion_condition[world.player] = lambda state: state.has('Boss Dogtag', world.player, world.boss_goal)
        case 2: # Dogtag Collection
            world.multiworld.completion_condition[world.player] = lambda state: state.has('Dogtag', world.player, world.dogtag_goal)