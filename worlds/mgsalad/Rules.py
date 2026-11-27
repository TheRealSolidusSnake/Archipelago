from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule, add_item_rule, add_rule
from .Regions import BOSS_ORDER
from BaseClasses import ItemClassification
if TYPE_CHECKING:
    from . import MGSWorld

def set_rules(world: 'MGSWorld') -> None:
    # These locations could be missed, but now we hold them until they're checked in-game
    # We're leaving the list intact so we can roll it back at any given point
    # but also because I'm lazy and it was a lot easier to just leave them like this XD
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
        world.get_location(world.get_full_location_name('Camera')),
        world.get_location(world.get_full_location_name('Suppressor')),
        world.get_location(world.get_full_location_name('Mine Detector')),
        world.get_location(world.get_full_location_name('Gas Mask')),
        world.get_location(world.get_full_location_name('Rope')),
    ]
	
    # Keep this list for documentation and easy rollback.
    # The client now holds these items from the player until their physical pickup in-game
    # has been checked, so progression items are now allowed at these locations.

    # for loc in missable_locations:
    #     add_item_rule(loc, 
    #                   lambda item: not item.advancement
    #                   )
    
    # Ensure 'Victory' item is always received at the end of the game
    world.get_location(world.get_full_location_name('The Best is Yet to Come')).place_locked_item(world.create_item('Victory'))
    set_rule(world.get_location(world.get_full_location_name('BOSS: Black-outfitted Genome Soldiers I')),
             lambda state: state.has('Rope', world.player))

    # Ensure specific items have been received before certain points in the game.
    # Ex. C4 is required before fighting Ocelot
    set_rule(world.multiworld.get_entrance('hangar_to_cell', world.player),
            lambda state: state.has('SOCOM', world.player))
    set_rule(world.multiworld.get_entrance('armory_to_cell', world.player),
            lambda state: state.has('SOCOM', world.player))
    for location_name in ('Cell - SOCOM 5', 'Cell - SOCOM 6'):
        set_rule(world.get_location(location_name),
                 lambda state: state.has('Progressive Key Card', world.player, 1))

    set_rule(world.multiworld.get_entrance('armory_to_armory_lvl1', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 1))
    set_rule(world.multiworld.get_entrance('armory_to_armory_lvl2', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 2))
    set_rule(world.multiworld.get_entrance('armory_to_armory_lvl3', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 3))
    set_rule(world.multiworld.get_entrance('armory_to_armory_lvl5', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 5)
             and state.has('Mine Detector', world.player))
    # Easy logic allows either explosive weapon to destroy every Armory blast wall.
    # Hard logic requires C4 specifically for every wall, including the wall leading to Ocelot.
    if world.logic_difficulty == 0:  # Easy
        set_rule(world.multiworld.get_entrance('armory_to_armory_sth_c4', world.player),
                 lambda state: state.has('C4', world.player)
                 or state.has('Stinger', world.player))
        set_rule(world.multiworld.get_entrance('armory_to_armory_sth', world.player),
                 lambda state: state.has('C4', world.player)
                 or state.has('Stinger', world.player))
    else:  # Hard
        set_rule(world.multiworld.get_entrance('armory_to_armory_sth_c4', world.player),
                 lambda state: state.has('C4', world.player))
        set_rule(world.multiworld.get_entrance('armory_to_armory_sth', world.player),
                 lambda state: state.has('C4', world.player))
    set_rule(world.multiworld.get_entrance('armory_sth_c4_to_armory_sth_c4_lvl4', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 4))
    set_rule(world.multiworld.get_entrance('armory_sth_c4_to_armory_sth_c4_lvl6', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 6))
    set_rule(world.get_entrance('hangar_to_hangar_lvl1'),
             lambda state: state.has('Progressive Key Card', world.player, 1))
    set_rule(world.get_entrance('hangar_to_hangar_lvl2'),
             lambda state: state.has('Progressive Key Card', world.player, 2))
    if world.logic_difficulty == 0:  # Easy
        set_rule(world.multiworld.get_entrance('hangar_to_canyon', world.player),
                 lambda state: state.has('Progressive Key Card', world.player, 2)
                 and state.has('Chaff Grenade', world.player)
                 and (state.has('Grenade', world.player)
                 or state.has('Stinger', world.player))
                 and state.has('Mine Detector', world.player))
    else:  # Hard
        set_rule(world.multiworld.get_entrance('hangar_to_canyon', world.player),
                 lambda state: state.has('Progressive Key Card', world.player, 2)
                 and state.has('Chaff Grenade', world.player)
                 and state.has('Grenade', world.player))
    set_rule(world.multiworld.get_entrance('canyon_to_nuke_building_1', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 3))
    # Gas Mask is a physical pickup in B2; requiring it here would lock its own check.
    for entrance_name in (
        'nuke_building_1_to_nuke_building_b2',
        'nuke_building_b1_to_nuke_building_b2',
    ):
        set_rule(world.multiworld.get_entrance(entrance_name, world.player),
                 lambda state: state.has('Nikita', world.player))
    set_rule(world.multiworld.get_entrance('nuke_building_b1_to_nuke_bulding_b1_lvl4', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 4))
    set_rule(world.multiworld.get_entrance('nuke_building_b1_to_nuke_bulding_b1_lvl5', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 5))
    set_rule(world.multiworld.get_entrance('nuke_bulding_b2_to_nuke_building_b2_lvl4', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 4))
    set_rule(world.multiworld.get_entrance('nuke_bulding_b2_to_nuke_building_b2_lvl6', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 6))
    set_rule(world.multiworld.get_entrance('nuke_building_b1_to_commander_room', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 5)
             and state.has('Nikita', world.player))
    set_rule(world.multiworld.get_entrance('cave_to_underground_passage', world.player),
             lambda state: state.has('PSG-1', world.player, 2))
    if world.logic_difficulty == 0:  # Easy
        set_rule(world.multiworld.get_entrance('medi_room_to_comm_tower_a', world.player),
                 lambda state: state.has('Progressive Key Card', world.player, 6)
                 and state.has('Medicine', world.player))
    else:  # Hard
        set_rule(world.multiworld.get_entrance('medi_room_to_comm_tower_a', world.player),
                 lambda state: state.has('Progressive Key Card', world.player, 6))
    set_rule(world.multiworld.get_entrance('comm_tower_a_to_walkway', world.player),
             lambda state: state.has('Rope', world.player))
    set_rule(world.multiworld.get_entrance('comm_tower_b_to_comm_tower_b_roof', world.player),
             lambda state: state.has('Stinger', world.player, 2))
    set_rule(world.multiworld.get_entrance('comm_tower_b_to_comm_tower_b_after_hind', world.player),
             lambda state: state.has('Stinger', world.player, 2))
    set_rule(world.multiworld.get_entrance('comm_tower_b_to_snowfield', world.player),
             lambda state: state.has('PSG-1', world.player, 2))

    # The Stinger ammo room in Snow Field is locked behind a level 7 door.
    for location_name in ('Stinger 10', 'Stinger 11', 'Stinger 12', 'Stinger 13'):
        set_rule(world.get_location(world.get_full_location_name(location_name)),
                 lambda state: state.has('Progressive Key Card', world.player, 7))
    set_rule(world.multiworld.get_entrance('warehouse_to_warehouse_nt', world.player),
             lambda state: state.has('Progressive Key Card', world.player, 7))
    # The first Command Room ration is available before using the PAL Key.
    # The second one is behind the PAL Key sequence.
    set_rule(world.get_location(world.get_full_location_name('Ration 44')),
             lambda state: state.has('Pal Key', world.player))
    set_rule(world.multiworld.get_entrance('under_ground_base_to_rex_battle', world.player),
             lambda state: state.has('Stinger', world.player, 2) and state.has('Pal Key', world.player))
    
    # Every story transition requires the preceding boss, without replacing item rules.
    boss_gates = {
        'armory_to_armory_sth': 0,
        'armory_to_armory_sth_c4': 0,
        'hangar_to_canyon': 1,
        'canyon_to_nuke_building_1': 2,
        'nuke_building_b1_to_commander_room': 3,
        'commander_room_to_cave': 4,
        'armory_to_armory_lvl5': 4,
        'underground_passage_to_medi_room': 5,
        'medi_room_to_comm_tower_a': 5,
        'comm_tower_a_to_walkway': 6,
        'comm_tower_b_to_comm_tower_b_after_hind': 7,
        'comm_tower_b_to_snowfield': 8,
        'snowfield_to_snowfield_sans_wolf': 9,
        'cargo_elevator_to_warehouse': 10,
        'warehouse_to_warehouse_nt': 11,
        'rex_battle_to_escape_route': 13,
    }
    for entrance_name, boss_index in boss_gates.items():
        add_rule(world.get_entrance(entrance_name),
                 lambda state, event=BOSS_ORDER[boss_index][2]: state.has(event, world.player))

    # Liquid shares a region with REX; enforce boss order on individual checks too.
    for index, (boss_name, event_name, item_name) in enumerate(BOSS_ORDER):
        boss = world.get_location(world.get_full_location_name(boss_name))
        if index:
            add_rule(boss, lambda state, previous=BOSS_ORDER[index - 1][2]: state.has(previous, world.player))
        event = world.get_location(event_name)
        # Mirror the actual boss check rule, including Rope and previous boss.
        if getattr(world.multiworld, 'generation_is_fake', False) and getattr(world.multiworld, 'enforce_deferred_connections', 'default') != 'off':
            set_rule(event, lambda state, boss=boss, bit=index:
                     bool(world.boss_event_mask & (1 << bit)) and boss.access_rule(state))
        else:
            set_rule(event, lambda state, boss=boss: boss.access_rule(state))

    # Scripted rewards only become available after the relevant fight.
    for location_name, boss_index in (
        ('Key Card Level 1', 0),
        ('Key Card Level 2', 1),
        ('Key Card Level 3', 2),
        ('Key Card Level 4', 3),
        ('Key Card Level 5', 3),
        ('Pal Key', 3),
        ('Key Card Level 7', 11),
    ):
        add_rule(world.get_location(world.get_full_location_name(location_name)),
                 lambda state, event=BOSS_ORDER[boss_index][2]: state.has(event, world.player))

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