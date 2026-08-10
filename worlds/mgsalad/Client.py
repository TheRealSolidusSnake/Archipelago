import logging
import json
import time
import hashlib
from typing import TYPE_CHECKING, Any

from pathlib import Path

from NetUtils import ClientStatus, NetworkItem
from Utils import user_path

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .RAMAddress import RAM
# these imports aren't used in this file, but are required to be here for Archipelago to function
from . import Locations
from . import Items
from . import Options
from . import Regions

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

# TODO MGS: Add support for DeathLink (give the player a Time Bomb with 1 second left)
# TODO MGS: Make increasing max health a "useful" item
# TODO MGS: Refactor different sections of game_watcher to their own functions

logger = logging.getLogger('Client')


def to_u16_bytes(value: int) -> bytes:
    # PSX inventory/ammo fields are unsigned 16-bit. Values can legitimately
    # reach 0xFFFF in saves; AP rewards after that must not overflow
	# or else the client will refuse to send/receive anymore
    value = max(0, min(int(value), 0xFFFF))
    return value.to_bytes(length=2, byteorder='little')

def sanitize_save_component(value: object, max_length: int = 80) -> str:
    """Return a Windows-safe, collision-resistant filename component."""
    original = str(value)
    sanitized = ''.join(
        character if character.isalnum() or character in ('-', '_', '.') else '_'
        for character in original
    ).strip(' ._')
    sanitized = sanitized or 'unknown'

    # If sanitizing changed the seed name, append a short digest so two seed
    # names which differ only by invalid filename characters cannot collide.
    if sanitized != original or len(sanitized) > max_length:
        digest = hashlib.sha256(original.encode('utf-8')).hexdigest()[:8]
        prefix_length = max(1, max_length - len(digest) - 1)
        sanitized = f'{sanitized[:prefix_length]}_{digest}'

    return sanitized

def cmd_check_goal(self: "BizHawkClientCommandProcessor") -> None:
    """Check progress towards goal"""
    from worlds._bizhawk.context import BizHawkClientContext
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, MetalGearSolidClient)
    if client.run_goal:
        match client.run_goal:
            case 0:
                logger.info('Run Goal: Game Completion')
            case 1:
                logger.info('Run Goal: Boss Blitz')
                logger.info(f"Defeated {client.save_state['dogtag_counter']} of {client.boss_goal} bosses.")
            case 2:
                logger.info('Run Goal: Dogtag Collection')
                logger.info(f"Collected {client.save_state['dogtag_counter']} of {client.dogtag_goal} dogtags.")
            case _:
                logger.info(f'[MGS: Masala Garden Salad] Error checking goal: {client.run_goal}')
    else:
        logger.info('No slot data. Connect to a server and try again.')

def cmd_check_collection(self: "BizHawkClientCommandProcessor", region='here') -> None:
    """Check which locations have been checked for a region. Can also specify 'all'."""
    from worlds._bizhawk.context import BizHawkClientContext
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, MetalGearSolidClient)
    checks_per_region_tracker: dict[str, dict[str, int]] = client.save_state['checks_per_region_tracker']
    logger.info('==== Current Item Collection Log ====')
    if region == 'here':
        region = client.current_region
    if region == 'all':
        for re in checks_per_region_tracker.keys():
            logger.info(f'{re}:')
            items = [item_name for item_name in checks_per_region_tracker[re].keys() if '_max' not in item_name]
            for item in items:
                item_max = ''.join([item,'_max'])
                logger.info(f'  - {item}: {checks_per_region_tracker[re][item]} of {checks_per_region_tracker[re][item_max]}')
    elif region in client.save_state['regions']:
        logger.info(f'{region}:')
        items = [item_name for item_name in checks_per_region_tracker[region].keys() if '_max' not in item_name]
        for item in items:
            item_max = ''.join([item,'_max'])
            logger.info(f'  - {item}: {checks_per_region_tracker[region][item]} of {checks_per_region_tracker[region][item_max]}')
    else:
        logger.info('Region name not recognized.')
    logger.info('=====================================')
    logger.info('NOTE: Locations labeled missable can now contain progression. Matching items are held until the physical pickup is checked.')

def cmd_kill_mantis(self: "BizHawkClientCommandProcessor") -> None:
    """Kill Psycho Mantis in case you cannot change controller ports. Do not use during 'HIDEO'! Needs to be used at each phase of his fight. Need to last hit when Mantis is at 0 HP"""
    from worlds._bizhawk.context import BizHawkClientContext
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, MetalGearSolidClient)
    client.kill_mantis_command = True

# Single source of truth for "which Key Card level does this cutscene text belong to".
# Gray Fox happened to want to send Key Card 5 from Nuke Building B1 for some reason. (since we added regions, anyway)
# So we try to lock the key cards to their appropriate locations.
KEY_CARD_LEVEL_BY_CUTSCENE_BYTES: dict[bytes, int] = {
    RAM.key_card_level_1_cutscene_bytes: 1,
    RAM.key_card_level_2_cutscene_bytes: 2,
    RAM.key_card_level_3_cutscene_bytes: 3,
    RAM.key_card_level_4_cutscene_bytes: 4,  # shared with 'BOSS: Gray Fox'
    RAM.key_card_level_5_cutscene_bytes: 5,
    RAM.key_card_level_6_cutscene_bytes: 6,  # shared with 'Otacon Gifts'
    RAM.key_card_level_7_cutscene_bytes: 7,  # shared with 'BOSS: Vulcan Raven'
}

class MetalGearSolidClient(BizHawkClient):
    game = "MGS: Masala Garden Salad"
    system = "PSX"
    patch_suffix = ".apmgsalad"
    build_version = "1.0.0"

    # These are physical pickups that disappear if the player already has the item.
    # If AP sends one early, hold it until the matching in-game location has been checked.
    # This allows us to have progression there, and it prevents the need to manually send these locations.
    HOLD_MISSABLE_ITEMS = {
        'Cardboard Box A': 'cbox_a_location_counter',
        'Cardboard Box B': 'cbox_b_location_counter',
        'Cardboard Box C': 'cbox_c_location_counter',
        'Night Vision Goggles': 'night_vision_goggles_location_counter',
        'Thermal Goggles': 'thermal_goggles_location_counter',
        'Gas Mask': 'gasmask_location_counter',
        'Body Armor': 'body_armor_location_counter',
        'Camera': 'camera_location_counter',
        'Mine Detector': 'mine_detector_location_counter',
        'Rope': 'rope_location_counter',
        'Suppressor': 'suppressor_location_counter',
    }

    def __init__(self):
        super().__init__()

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd == 'Connected':
            self.bizhawk_ctx = ctx
            self.initalize_client()

    def initalize_client(self):
        logger.info(f'[MGS: Masala Garden Salad] Client build: {self.build_version}')
        if self.bizhawk_ctx.slot_data:
            self.run_goal = self.bizhawk_ctx.slot_data['run_goal']
            self.boss_goal = self.bizhawk_ctx.slot_data['boss_goal']
            self.dogtag_goal = self.bizhawk_ctx.slot_data['dogtag_goal']
            self.logic_difficulty = self.bizhawk_ctx.slot_data.get('logic_difficulty', 0)
        else:
            self.logic_difficulty = 0
        self.run_once = True
        self.max_items = 1000
        self.locations_to_send = []
        self.received_item_count = 0
        self.location_name_to_server_location_id = {}
        self.kill_mantis_command = False
        self.current_region = ''
        # The identifying cutscene bytes and the scripted Key Card RAM increase
        # do not always appear during the same client poll. Briefly retain each
        # signal so they can be paired without guessing from the counter alone.
        self.recent_key_card_cutscene_level: int | None = None
        self.recent_key_card_cutscene_time = 0.0
        self.pending_key_card_level: int | None = None
        self.pending_key_card_time = 0.0
        # The game restores Snake's pre-capture inventory as he leaves the
        # Medi Room. For a few watcher polls those restored counts can look
        # like duplicate pickups, even though no world item was collected.
        self.suppress_post_capture_ration_messages_until = 0.0
        # A denied pickup can remain visible for a few watcher polls while the
        # ammo rollback is being written. Throttle identical access warnings so
        # one attempted pickup produces one useful message instead of log spam.
        self.blocked_pickup_message_times: dict[tuple[str, str, str], float] = {}

        # Keep each Archipelago seed and slot in its own client save. This prevents
        # one run's counters and received-item history from carrying into another
        # multiworld while still allowing reconnects to resume normally.
        # BizHawkClientContext stores the RoomInfo seed in server_seed_name.
        # Older/custom client contexts may expose seed_name instead, so retain that
        # as a compatibility fallback. Do not use the connection address (such as
        # localhost), because multiple multiworlds can be hosted at the same address.
        seed_name = (
            getattr(self.bizhawk_ctx, 'server_seed_name', None)
            or getattr(self.bizhawk_ctx, 'seed_name', None)
            or 'unknown_seed'
        )
        slot_number = self.bizhawk_ctx.slot if self.bizhawk_ctx.slot is not None else 0

        # Archipelago's automatically generated seed names commonly begin with
        # "Archipelago_". The mgsalad prefix already identifies the file, so
        # omit that redundant prefix from the per-seed filename.
        filename_seed_name = seed_name
        if filename_seed_name.casefold().startswith('archipelago_'):
            filename_seed_name = filename_seed_name[len('Archipelago_'):]

        seed_component = sanitize_save_component(filename_seed_name)
        self.save_file = Path(user_path(
            f'mgsalad_{seed_component}_slot{slot_number}.json'
        ))

        if self.save_file.exists():
            with open(self.save_file) as save:
                try:
                    self.save_state: dict[str, Any] = json.load(save)
                    logger.info(
                        f'[MGS: Masala Garden Salad] Loaded save for seed "{seed_name}", slot {slot_number}:'
                    )
                    logger.info(f'[MGS: Masala Garden Salad] {self.save_file}')
                except json.JSONDecodeError:
                    logger.info(
                        f'[MGS: Masala Garden Salad] Save file was unreadable. Creating a fresh save for seed "{seed_name}", slot {slot_number}.'
                    )
                    self.save_state = self.initalize_save_data()
                    with open(self.save_file, 'w') as save:
                        json.dump(self.save_state, save)
        else:
            self.save_state: dict[str, Any] = self.initalize_save_data()
            logger.info(
                f'[MGS: Masala Garden Salad] No save found for seed "{seed_name}", slot {slot_number}. Creating a new save:'
            )
            logger.info(f'[MGS: Masala Garden Salad] {self.save_file}')
            with open(self.save_file, 'w') as save:
                json.dump(self.save_state, save)

        # The Archipelago Server has an ID for all locations in the multiworld, this creates a dictionary where location names get mapped to their ID on the server
        self.save_state['region_item_location_names'] = self.build_region_item_location_names()
        self.save_state.setdefault('viewed_pal_key_cutscene_text', [])
        self.save_state.setdefault('medi_room_otacon_gifts_received', False)
        self.save_state.setdefault('has_defeated_hind', False)
        self.save_state.setdefault('has_camera', False)
        self.save_state.setdefault('camera_counter', 0)
        self.save_state.setdefault('camera_location_counter', 1)
        self.save_state.setdefault('camera_max_location_counter', 1)
        self.save_state.setdefault('endgame_inventory_locked', False)
        self.save_state.setdefault('endgame_rations_last_seen', None)
        self.save_state.setdefault('pending_endgame_items', [])

        for server_location in self.bizhawk_ctx.server_locations:
            self.location_name_to_server_location_id[self.bizhawk_ctx.location_names.lookup_in_game(code=server_location, game_name='MGS: Masala Garden Salad')] = server_location

        for full_name, server_location in list(self.location_name_to_server_location_id.items()):
            if ' - ' in full_name:
                short_name = full_name.rsplit(' - ', 1)[1]
                self.location_name_to_server_location_id.setdefault(short_name, server_location)

        hind_location_id = self.resolve_location_id('BOSS: A Hind D?')
        rex_location_id = self.resolve_location_id('BOSS: Metal Gear REX')
        checked_locations = getattr(self.bizhawk_ctx, 'checked_locations', set())
        if hind_location_id is not None and hind_location_id in checked_locations:
            self.save_state['has_defeated_hind'] = True
        if rex_location_id is not None and rex_location_id in checked_locations:
            self.save_state['endgame_inventory_locked'] = True

        # Keep the per-region counters and maximums aligned with the actual
        # regional AP location names. This also migrates older save files whose
        # Comm Tower B counters combined the pre-Hind and post-Hind areas.
        self.synchronize_region_check_trackers()

    def has_received_ap_item(self, item_name: str) -> bool:
        """Return whether Archipelago has ever sent this item to the player."""
        for network_item in self.bizhawk_ctx.items_received:
            received_name = self.bizhawk_ctx.item_names.lookup_in_game(
                code=network_item.item,
                game_name='MGS: Masala Garden Salad',
            )
            if received_name == item_name:
                return True
        return False

    def resolve_location_id(self, location_name: str) -> int | None:
        # Direct lookup first. 
		# This covers exact server names and the short helper names.
        location_id = self.location_name_to_server_location_id.get(location_name)
        if location_id is not None:
            return location_id

        # Known short-name aliases that should resolve to an AP location.
        location_aliases = {
            'BOSS: Metal Gear REX': 'Metal Gear REX - BOSS: Metal Gear REX',
            'BOSS: Liquid Snake': 'Metal Gear REX - BOSS: Liquid Snake',

            # Compatibility for seeds/clients created while the restored Armory
            # C4 room was represented as one region. The current layout splits
            # the Level 1 C4 and Level 2 FA-MAS checks into their actual doors.
        }

        alias_name = location_aliases.get(location_name)
        if alias_name is not None:
            location_id = self.location_name_to_server_location_id.get(alias_name)
            if location_id is not None:
                return location_id

        # Fall back to a unique suffix match instead of crashing.
        suffix = f' - {location_name}'
        matches = {
            server_id
            for full_name, server_id in self.location_name_to_server_location_id.items()
            if full_name.endswith(suffix)
        }

        if len(matches) == 1:
            return next(iter(matches))

        if len(matches) > 1:
            logger.info(f'[MGS: Masala Garden Salad] Location name is ambiguous on server: {location_name}')
        else:
            logger.info(f'[MGS: Masala Garden Salad] Location not found on server: {location_name}')

        return None

    def queue_location(self, location_name: str) -> bool:
        location_id = self.resolve_location_id(location_name)

        if location_id is None:
            return False

        if location_id not in self.locations_to_send:
            self.locations_to_send.append(location_id)

        return True

    async def check_received_victory(self, ctx: "BizHawkClientContext") -> None:
        """Report Game Completion as soon as the server sends the Victory item.
        """
        if self.run_goal != 0 or ctx.finished_game:
            return

        for item in ctx.items_received:
            local_item_name = ctx.item_names.lookup_in_game(
                code=item.item, game_name='MGS: Masala Garden Salad'
            )
            if local_item_name == 'Victory':
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                ctx.finished_game = True
                return

    def missable_location_has_been_sent(self, item_name: str) -> bool:
        location_counter_name = self.HOLD_MISSABLE_ITEMS.get(item_name)
        if location_counter_name is None:
            return False

        # These counters start at 1 and are incremented after the location is queued.
        return self.save_state[location_counter_name] > 1

    def hold_missable_item(self, item_name: str) -> bool:
        if item_name not in self.HOLD_MISSABLE_ITEMS:
            return False

        return not self.missable_location_has_been_sent(item_name)

    def give_missable_item(self, item_name: str, write_list: list) -> None:
        match item_name:
            case 'Cardboard Box A':
                self.save_state['has_cbox_a'] = True
                self.save_state['cbox_a_counter'] = 1
                write_list.append((RAM.cbox_a_count_address, to_u16_bytes(self.save_state['cbox_a_counter']), 'MainRAM'))
                write_list.append((RAM.cbox_a_death_count_address, to_u16_bytes(self.save_state['cbox_a_counter']), 'MainRAM'))
            case 'Cardboard Box B':
                self.save_state['has_cbox_b'] = True
                self.save_state['cbox_b_counter'] = 1
                write_list.append((RAM.cbox_b_count_address, to_u16_bytes(self.save_state['cbox_b_counter']), 'MainRAM'))
                write_list.append((RAM.cbox_b_death_count_address, to_u16_bytes(self.save_state['cbox_b_counter']), 'MainRAM'))
            case 'Cardboard Box C':
                self.save_state['has_cbox_c'] = True
                self.save_state['cbox_c_counter'] = 1
                write_list.append((RAM.cbox_c_count_address, to_u16_bytes(self.save_state['cbox_c_counter']), 'MainRAM'))
                write_list.append((RAM.cbox_c_death_count_address, to_u16_bytes(self.save_state['cbox_c_counter']), 'MainRAM'))
            case 'Night Vision Goggles':
                self.save_state['has_night_vision_goggles'] = True
                self.save_state['night_vision_goggles_counter'] = 1
                write_list.append((RAM.nvg_count_address, to_u16_bytes(self.save_state['night_vision_goggles_counter']), 'MainRAM'))
                write_list.append((RAM.nvg_death_count_address, to_u16_bytes(self.save_state['night_vision_goggles_counter']), 'MainRAM'))
            case 'Thermal Goggles':
                self.save_state['has_thermal_goggles'] = True
                self.save_state['thermal_goggles_counter'] = 1
                write_list.append((RAM.therm_g_count_address, to_u16_bytes(self.save_state['thermal_goggles_counter']), 'MainRAM'))
                write_list.append((RAM.therm_g_death_count_address, to_u16_bytes(self.save_state['thermal_goggles_counter']), 'MainRAM'))
            case 'Gas Mask':
                self.save_state['has_gasmask'] = True
                self.save_state['gasmask_counter'] = 1
                write_list.append((RAM.gasmask_count_address, to_u16_bytes(self.save_state['gasmask_counter']), 'MainRAM'))
                write_list.append((RAM.gasmask_death_count_address, to_u16_bytes(self.save_state['gasmask_counter']), 'MainRAM'))
            case 'Body Armor':
                self.save_state['has_body_armor'] = True
                self.save_state['body_armor_counter'] = 1
                write_list.append((RAM.b_armor_count_address, to_u16_bytes(self.save_state['body_armor_counter']), 'MainRAM'))
                write_list.append((RAM.b_armor_death_count_address, to_u16_bytes(self.save_state['body_armor_counter']), 'MainRAM'))
            case 'Camera':
                self.save_state['has_camera'] = True
                self.save_state['camera_counter'] = 1
                write_list.append((RAM.camera_count_address, to_u16_bytes(self.save_state['camera_counter']), 'MainRAM'))
                write_list.append((RAM.camera_death_count_address, to_u16_bytes(self.save_state['camera_counter']), 'MainRAM'))
            case 'Mine Detector':
                self.save_state['has_mine_detector'] = True
                self.save_state['mine_detector_counter'] = 1
                write_list.append((RAM.mine_d_count_address, to_u16_bytes(self.save_state['mine_detector_counter']), 'MainRAM'))
                write_list.append((RAM.mind_d_death_count_address, to_u16_bytes(self.save_state['mine_detector_counter']), 'MainRAM'))
            case 'Rope':
                self.save_state['has_rope'] = True
                self.save_state['rope_counter'] = 1
                write_list.append((RAM.rope_count_address, to_u16_bytes(self.save_state['rope_counter']), 'MainRAM'))
                write_list.append((RAM.rope_death_count_address, to_u16_bytes(self.save_state['rope_counter']), 'MainRAM'))
            case 'Suppressor':
                self.save_state['has_suppressor'] = True
                self.save_state['suppressor_counter'] = 1
                write_list.append((RAM.suppressor_count_address, to_u16_bytes(self.save_state['suppressor_counter']), 'MainRAM'))
                write_list.append((RAM.suppressor_death_count_address, to_u16_bytes(self.save_state['suppressor_counter']), 'MainRAM'))

    def release_pending_missable_items(self, write_list: list) -> bool:
        pending_items = self.save_state.get('pending_missable_items', [])
        if not pending_items:
            return False

        still_waiting = []
        release_items = False

        for item_name in pending_items:
            if self.missable_location_has_been_sent(item_name):
                self.give_missable_item(item_name, write_list)
                release_items = True
                logger.info(f'[MGS: Masala Garden Salad] Released held AP item after location sent: {item_name}')
            else:
                still_waiting.append(item_name)

        self.save_state['pending_missable_items'] = still_waiting
        return release_items


    # A player could repeatedly reload an area where a ration pickup spawns and check all ration locations in the game
    # Prevent this by tracking item pickups per game region and limiting them
    # Note, the endgame regions have higher maximums on purpose to allow a player to use the repeat reload 'exploit' to prevent softlocks
    def build_checks_per_region(self) -> dict[str, dict[str, int]]:
        checks_per_region_tracker = {
            'dock': {
                'rations': 0,
                'rations_max': 3,
            },
            'heliport': {
                'rations': 0,
                'rations_max': 1,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
                'stun_grenade': 0,
                'stun_grenade_max': 1,
                'socom': 0,
                'socom_max': 1,
            },
            'tank hangar': {
                'rations': 0,
                'rations_max': 1,
                'socom': 0,
                'socom_max': 1,
                'thermal_goggles': 0,
                'thermal_goggles_max': 1,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
                'suppressor': 0,
                'suppressor_max': 1,
                'cbox_a': 0,
                'cbox_a_max': 1,
                'mine_detector': 0,
                'mine_detector_max': 1,
            },
            'cell': {
                'rations': 0,
                'rations_max': 2,
                'socom': 0,
                'socom_max': 4,
            },
            'armory': {
                'socom': 0,
                'socom_max': 2,
                'grenade': 0,
                'grenade_max': 2,
                'famas': 0,
                'famas_max': 3,
                'nikita': 0,
                'nikita_max': 2,
                'psg1': 0,
                'psg1_max': 3,
            },
            'armory sth': {
                'rations': 0,
                'rations_max': 1,
                'socom': 0,
                'socom_max': 3,
                'c4': 0,
                'c4_max': 1,
                'stinger': 0,
                'stinger_max': 4,
                'stun_grenade': 0,
                'stun_grenade_max': 1,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
                'camera': 0,
                'camera_max': 1,
            },
            'canyon': {
                'rations': 0,
                'rations_max': 1,
                'grenade': 0,
                'grenade_max': 3,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
                'claymore': 0,
                'claymore_max': 5,
            },
            'nuke bldg 1': {
                'rations': 0,
                'rations_max': 1,
                'grenade': 0,
                'grenade_max': 1,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
                'famas': 0,
                'famas_max': 2,
                'socom': 0,
                'socom_max': 1,
            },
            'nuke bldg b1': {
                'rations': 0,
                'rations_max': 1,
                'socom': 0,
                'socom_max': 2,
                'famas': 0,
                'famas_max': 4,
                'nikita': 0,
                'nikita_max': 3,
                'stun_grenade': 0,
                'stun_grenade_max': 1,
                'diazepam': 0,
                'diazepam_max': 1,
                'cbox_b': 0,
                'cbox_b_max': 1,
                'pal_key': 0,
                'pal_key_max': 1,
            },
            'nuke bldg b2': {
                'rations': 0,
                'rations_max': 2,
                'c4': 0,
                'c4_max': 1,
                'grenade': 0,
                'grenade_max': 2,
                'stun_grenade': 0,
                'stun_grenade_max': 2,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
                'famas': 0,
                'famas_max': 1,
                'nikita': 0,
                'nikita_max': 2,
                'night_vision_goggles': 0,
                'night_vision_goggles_max': 1,
                'gasmask': 0,
                'gasmask_max': 1,
                # Body Armor AP location is generated in Blast Furnace, but the
                # vanilla Nuke Bldg B2 pickup can still exist. Allow either
                # physical pickup to send the single Body Armor location
				# since if you have don't have thermals they don't appear in Nuke B2
                'body_armor': 0,
                'body_armor_max': 1,
            },
            'lab': {
                'rations': 0,
                'rations_max': 1,
                'socom': 0,
                'socom_max': 1,
                'famas': 0,
                'famas_max': 2,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
            },
            'cmnder room': {
                'rations': 0,
                'rations_max': 2,
                'socom': 0,
                'socom_max': 2,
                'famas': 0,
                'famas_max': 3,
            },
            'cave': {
                'rations': 0,
                'rations_max': 3,
                'socom': 0,
                'socom_max': 1,
                'famas': 0,
                'famas_max': 2,
                'diazepam': 0,
                'diazepam_max': 1,
                'psg1': 0,
                'psg1_max': 3,  
            },
            'u.grnd pssge': {
                'rations': 0,
                'rations_max': 1,
                'socom': 0,
                'socom_max': 1,
                'famas': 0,
                'famas_max': 1,
                'psg1': 0,
                'psg1_max': 4,
            },
            'medi room': {
                'rations': 0,
                'rations_max': 1,
                'handkerchief': 0,
                'handkerchief_max': 1,
                'time_bomb': 0,
                'time_bomb_max': 1,

            },
            'comm twr a': {
                'rations': 0,
                'rations_max': 3,
                'socom': 0,
                'socom_max': 7,
                'famas': 0,
                'famas_max': 9,
                'stun_grenade': 0,
                'stun_grenade_max': 1,
                'rope': 0,
                'rope_max': 1,
            },
            # This area is for the roofs of both tower A and tower B
            'roof/comm tw': {
                'rations': 0,
                'rations_max': 1,
                'stinger': 0,
                'stinger_max': 1,
            },
            'twr wall a': {},
            'walkway': {
                'rations': 0,
                'rations_max': 2,
                'c4': 0,
                'c4_max': 1,
                'stinger': 0,
                'stinger_max': 1,
            },
            'comm twr b': {
                'rations': 0,
                'rations_max': 1,
                'socom': 0,
                'socom_max': 1,
                'famas': 0,
                'famas_max': 2,
                'grenade': 0,
                'grenade_max': 1,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
                'stinger': 0,
                'stinger_max': 3,
            },
            'comm twr b hind defeated': {
                'rations': 0,
                'rations_max': 2,
                'socom': 0,
                'socom_max': 2,
                'famas': 0,
                'famas_max': 9,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
                'psg1': 0,
                'psg1_max': 3,
            },
            'snowfield': {
                'rations': 0,
                'rations_max': 4,
                'socom': 0,
                'socom_max': 3,
                'famas': 0,
                'famas_max': 3,
                'diazepam': 0,
                'diazepam_max': 1,
                'psg1': 0,
                'psg1_max': 4,
                'cbox_c': 0,
                'cbox_c_max': 1,
                'grenade': 0,
                'grenade_max': 2,
                'stun_grenade': 0,
                'stun_grenade_max': 1,
                'chaff_grenade': 0,
                'chaff_grenade_max': 2,
                'claymore': 0,
                'claymore_max': 5,
                'stinger': 0,
                'stinger_max': 4,
                'nikita': 0,
                'nikita_max': 4,
            },
            # Areas below are on Disc 2
            'blast furnac': {
                'rations': 0,
                'rations_max': 2,
                'socom': 0,
                'socom_max': 3,
                'famas': 0,
                'famas_max': 1,
                'c4': 0,
                'c4_max': 1,
                # The alternate Body Armor pickup in Nuke B2 lvl 6 can still satisfy the check.
                'body_armor': 0,
                'body_armor_max': 1,
                'stinger': 0,
                'stinger_max': 2,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
                'stun_grenade': 0,
                'stun_grenade_max': 2,
                'nikita': 0,
                'nikita_max': 2,
                'psg1': 0,
                'psg1_max': 2
            },
            'cargo elev.': {
                'rations': 0,
                'rations_max': 1,
                'famas': 0,
                'famas_max': 9,
                'socom': 0,
                'socom_max': 3,
                'claymore': 0,
                'claymore_max': 5,
            },
            'warehouse': {
                'rations': 0,
                'rations_max': 1,
                'stinger': 0,
                'stinger_max': 2,
                'nikita': 0,
                'nikita_max': 2,
            },
            'warehouse nt': {
                'rations': 0,
                'rations_max': 1,
                'stinger': 0,
                'stinger_max': 4,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
            },
            # There are actually u.grnd base 1, 2, and 3, but current code doesn't pick up the number
            # Note the space after 'base' is important. The code picks up the space.
            'u.grnd base ': {
                'rations': 0,
                'rations_max': 2,
                'socom': 0,
                'socom_max': 3,
                'famas': 0,
                'famas_max': 4,
                'chaff_grenade': 0,
                'chaff_grenade_max': 3,
                'stinger': 0,
                'stinger_max': 2,
            },
            'cmnd room': {
                'rations': 0,
                'rations_max': 2,
            },
            'spply rte.': {
                'rations': 0,
                'rations_max': 2,
                'stinger': 0,
                'stinger_max': 3,
                'chaff_grenade': 0,
                'chaff_grenade_max': 1,
                'stun_grenade': 0,
                'stun_grenade_max': 1,
            },
            'esc route': {
                'rations': 0,
                'rations_max': 1,
            }
        }
        return checks_per_region_tracker


    def build_region_item_location_names(self) -> dict[str, dict[str, list[str]]]:
        region_aliases = {
            'Docks': 'dock',
            'Heliport': 'heliport',
            'Tank Hangar': 'tank hangar',
            'Tank Hangar_lvl1': 'tank hangar',
            'Tank Hangar_lvl2': 'tank hangar',
            'Cell': 'cell',
            'Cell_lvl1': 'cell',
            'Armory': 'armory',
            'Armory_lvl1': 'armory',
            'Armory_lvl2': 'armory',
            'Armory_lvl3': 'armory',
            'Armory_lvl5': 'armory',
            'Armory Sth': 'armory sth',
            'Armory Sth_C4': 'armory sth',
            'Armory Sth_C4_lvl4': 'armory sth',
            'Armory Sth_C4_lvl6': 'armory sth',
            'Canyon': 'canyon',
            'Nuke Building 1': 'nuke bldg 1',
            'Nuke Building B1': 'nuke bldg b1',
            'Nuke Building B1 lvl4': 'nuke bldg b1',
            'Nuke Building B1 lvl5': 'nuke bldg b1',
            'Nuke Building B2': 'nuke bldg b2',
            'Nuke Building B2 lvl4': 'nuke bldg b2',
            'Nuke Building B2 lvl6': 'nuke bldg b2',
            'Lab': 'lab',
            'Commander Room': 'cmnder room',
            'Cave': 'cave',
            'Underground Passage': 'u.grnd pssge',
            'Medi Room': 'medi room',
            'Comm Tower A': 'comm twr a',
            'Roof/Comm Tw': 'roof/comm tw',
            'Comm Tower B Roof': 'roof/comm tw',
            'Twr Wall A': 'twr wall a',
            'Walkway': 'walkway',
            'Comm Tower B': 'comm twr b',
            'Comm Tower B (Hind D[efeated])': 'comm twr b hind defeated',
            'Snow Field': 'snowfield',
            'Snow Field (sans Wolf)': 'snowfield',
            'Blast Furnace': 'blast furnac',
            'Cargo Elev.': 'cargo elev.',
            'Cargo Elevator': 'cargo elev.',
            'Warehouse': 'warehouse',
            'Warehouse North': 'warehouse nt',
            'U.Ground Base': 'u.grnd base ',
            'Underground Base': 'u.grnd base ',
            'Command Room': 'cmnd room',
            'Cmnd Room': 'cmnd room',
            'Metal Gear REX': 'spply rte.',
            'Spply Rte.': 'spply rte.',
            'Esc Route': 'esc route',
            'Escape Route': 'esc route',
        }
        item_prefix_to_key = {
            'Ration': 'rations',
            'Medicine': 'medicine',
            'Diazepam': 'diazepam',
            'SOCOM': 'socom',
            'FA-MAS': 'famas',
            'Grenade': 'grenade',
            'Nikita': 'nikita',
            'Stinger': 'stinger',
            'Claymore': 'claymore',
            'C4': 'c4',
            'Stun Grenade': 'stun_grenade',
            'Chaff Grenade': 'chaff_grenade',
            'PSG-1': 'psg1',
            'Body Armor': 'body_armor',
            'Camera': 'camera',
        }
        region_item_location_names: dict[str, dict[str, list[str]]] = {}
        for full_name in Regions.build_location_name_to_id_table().keys():
            if ' - ' not in full_name:
                continue
            region_name, location_name = full_name.rsplit(' - ', 1)
            if region_name not in region_aliases:
                continue
            matched_prefix = None
            for prefix in item_prefix_to_key.keys():
                if location_name == prefix or location_name.startswith(prefix + ' '):
                    matched_prefix = prefix
                    break
            if matched_prefix is None:
                continue
            region_key = region_aliases[region_name]
            item_key = item_prefix_to_key[matched_prefix]
            region_item_location_names.setdefault(region_key, {}).setdefault(item_key, []).append(full_name)
        return region_item_location_names

    def synchronize_region_check_trackers(self) -> None:
        defaults = self.build_checks_per_region()
        saved_trackers = self.save_state.setdefault('checks_per_region_tracker', {})
        checked_locations = getattr(self.bizhawk_ctx, 'checked_locations', None)
        total_locations_by_item: dict[str, int] = {}
        checked_locations_by_item: dict[str, int] = {}

        for region_name, default_tracker in defaults.items():
            saved_tracker = saved_trackers.setdefault(region_name, {})

            for tracker_key, default_value in default_tracker.items():
                saved_tracker.setdefault(tracker_key, default_value)

            # Numbered pickup locations are the authoritative source for these
            # maximums. Deriving the values here prevents the client tracker from
            # drifting when regional location names are added, removed, or split.
            item_locations = self.save_state['region_item_location_names'].get(region_name, {})
            for item_key, location_names in item_locations.items():
                saved_tracker[f'{item_key}_max'] = len(location_names)
                total_locations_by_item[item_key] = total_locations_by_item.get(item_key, 0) + len(location_names)

                if checked_locations is not None:
                    checked_count = 0
                    for location_name in location_names:
                        location_id = self.location_name_to_server_location_id.get(location_name)
                        if location_id is not None and location_id in checked_locations:
                            checked_count += 1
                    saved_tracker[item_key] = checked_count
                    checked_locations_by_item[item_key] = checked_locations_by_item.get(item_key, 0) + checked_count
                else:
                    saved_tracker[item_key] = min(saved_tracker.get(item_key, 0), len(location_names))

        # The old global counters are still used as an additional safety gate.
        # Keep those totals aligned with the same regional location source too.
        for item_key, total_locations in total_locations_by_item.items():
            self.save_state[f'{item_key}_max_location_counter'] = total_locations
            if checked_locations is not None:
                self.save_state[f'{item_key}_location_counter'] = checked_locations_by_item.get(item_key, 0) + 1

        # Body Armor has one AP location in Blast Furnace, but either the Blast
        # Furnace pickup or the alternate Nuke Bldg B2 pickup may satisfy it.
        # Mirror the server-checked state into both physical-region trackers
        # without counting the single AP location twice in the global maximum.
        if checked_locations is not None:
            body_armor_location_id = self.resolve_location_id('Body Armor')
            body_armor_checked = (
                body_armor_location_id is not None
                and body_armor_location_id in checked_locations
            )
            for region_name in ('blast furnac', 'nuke bldg b2'):
                region_tracker = saved_trackers.get(region_name)
                if region_tracker is not None and 'body_armor' in region_tracker:
                    region_tracker['body_armor_max'] = 1
                    region_tracker['body_armor'] = int(body_armor_checked)
            self.save_state['body_armor_max_location_counter'] = 1
            self.save_state['body_armor_location_counter'] = 2 if body_armor_checked else 1

        self.save_state['regions'] = list(defaults.keys())

    def log_blocked_pickup_message(self, region_name: str, item_key: str, message: str) -> None:
        message_key = (region_name, item_key, message)
        now = time.monotonic()
        last_message_time = self.blocked_pickup_message_times.get(message_key, 0.0)
        if now - last_message_time < 2.0:
            return
        self.blocked_pickup_message_times[message_key] = now
        logger.info(f'[MGS: Masala Garden Salad] {message}')

    def get_next_region_location_name(self, region_name: str, item_key: str) -> str | None:
        region_checks = self.save_state['checks_per_region_tracker'][region_name]
        region_item_locations = self.save_state['region_item_location_names'].get(region_name, {})
        all_item_locations = list(region_item_locations.get(item_key, []))
        item_locations = all_item_locations
        item_index = region_checks.get(item_key, 0)
        blocked_message: str | None = None
        item_display_names = {
            'rations': 'Ration',
            'medicine': 'Medicine',
            'diazepam': 'Diazepam',
            'socom': 'SOCOM',
            'famas': 'FA-MAS',
            'grenade': 'Grenade',
            'nikita': 'Nikita',
            'stinger': 'Stinger',
            'claymore': 'Claymore',
            'c4': 'C4',
            'stun_grenade': 'Stun Grenade',
            'chaff_grenade': 'Chaff Grenade',
            'psg1': 'PSG-1',
            'camera': 'Camera',
        }
        item_display_name = item_display_names.get(item_key, item_key.replace('_', ' ').title())

        # Every main Armory key-card room is reported under the same RAM
        # region name. Filter by the AP-controlled Progressive Key Card level
        # so reloading an accessible pickup cannot consume checks behind a
        # higher-level door. The deleted main Armory C4-wall rooms are not
        # part of this list; only the normal Level 1, 2, 3, and 5 rooms remain.
        if region_name == 'armory':
            key_card_level = max(0, min(int(self.save_state.get('key_card_counter', 0)), 7))
            armory_key_card_requirements = {
                'Armory_lvl1': 1,
                'Armory_lvl2': 2,
                'Armory_lvl3': 3,
                'Armory_lvl5': 5,
            }
            item_locations = [
                location_name
                for location_name in all_item_locations
                if key_card_level >= armory_key_card_requirements.get(
                    location_name.rsplit(' - ', 1)[0],
                    0,
                )
            ]

            if item_index >= len(item_locations) and item_index < len(all_item_locations):
                blocked_location = all_item_locations[item_index]
                blocked_region = blocked_location.rsplit(' - ', 1)[0]
                required_key_card_level = armory_key_card_requirements.get(blocked_region, 0)
                if key_card_level < required_key_card_level:
                    blocked_message = (
                        f'No {item_display_name} check sent: the next Armory '
                        f'{item_display_name} check requires Progressive Key Card '
                        f'Level {required_key_card_level}. No location was consumed.'
                    )

        # Metal Gear Solid reports the base room, C4 room, Level 4 room, and
        # Level 6 room in Armory South under the same RAM region name. Entry to
        # Armory South is already gated by C4/Stinger logic, so the client only
        # needs to separate the Key Card 4 and Key Card 6 pickup tiers. Without
        # this filter, repeatedly reloading the Level 4 Stinger could consume
        # the later Level 6 Stinger checks. The C4 room itself has no Key Card
        # requirement.
        if region_name == 'armory sth':
            key_card_level = max(0, min(int(self.save_state.get('key_card_counter', 0)), 7))
            armory_south_key_card_requirements = {
                'Armory Sth_C4_lvl4': 4,
                'Armory Sth_C4_lvl6': 6,
            }
            item_locations = [
                location_name
                for location_name in all_item_locations
                if key_card_level >= armory_south_key_card_requirements.get(
                    location_name.rsplit(' - ', 1)[0],
                    0,
                )
            ]

            if item_index >= len(item_locations) and item_index < len(all_item_locations):
                blocked_location = all_item_locations[item_index]
                blocked_region = blocked_location.rsplit(' - ', 1)[0]
                required_key_card_level = armory_south_key_card_requirements.get(blocked_region, 0)
                if key_card_level < required_key_card_level:
                    blocked_message = (
                        f'No {item_display_name} check sent: the next Armory South '
                        f'{item_display_name} check requires Progressive Key Card '
                        f'Level {required_key_card_level}. No location was consumed.'
                    )

        if item_index < len(item_locations):
            return item_locations[item_index]
        if blocked_message is not None:
            self.log_blocked_pickup_message(region_name, item_key, blocked_message)
        return None

    # Various game states are placed into a dictionary and saved as a json file so that runs can be saved and reloaded.
    def initalize_save_data(self):
        save_state : dict[str, Any] = {
            'received_item_counter': 0,
            'pending_missable_items': [],
            'has_cbox_a': False,
            'cbox_a_counter': 0,
            'has_cbox_b': False,
            'cbox_b_counter': 0,
            'has_cbox_c': 0,
            'cbox_c_counter': 0,
            'has_night_vision_goggles': False,
            'night_vision_goggles_counter': 0,
            'has_thermal_goggles': False,
            'thermal_goggles_counter': 0,
            'has_gasmask': False,
            'gasmask_counter': 0,
            'has_body_armor': False,
            'body_armor_counter': 0,
            'has_camera': False,
            'camera_counter': 0,
            'stealth_counter': 0,
            'bandana_counter': 0,
            'rations_counter': 0,
            'medicine_counter': 0,
            'diazepam_counter': 0,
            'pal_key_counter': 0,
            'key_card_counter': 0,
            'time_bomb_counter': 0,
            'has_mine_detector': False,
            'mine_detector_counter': 0,
            'has_rope': False,
            'rope_counter': 0,
            'handkerchief_counter': 0,
            'has_suppressor': False,
            'suppressor_counter': 0,
            'has_socom': True,
            'socom_counter': 0,
            'has_famas': True,
            'famas_counter': 0,
            'has_grenade': False,
            'grenade_counter': 0,
            'has_nikita': True,
            'nikita_counter': 0,
            'has_stinger': True,
            'stinger_counter': 0,
            'has_claymore': False,
            'claymore_counter': 0,
            'has_c4': False,
            'c4_counter': 0,
            'has_stun_grenade': False,
            'stun_grenade_counter': 0,
            'has_chaff_grenade': False,
            'chaff_grenade_counter': 0,
            'has_psg1': True,
            'psg1_counter': 0,
            'dogtag_counter': 0,
            'boss_defeat_counter': 0,
            'cbox_a_location_counter': 1,
            'cbox_a_max_location_counter': 1,
            'cbox_b_location_counter': 1,
            'cbox_b_max_location_counter': 1,
            'cbox_c_location_counter': 1,
            'cbox_c_max_location_counter': 1,
            'night_vision_goggles_location_counter': 1,
            'night_vision_goggles_max_location_counter': 1,
            'thermal_goggles_location_counter': 1,
            'thermal_goggles_max_location_counter': 1,
            'gasmask_location_counter': 1,
            'gasmask_max_location_counter': 1,
            'body_armor_location_counter': 1,
            'body_armor_max_location_counter': 1,
            'camera_location_counter': 1,
            'camera_max_location_counter': 1,
            'rations_location_counter': 1,
            'rations_max_location_counter': 46,
            'medicine_location_counter': 1,
            'medicine_max_location_counter': 1,
            'diazepam_location_counter': 1,
            'diazepam_max_location_counter': 3,
            'pal_key_location_counter': 1,
            'pal_key_max_location_counter': 1,
            'key_card_location_counter': 1,
            'key_card_max_location_counter': 7,
            'time_bomb_location_counter': 1,
            'time_bomb_max_location_counter': 1,
            'mine_detector_location_counter': 1,
            'mine_detector_max_location_counter': 1,
            'rope_location_counter': 1,
            'rope_max_location_counter': 1,
            'handkerchief_location_counter': 1,
            'handkerchief_max_location_counter': 1,
            'suppressor_location_counter': 1,
            'suppressor_max_location_counter': 1,
            'socom_location_counter': 1,
            'socom_max_location_counter': 43,
            'famas_location_counter': 1,
            'famas_max_location_counter': 58,
            'grenade_location_counter': 1,
            'grenade_max_location_counter': 11,
            'nikita_location_counter': 1,
            'nikita_max_location_counter': 15,
            'stinger_location_counter': 1,
            'stinger_max_location_counter': 26,
            'claymore_location_counter': 1,
            'claymore_max_location_counter': 15,
            'c4_location_counter': 1,
            'c4_max_location_counter': 4,
            'stun_grenade_location_counter': 1,
            'stun_grenade_max_location_counter': 11,
            'chaff_grenade_location_counter': 1,
            'chaff_grenade_max_location_counter': 18,
            'psg1_location_counter': 1,
            'psg1_max_location_counter': 19,
            'viewed_boss_cutscene_bytes': [],
            'viewed_key_card_cutscene_text': [],
            'viewed_pal_key_cutscene_text': [],
            'is_captured': False,
            'endgame_inventory_locked': False,
            'endgame_rations_last_seen': None,
            'pending_endgame_items': [],
            'has_snowfield': False,
            'has_defeated_hind': False,
            'checks_per_region_tracker': self.build_checks_per_region(),
            'region_item_location_names': self.build_region_item_location_names(),
            'last_region': None,
            }
        save_state['regions'] = [key for key in save_state['checks_per_region_tracker'].keys()]
        return save_state
    
    # Works by comparing the in-game item counters to counts tracked by the Archipelago client.
    # Ex. Assume the in-game counts are Rations: 0, SOCOM: 0 and the Client counts are the same.
    # The player picks up a ration. The in-game count is now Rations: 1, SOCOM: 0. The Client count is still Rations: 0, SOCOM: 0.
    # The client will detect that the Rations count is higher than it should be and send out a Rations location check to the Archipelago server.
    # It will then decrease the in-game Rations count to 0.
    # Items that can be received during cutscenes work differently!
    def handle_endgame_pickups(self, read_values: dict, write_list: list) -> bool:
        """Allow only the physical Escape Route Ration after REX.

        Liquid removes Snake's inventory after the REX battle. During the
        remaining Liquid/escape sequence, ordinary pickup reconciliation would
        either restore that removed gear or interpret the removal as item loss.
        Keep all normal pickup handling disabled, but preserve the one intended
        physical pickup in the Escape Route.
        """
        has_state_changed = False
        current_rations = read_values['rations_held']
        previous_rations = self.save_state.get('endgame_rations_last_seen')

        def normalized_ration_count(value: int | None) -> int:
            if value is None or value == 0xFFFF:
                return -1
            return value

        current_normalized = normalized_ration_count(current_rations)
        previous_normalized = normalized_ration_count(previous_rations)

        if read_values['current_region_name'] == 'esc route':
            region_checks = self.save_state['checks_per_region_tracker'].get('esc route', {})
            ration_unsent = (
                'rations' in region_checks
                and region_checks['rations'] < region_checks['rations_max']
            )

            # During continuous play, detect the increase from no ration to one
            # ration. If reconnecting after the physical pickup but before its
            # check was sent, a positive first observed value is also sufficient
            # because Liquid leaves Snake with no inventory.
            ration_was_picked_up = (
                previous_rations is not None
                and current_normalized > previous_normalized
            )
            reconnect_after_pickup = (
                previous_rations is None
                and current_normalized > 0
            )

            if ration_unsent and (ration_was_picked_up or reconnect_after_pickup):
                location_name = self.get_next_region_location_name('esc route', 'rations')
                if location_name is not None and self.queue_location(location_name):
                    if self.save_state['rations_location_counter'] <= self.save_state['rations_max_location_counter']:
                        self.save_state['rations_location_counter'] += 1
                    region_checks['rations'] += 1

                    # Keep the vanilla Ration in Snake's inventory and copy it
                    # to the game's retry/death inventory. Do not merge it into
                    # the pre-REX AP ration total, which remains intentionally
                    # inaccessible for the rest of the run.
                    if current_rations != 0xFFFF:
                        write_list.append((
                            RAM.rations_death_count_address,
                            to_u16_bytes(current_rations),
                            'MainRAM',
                        ))
                    logger.info(
                        '[MGS: Masala Garden Salad] Escape Route Ration collected; '
                        'the physical Ration remains available during the endgame lock.'
                    )
                    has_state_changed = True

        if previous_rations != current_rations:
            self.save_state['endgame_rations_last_seen'] = current_rations
            has_state_changed = True

        return has_state_changed

    def handle_item_pickups(self, read_values: dict, write_list: list) -> bool:
        has_state_changed = False
        # Don't check for item pickups during scene when locked up.
        # All items are taken away and then given back after escape which messes up checks.
        # Note, item counts aren't erased but are prefixed with an '8' during this scene.
        # Ex. SOCOM ammo count of 0x001B becomes 0x801B
        if self.save_state['is_captured']:
            return has_state_changed
        if self.save_state.get('endgame_inventory_locked', False):
            return self.handle_endgame_pickups(read_values, write_list)
        
        # A value of 0x0000 means the player has it in inventory with 0 ammo
        # A value of 0xFFFF means the player hasn't been picked up the item yet
        # Cardboard Box A
        if read_values['cbox_a_held'] != 0xFFFF and read_values['cbox_a_held'] > self.save_state['cbox_a_counter']:
            if not self.save_state['has_cbox_a']:
                write_value = 65535
            else:
                write_value = self.save_state['cbox_a_counter']
            write_list.append((RAM.cbox_a_count_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'cbox_a' in region_checks.keys():
                if region_checks['cbox_a'] < region_checks['cbox_a_max'] and self.save_state['cbox_a_location_counter'] <= self.save_state['cbox_a_max_location_counter']:
                    location_name = 'Cardboard Box A'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['cbox_a_location_counter'] += 1
                    region_checks['cbox_a'] += 1
                    has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['cbox_a']} of {region_checks['cbox_a_max']} Cardboard Box A in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Cardboard Box A not found in: {read_values['current_region_name']}")

        # Cardboard Box B
        if read_values['cbox_b_held'] != 0xFFFF and read_values['cbox_b_held'] > self.save_state['cbox_b_counter']:
            if not self.save_state['has_cbox_b']:
                write_value = 65535
            else:
                write_value = self.save_state['cbox_b_counter']
            write_list.append((RAM.cbox_b_count_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'cbox_b' in region_checks.keys():
                if region_checks['cbox_b'] < region_checks['cbox_b_max'] and self.save_state['cbox_b_location_counter'] <= self.save_state['cbox_b_max_location_counter']:
                    location_name = 'Cardboard Box B'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['cbox_b_location_counter'] += 1
                    region_checks['cbox_b'] += 1
                    has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['cbox_b']} of {region_checks['cbox_b_max']} Cardboard Box B in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Cardboard Box B not found in: {read_values['current_region_name']}")

        # Cardboard Box C
        if read_values['cbox_c_held'] != 0xFFFF and read_values['cbox_c_held'] > self.save_state['cbox_c_counter']:
            if not self.save_state['has_cbox_c']:
                write_value = 65535
            else:
                write_value = self.save_state['cbox_c_counter']
            write_list.append((RAM.cbox_c_count_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'cbox_c' in region_checks.keys():
                if region_checks['cbox_c'] < region_checks['cbox_c_max'] and self.save_state['cbox_c_location_counter'] <= self.save_state['cbox_c_max_location_counter']:
                    location_name = 'Cardboard Box C'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['cbox_c_location_counter'] += 1
                    region_checks['cbox_c'] += 1
                    has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['cbox_c']} of {region_checks['cbox_c_max']} Cardboard Box C in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Cardboard Box C not found in: {read_values['current_region_name']}")

        # Night Vision Goggles
        if read_values['night_vision_goggles_held'] != 0xFFFF and read_values['night_vision_goggles_held'] > self.save_state['night_vision_goggles_counter']:
            if not self.save_state['has_night_vision_goggles']:
                write_value = 65535
            else:
                write_value = self.save_state['night_vision_goggles_counter']
            write_list.append((RAM.nvg_count_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'night_vision_goggles' in region_checks.keys():
                if region_checks['night_vision_goggles'] < region_checks['night_vision_goggles_max'] and self.save_state['night_vision_goggles_location_counter'] <= self.save_state['night_vision_goggles_max_location_counter']:
                    location_name = 'Night Vision Goggles'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['night_vision_goggles_location_counter'] += 1
                    region_checks['night_vision_goggles'] += 1
                    has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['night_vision_goggles']} of {region_checks['night_vision_goggles_max']} Night Vision Goggles in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Night Vision Goggles not found in: {read_values['current_region_name']}")

        # Thermal Goggles
        if read_values['thermal_goggles_held'] != 0xFFFF and read_values['thermal_goggles_held'] > self.save_state['thermal_goggles_counter']:
            if not self.save_state['has_thermal_goggles']:
                write_value = 65535
            else:
                write_value = self.save_state['thermal_goggles_counter']
            write_list.append((RAM.therm_g_count_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'thermal_goggles' in region_checks.keys():
                if region_checks['thermal_goggles'] < region_checks['thermal_goggles_max'] and self.save_state['thermal_goggles_location_counter'] <= self.save_state['thermal_goggles_max_location_counter']:
                    location_name = 'Thermal Goggles'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['thermal_goggles_location_counter'] += 1
                    region_checks['thermal_goggles'] += 1
                    has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['thermal_goggles']} of {region_checks['thermal_goggles_max']} Thermal Goggles in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Thermal Goggles not found in: {read_values['current_region_name']}")

        # Gasmask
        if read_values['gasmask_held'] != 0xFFFF and read_values['gasmask_held'] > self.save_state['gasmask_counter']:
            if not self.save_state['has_gasmask']:
                write_value = 65535
            else:
                write_value = self.save_state['gasmask_counter']
            write_list.append((RAM.gasmask_count_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'gasmask' in region_checks.keys():
                if region_checks['gasmask'] < region_checks['gasmask_max'] and self.save_state['gasmask_location_counter'] <= self.save_state['gasmask_max_location_counter']:
                    location_name = 'Gas Mask'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['gasmask_location_counter'] += 1
                    region_checks['gasmask'] += 1
                    has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['gasmask']} of {region_checks['gasmask_max']} Gasmask in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Gas Mask not found in: {read_values['current_region_name']}")

        # Body Armor
        if read_values['body_armor_held'] != 0xFFFF and read_values['body_armor_held'] > self.save_state['body_armor_counter']:
            if not self.save_state['has_body_armor']:
                write_value = 65535
            else:
                write_value = self.save_state['body_armor_counter']
            write_list.append((RAM.b_armor_count_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'body_armor' in region_checks.keys():
                if region_checks['body_armor'] < region_checks['body_armor_max'] and self.save_state['body_armor_location_counter'] <= self.save_state['body_armor_max_location_counter']:
                    location_name = 'Body Armor'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['body_armor_location_counter'] += 1
                    region_checks['body_armor'] += 1
                    has_state_changed = True
                else:
                    # Body Armor is a single AP location with two possible
                    # physical pickups. A duplicate/stale pickup needs only to
                    # be reverted; do not emit a misleading "0 of 1" warning.
                    region_checks['body_armor'] = region_checks['body_armor_max']
                    has_state_changed = True
            else:
                logger.info(f"[MGS: Masala Garden Salad] Body Armor not found in: {read_values['current_region_name']}")

        # Camera
        if read_values['camera_held'] != 0xFFFF and read_values['camera_held'] > self.save_state['camera_counter']:
            if not self.save_state['has_camera']:
                write_value = 0xFFFF
            else:
                write_value = self.save_state['camera_counter']
            write_list.append((RAM.camera_count_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'camera' in region_checks:
                if (region_checks['camera'] < region_checks['camera_max']
                        and self.save_state['camera_location_counter'] <= self.save_state['camera_max_location_counter']):
                    location_name = self.get_next_region_location_name(
                        read_values['current_region_name'], 'camera'
                    )
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['camera_location_counter'] += 1
                        region_checks['camera'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['camera']} of {region_checks['camera_max']} Camera in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Camera not found in: {read_values['current_region_name']}")

        # Rations
        if read_values['rations_held'] != 0xFFFF and read_values['rations_held'] > self.save_state['rations_counter']:
            write_list.append((RAM.rations_count_address, to_u16_bytes(self.save_state['rations_counter']), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'rations' in region_checks.keys():
                if region_checks['rations'] < region_checks['rations_max']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'rations')
                    if location_name is not None:
                        if self.save_state['rations_location_counter'] <= self.save_state['rations_max_location_counter'] or read_values['current_region_name'] == 'esc route':
                            self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                            if self.save_state['rations_location_counter'] <= self.save_state['rations_max_location_counter']:
                                self.save_state['rations_location_counter'] += 1
                            region_checks['rations'] += 1
                            has_state_changed = True
                        else:
                            logger.info(f"[MGS: Masala Garden Salad] Ration location counter exhausted ({self.save_state['rations_location_counter']} > {self.save_state['rations_max_location_counter']}) before sending {location_name} in {read_values['current_region_name']}!")
                else:
                    # Leaving the Medi Room restores Snake's confiscated
                    # inventory and can briefly make the Ration count appear
                    # higher than the AP-owned count. Reconcile it silently;
                    # this was not another physical Ration pickup.
                    if time.monotonic() >= self.suppress_post_capture_ration_messages_until:
                        logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['rations']} of {region_checks['rations_max']} Rations in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Rations not found in: {read_values['current_region_name']}")
        elif read_values['rations_held'] < self.save_state['rations_counter']:
            self.save_state['rations_counter'] = read_values['rations_held']
            has_state_changed = True

        # Medicine
        if read_values['medicine_held'] != 0xFFFF and read_values['medicine_held'] > self.save_state['medicine_counter']:
            write_list.append((RAM.medicine_count_address, to_u16_bytes(self.save_state['medicine_counter']), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'medicine' in region_checks.keys():
                if region_checks['medicine'] < region_checks['medicine_max'] and self.save_state['medicine_location_counter'] <= self.save_state['medicine_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'medicine')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['medicine_location_counter'] += 1
                        region_checks['medicine'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['medicine']} of {region_checks['medicine_max']} Medicine in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Medicine not found in: {read_values['current_region_name']}")
        elif read_values['medicine_held'] < self.save_state['medicine_counter']:
            self.save_state['medicine_counter'] = read_values['medicine_held']
            has_state_changed = True

        # Diazepam
        if read_values['diazepam_held'] != 0xFFFF and read_values['diazepam_held'] > self.save_state['diazepam_counter']:
            write_list.append((RAM.diazepam_count_address, to_u16_bytes(self.save_state['diazepam_counter']), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'diazepam' in region_checks.keys():
                if region_checks['diazepam'] < region_checks['diazepam_max'] and self.save_state['diazepam_location_counter'] <= self.save_state['diazepam_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'diazepam')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['diazepam_location_counter'] += 1
                        region_checks['diazepam'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['diazepam']} of {region_checks['diazepam_max']} Diazepam in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Diazepam not found in: {read_values['current_region_name']}")
        elif read_values['diazepam_held'] < self.save_state['diazepam_counter']:
            self.save_state['diazepam_counter'] = read_values['diazepam_held']
            has_state_changed = True

        # HACK MGS: It would probably be easier to ignore read values of Pal Key and Key Card and only use cutscenes as the check
        # Pal Key
        # Can be received during a cutscene. If the player doesn't already have a Pal Key in their inventory, this check works all the rest.
        # If the player does have a Pal Key, then the location will be sent when the cutscene is loaded.
        self.save_state.setdefault('viewed_pal_key_cutscene_text', [])
        self.save_state.setdefault('medi_room_otacon_gifts_received', False)
        pal_key_location_unsent = self.save_state['pal_key_location_counter'] <= self.save_state['pal_key_max_location_counter']

        if read_values['pal_key_held'] != 0xFFFF and read_values['pal_key_held'] > self.save_state['pal_key_counter']:
            write_list.append((RAM.pal_key_count_address, to_u16_bytes(self.save_state['pal_key_counter']), 'MainRAM'))
            if pal_key_location_unsent and self.queue_location('Pal Key'):
                self.save_state['pal_key_location_counter'] = self.save_state['pal_key_max_location_counter'] + 1
                if 'nuke bldg b1' in self.save_state['checks_per_region_tracker'] and 'pal_key' in self.save_state['checks_per_region_tracker']['nuke bldg b1']:
                    self.save_state['checks_per_region_tracker']['nuke bldg b1']['pal_key'] = self.save_state['checks_per_region_tracker']['nuke bldg b1']['pal_key_max']
                has_state_changed = True
        # If AP already gave the player a Pal Key, the in-game PAL pickup may not
        # increase RAM. In that case, use the Meryl/PAL cutscene line as the check.
        # Keep this separate from viewed_key_card_cutscene_text because the same text
        # is also used by Key Card Level 5 handling.
        elif (read_values['current_cutscene_bytes'] == RAM.key_card_level_5_cutscene_bytes
              and read_values['current_cutscene_text'] not in self.save_state['viewed_pal_key_cutscene_text']
              and self.save_state['pal_key_counter'] >= 1
              and pal_key_location_unsent):
            if self.queue_location('Pal Key'):
                self.save_state['pal_key_location_counter'] = self.save_state['pal_key_max_location_counter'] + 1
                if 'nuke bldg b1' in self.save_state['checks_per_region_tracker'] and 'pal_key' in self.save_state['checks_per_region_tracker']['nuke bldg b1']:
                    self.save_state['checks_per_region_tracker']['nuke bldg b1']['pal_key'] = self.save_state['checks_per_region_tracker']['nuke bldg b1']['pal_key_max']
                self.save_state['viewed_pal_key_cutscene_text'].append(read_values['current_cutscene_text'])
                has_state_changed = True
        # Handle loss - Technically the player does get their Pal Key taken away from them, but I'm ignoring that.
        # elif read_values['pal_key_held'] < self.save_state['pal_key_counter']:
        #     self.save_state['pal_key_counter'] = read_values['pal_key_held']
        #     has_state_changed = True

        # Key Card
        # NOTE: No regional check for pickups. Should be impossible to pickup key cards multiple times as they trigger during cutscenes
        # Several Key Card cutscenes were popping the wrong Key Card i.e. Gray Fox would pop Meryl's Key Card
        # This didn't matter before the region rewrite since they were just named "Key Card"
        # Identify the level from the cutscene text instead of trusting whatever
        # number the counter happens to be sitting on. The identifying bytes and
        # the RAM increase can land on adjacent polls, so retain each briefly and
        # only pair them when they identify the same Key Card level.
        key_card_event_window = 5.0
        key_card_event_time = time.monotonic()
        identified_level = KEY_CARD_LEVEL_BY_CUTSCENE_BYTES.get(read_values['current_cutscene_bytes'])

        # Level 2 is paired directly with the Revolver Ocelot story check in
        # the boss-cutscene handler below. Do not use the AP-owned Progressive
        # Key Card level as authorization for this location; the randomized
        # card may be anywhere in the multiworld.

        if identified_level is not None:
            self.recent_key_card_cutscene_level = identified_level
            self.recent_key_card_cutscene_time = key_card_event_time
        elif key_card_event_time - self.recent_key_card_cutscene_time > key_card_event_window:
            self.recent_key_card_cutscene_level = None

        if (self.pending_key_card_level is not None
                and key_card_event_time - self.pending_key_card_time > key_card_event_window):
            self.pending_key_card_level = None

        if read_values['key_card_held'] != 0xFFFF and read_values['key_card_held'] > self.save_state['key_card_counter']:
            write_list.append((RAM.key_card_count_address, to_u16_bytes(self.save_state['key_card_counter']), 'MainRAM'))
            if self.save_state['key_card_location_counter'] <= self.save_state['key_card_max_location_counter']:
                observed_level = read_values['key_card_held'] & 0x7FFF
                self.pending_key_card_level = observed_level
                self.pending_key_card_time = key_card_event_time

                matching_cutscene_level = identified_level
                if matching_cutscene_level is None:
                    matching_cutscene_level = self.recent_key_card_cutscene_level

                confirmed_level = matching_cutscene_level

                if confirmed_level == observed_level:
                    location_name = f'Key Card Level {confirmed_level}'
                    next_key_card_location_counter = max(
                        self.save_state['key_card_location_counter'],
                        confirmed_level + 1,
                    )

                    if self.queue_location(location_name):
                        self.save_state['key_card_location_counter'] = next_key_card_location_counter
                        if read_values['current_cutscene_text'] not in self.save_state['viewed_key_card_cutscene_text']:
                            self.save_state['viewed_key_card_cutscene_text'].append(read_values['current_cutscene_text'])
                        self.pending_key_card_level = None
                        has_state_changed = True
        # When a cutscene gives keycard level 1, it will set keycard count to 1 in RAM
        # Ensure the player cannot 'lose' keycard levels
        elif read_values['key_card_held'] < self.save_state['key_card_counter']:
            write_list.append((RAM.key_card_count_address, to_u16_bytes(self.save_state['key_card_counter']), 'MainRAM'))
            has_state_changed = True
        # The scripted RAM increase can occur before its identifying cutscene
        # bytes. Finish the check on a later poll once both signals agree.
        elif (self.pending_key_card_level is not None
              and identified_level == self.pending_key_card_level
              and self.save_state['key_card_location_counter'] <= self.save_state['key_card_max_location_counter']):
            location_name = f'Key Card Level {identified_level}'
            next_key_card_location_counter = max(
                self.save_state['key_card_location_counter'],
                identified_level + 1,
            )

            if self.queue_location(location_name):
                self.save_state['key_card_location_counter'] = next_key_card_location_counter
                self.save_state['viewed_key_card_cutscene_text'].append(read_values['current_cutscene_text'])
                self.pending_key_card_level = None
                has_state_changed = True
        # If the player currently has a keycard level greater than or equal to the keycard level provided by a cutscene, the location check won't trigger naturally.
        # check for cutscene text when the current keycard level is higher than what is expected naturally
        elif read_values['current_cutscene_text'] not in self.save_state['viewed_key_card_cutscene_text']:
            assert isinstance(self.save_state['viewed_key_card_cutscene_text'], list)
            if read_values['current_cutscene_bytes'] == RAM.key_card_level_1_cutscene_bytes and self.save_state['key_card_counter'] >= 1:
                if self.save_state['key_card_location_counter'] <= self.save_state['key_card_max_location_counter']:
                    location_name = 'Key Card Level 1'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['key_card_location_counter'] += 1
                    self.save_state['viewed_key_card_cutscene_text'].append(read_values['current_cutscene_text'])
                    has_state_changed = True
            elif read_values['current_cutscene_bytes'] == RAM.key_card_level_3_cutscene_bytes and self.save_state['key_card_counter'] >= 3:
                if self.save_state['key_card_location_counter'] <= self.save_state['key_card_max_location_counter']:
                    m1_tank_location = 'BOSS: M1 Tank'
                    key_card_level_3_location = 'Key Card Level 3'
                    m1_tank_location_id = self.location_name_to_server_location_id[m1_tank_location]

                    if m1_tank_location_id not in self.bizhawk_ctx.server_locations and m1_tank_location_id not in self.locations_to_send:
                        self.locations_to_send += [m1_tank_location_id]

                    if m1_tank_location_id in self.bizhawk_ctx.server_locations or m1_tank_location_id in self.locations_to_send:
                        self.locations_to_send += [self.location_name_to_server_location_id[key_card_level_3_location]]
                        self.save_state['key_card_location_counter'] += 1
                        self.save_state['viewed_key_card_cutscene_text'].append(read_values['current_cutscene_text'])
                        has_state_changed = True
            elif read_values['current_cutscene_bytes'] == RAM.key_card_level_4_cutscene_bytes and self.save_state['key_card_counter'] >= 4:
                if self.save_state['key_card_location_counter'] <= self.save_state['key_card_max_location_counter']:
                    location_name = 'Key Card Level 4'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['key_card_location_counter'] += 1
                    self.save_state['viewed_key_card_cutscene_text'].append(read_values['current_cutscene_text'])
                    has_state_changed = True
            elif read_values['current_cutscene_bytes'] == RAM.key_card_level_5_cutscene_bytes and self.save_state['key_card_counter'] >= 5:
                if self.save_state['key_card_location_counter'] <= self.save_state['key_card_max_location_counter']:
                    location_name = 'Key Card Level 5'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['key_card_location_counter'] += 1
                    self.save_state['viewed_key_card_cutscene_text'].append(read_values['current_cutscene_text'])
                    has_state_changed = True
            elif read_values['current_cutscene_bytes'] == RAM.key_card_level_6_cutscene_bytes and self.save_state['key_card_counter'] >= 6:
                if self.save_state['key_card_location_counter'] <= self.save_state['key_card_max_location_counter']:
                    location_name = 'Key Card Level 6'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['key_card_location_counter'] += 1
                    self.save_state['viewed_key_card_cutscene_text'].append(read_values['current_cutscene_text'])
                    has_state_changed = True
            elif read_values['current_cutscene_bytes'] == RAM.key_card_level_7_cutscene_bytes and self.save_state['key_card_counter'] >= 7:
                if self.save_state['key_card_location_counter'] <= self.save_state['key_card_max_location_counter']:
                    location_name = 'Key Card Level 7'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['key_card_location_counter'] += 1
                    self.save_state['viewed_key_card_cutscene_text'].append(read_values['current_cutscene_text'])
                    has_state_changed = True

        # I thought it would be funny to trigger a location check for picking up the time bomb but this happens during the part of the game where the client's item pickup checks are disabled
        # Time Bomb
        # if read_values['time_bomb_held'] != 0xFFFF and read_values['time_bomb_held'] > self.save_state['time_bomb_counter']:
        #     write_list.append((RAM.time_bomb_count_address, to_u16_bytes(self.save_state['time_bomb_counter']), 'MainRAM'))
        #     region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
        #     if 'time_bomb' in region_checks.keys():
        #         if region_checks['time_bomb'] < region_checks['time_bomb_max'] and self.save_state['time_bomb_location_counter'] <= self.save_state['time_bomb_max_location_counter']:
        #             location_name = 'Time Bomb ' + str(self.save_state['time_bomb_location_counter'])
        #             self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
        #             self.save_state['time_bomb_location_counter'] += 1
        #             region_checks['time_bomb'] += 1
        #             has_state_changed = True
        #         else:
        #             logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['time_bomb']} of {region_checks['time_bomb_max']} Time Bomb in {read_values['current_region_name']}!")
        #     else:
        #         logger.info(f"[MGS: Masala Garden Salad] Time Bomb not found in: {read_values['current_region_name']}")
        # elif read_values['time_bomb_held'] < self.save_state['time_bomb_counter']:
        #     self.save_state['time_bomb_counter'] = read_values['time_bomb_held']
        #     has_state_changed = True

        # Mine Detector
        if read_values['mine_detector_held'] != 0xFFFF and read_values['mine_detector_held'] > self.save_state['mine_detector_counter']:
            if not self.save_state['has_mine_detector']:
                write_value = 65535
            else:
                write_value = self.save_state['mine_detector_counter']
            write_list.append((RAM.mine_d_count_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'mine_detector' in region_checks.keys():
                if region_checks['mine_detector'] < region_checks['mine_detector_max'] and self.save_state['mine_detector_location_counter'] <= self.save_state['mine_detector_max_location_counter']:
                    location_name = 'Mine Detector'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['mine_detector_location_counter'] += 1
                    region_checks['mine_detector'] += 1
                    has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['mine_detector']} of {region_checks['mine_detector_max']} Mine Detector in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Mine Detector not found in: {read_values['current_region_name']}")

        # Rope
        if read_values['rope_held'] != 0xFFFF and read_values['rope_held'] > self.save_state['rope_counter']:
            if not self.save_state['has_rope']:
                write_value = 65535
            else:
                write_value = self.save_state['rope_counter']
            write_list.append((RAM.rope_count_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'rope' in region_checks.keys():
                if region_checks['rope'] < region_checks['rope_max'] and self.save_state['rope_location_counter'] <= self.save_state['rope_max_location_counter']:
                    location_name = 'Rope'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['rope_location_counter'] += 1
                    region_checks['rope'] += 1
                    has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['rope']} of {region_checks['rope_max']} Rope in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Rope not found in: {read_values['current_region_name']}")
        elif read_values['rope_held'] < self.save_state['rope_counter']:
            self.save_state['rope_counter'] = read_values['rope_held']
            has_state_changed = True

        # Handkerchief
        if read_values['handkerchief_held'] != 0xFFFF and read_values['handkerchief_held'] > self.save_state['handkerchief_counter']:
            write_list.append((RAM.handkerchief_count_address, to_u16_bytes(self.save_state['handkerchief_counter']), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'handkerchief' in region_checks.keys():
                if region_checks['handkerchief'] < region_checks['handkerchief_max'] and self.save_state['handkerchief_location_counter'] <= self.save_state['handkerchief_max_location_counter']:
                    location_name = 'Handkerchief'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['handkerchief_location_counter'] += 1
                    region_checks['handkerchief'] += 1
                    has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['handkerchief']} of {region_checks['handkerchief_max']} Handkerchief in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Handkerchief not found in: {read_values['current_region_name']}")
        elif read_values['handkerchief_held'] < self.save_state['handkerchief_counter']:
            self.save_state['handkerchief_counter'] = read_values['handkerchief_held']
            has_state_changed = True

        # Suppressor
        if read_values['suppressor_held'] != 0xFFFF and read_values['suppressor_held'] > self.save_state['suppressor_counter']:
            if not self.save_state['has_suppressor']:
                write_value = 65535
            else:
                write_value = self.save_state['suppressor_counter']
            write_list.append((RAM.suppressor_count_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'suppressor' in region_checks.keys():
                if region_checks['suppressor'] < region_checks['suppressor_max'] and self.save_state['suppressor_location_counter'] <= self.save_state['suppressor_max_location_counter']:
                    location_name = 'Suppressor'
                    self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
                    self.save_state['suppressor_location_counter'] += 1
                    region_checks['suppressor'] += 1
                    has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['suppressor']} of {region_checks['suppressor_max']} Suppressor in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Suppressor not found in: {read_values['current_region_name']}")
        elif read_values['suppressor_held'] < self.save_state['suppressor_counter']:
            self.save_state['suppressor_counter'] = read_values['suppressor_held']
            has_state_changed = True
        
        # SOCOM
        if read_values['socom_ammo_held'] != 0xFFFF and read_values['socom_ammo_held'] > self.save_state['socom_counter']:
            if not self.save_state['has_socom']:
                write_value = 65535
            else:
                write_value = self.save_state['socom_counter']
            write_list.append((RAM.socom_ammo_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'socom' in region_checks.keys():
                if region_checks['socom'] < region_checks['socom_max'] and self.save_state['socom_location_counter'] <= self.save_state['socom_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'socom')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['socom_location_counter'] += 1
                        region_checks['socom'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['socom']} of {region_checks['socom_max']} SOCOM in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] SOCOM not found in: {read_values['current_region_name']}")
        elif read_values['socom_ammo_held'] < self.save_state['socom_counter']:
            self.save_state['socom_counter'] = read_values['socom_ammo_held']
            has_state_changed = True

        # FA-MAS
        if read_values['famas_ammo_held'] != 0xFFFF and read_values['famas_ammo_held'] > self.save_state['famas_counter']:
            # An ammo value of 0x0000 means the gun is in inventory with 0 ammo
            # An ammo value of 0xFFFF means the gun hasn't been picked up yet and won't show in inventory
            if not self.save_state['has_famas']:
                write_value = 65535
            else:
                write_value = self.save_state['famas_counter']
            write_list.append((RAM.famas_ammo_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'famas' in region_checks.keys():
                if region_checks['famas'] < region_checks['famas_max'] and self.save_state['famas_location_counter'] <= self.save_state['famas_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'famas')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['famas_location_counter'] += 1
                        region_checks['famas'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['famas']} of {region_checks['famas_max']} FA-MAS in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] FA-MAS not found in: {read_values['current_region_name']}")
        elif read_values['famas_ammo_held'] < self.save_state['famas_counter']:
            self.save_state['famas_counter'] = read_values['famas_ammo_held']
            has_state_changed = True

        # Grenade
        if read_values['grenade_ammo_held'] != 0xFFFF and read_values['grenade_ammo_held'] > self.save_state['grenade_counter']:
            # An ammo value of 0x0000 means the gun is in inventory with 0 ammo
            # An ammo value of 0xFFFF means the gun hasn't been picked up yet and won't show in inventory
            if not self.save_state['has_grenade']:
                write_value = 65535
            else:
                write_value = self.save_state['grenade_counter']
            write_list.append((RAM.grenade_ammo_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'grenade' in region_checks.keys():
                if region_checks['grenade'] < region_checks['grenade_max'] and self.save_state['grenade_location_counter'] <= self.save_state['grenade_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'grenade')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['grenade_location_counter'] += 1
                        region_checks['grenade'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['grenade']} of {region_checks['grenade_max']} Grenade in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Grenade not found in: {read_values['current_region_name']}")
        elif read_values['grenade_ammo_held'] < self.save_state['grenade_counter']:
            self.save_state['grenade_counter'] = read_values['grenade_ammo_held']
            has_state_changed = True

        # Nikita
        if read_values['nikita_ammo_held'] != 0xFFFF and read_values['nikita_ammo_held'] > self.save_state['nikita_counter']:
            if not self.save_state['has_nikita']:
                write_value = 65535
            else:
                write_value = self.save_state['nikita_counter']
            write_list.append((RAM.nikita_ammo_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'nikita' in region_checks.keys():
                if region_checks['nikita'] < region_checks['nikita_max'] and self.save_state['nikita_location_counter'] <= self.save_state['nikita_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'nikita')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['nikita_location_counter'] += 1
                        region_checks['nikita'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['nikita']} of {region_checks['nikita_max']} Nikita in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Nikita not found in: {read_values['current_region_name']}")
        elif read_values['nikita_ammo_held'] < self.save_state['nikita_counter']:
            self.save_state['nikita_counter'] = read_values['nikita_ammo_held']
            has_state_changed = True

        # Stinger
        if read_values['stinger_ammo_held'] != 0xFFFF and read_values['stinger_ammo_held'] > self.save_state['stinger_counter']:
            if not self.save_state['has_stinger']:
                write_value = 65535
            else:
                write_value = self.save_state['stinger_counter']
            write_list.append((RAM.stinger_ammo_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'stinger' in region_checks.keys():
                if region_checks['stinger'] < region_checks['stinger_max'] and self.save_state['stinger_location_counter'] <= self.save_state['stinger_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'stinger')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['stinger_location_counter'] += 1
                        region_checks['stinger'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['stinger']} of {region_checks['stinger_max']} Stinger in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Stinger not found in: {read_values['current_region_name']}")
        elif read_values['stinger_ammo_held'] < self.save_state['stinger_counter']:
            self.save_state['stinger_counter'] = read_values['stinger_ammo_held']
            has_state_changed = True

        # Claymore
        if read_values['claymore_ammo_held'] != 0xFFFF and read_values['claymore_ammo_held'] > self.save_state['claymore_counter']:
            if not self.save_state['has_claymore']:
                write_value = 65535
            else:
                write_value = self.save_state['claymore_counter']
            write_list.append((RAM.claymore_ammo_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'claymore' in region_checks.keys():
                if region_checks['claymore'] < region_checks['claymore_max'] and self.save_state['claymore_location_counter'] <= self.save_state['claymore_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'claymore')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['claymore_location_counter'] += 1
                        region_checks['claymore'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['claymore']} of {region_checks['claymore_max']} Claymore in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Claymore not found in: {read_values['current_region_name']}")
        elif read_values['claymore_ammo_held'] < self.save_state['claymore_counter']:
            self.save_state['claymore_counter'] = read_values['claymore_ammo_held']
            has_state_changed = True

        # C4
        if read_values['c4_ammo_held'] != 0xFFFF and read_values['c4_ammo_held'] > self.save_state['c4_counter']:
            if not self.save_state['has_c4']:
                write_value = 65535
            else:
                write_value = self.save_state['c4_counter']
            write_list.append((RAM.c4_ammo_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'c4' in region_checks.keys():
                if region_checks['c4'] < region_checks['c4_max'] and self.save_state['c4_location_counter'] <= self.save_state['c4_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'c4')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['c4_location_counter'] += 1
                        region_checks['c4'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['c4']} of {region_checks['c4_max']} C4 in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] C4 not found in: {read_values['current_region_name']}")
        elif read_values['c4_ammo_held'] < self.save_state['c4_counter']:
            self.save_state['c4_counter'] = read_values['c4_ammo_held']
            has_state_changed = True

         # Stun Grenade
        if read_values['stun_grenade_held'] != 0xFFFF and read_values['stun_grenade_held'] > self.save_state['stun_grenade_counter']:
            if not self.save_state['has_stun_grenade']:
                write_value = 65535
            else:
                write_value = self.save_state['stun_grenade_counter']
            write_list.append((RAM.stun_g_ammo_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'stun_grenade' in region_checks.keys():
                if region_checks['stun_grenade'] < region_checks['stun_grenade_max'] and self.save_state['stun_grenade_location_counter'] <= self.save_state['stun_grenade_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'stun_grenade')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['stun_grenade_location_counter'] += 1
                        region_checks['stun_grenade'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['stun_grenade']} of {region_checks['stun_grenade_max']} Stun Grenade in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Stun Grenade not found in: {read_values['current_region_name']}")
        elif read_values['stun_grenade_held'] < self.save_state['stun_grenade_counter']:
            self.save_state['stun_grenade_counter'] = read_values['stun_grenade_held']
            has_state_changed = True

        # Chaff Grenade
        if read_values['chaff_grenade_held'] != 0xFFFF and read_values['chaff_grenade_held'] > self.save_state['chaff_grenade_counter']:
            if not self.save_state['has_chaff_grenade']:
                write_value = 65535
            else:
                write_value = self.save_state['chaff_grenade_counter']
            write_list.append((RAM.chaff_g_ammo_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'chaff_grenade' in region_checks.keys():
                if region_checks['chaff_grenade'] < region_checks['chaff_grenade_max'] and self.save_state['chaff_grenade_location_counter'] <= self.save_state['chaff_grenade_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'chaff_grenade')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['chaff_grenade_location_counter'] += 1
                        region_checks['chaff_grenade'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['chaff_grenade']} of {region_checks['chaff_grenade_max']} Chaff Grenade in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] Chaff Grenade not found in: {read_values['current_region_name']}")
        elif read_values['chaff_grenade_held'] < self.save_state['chaff_grenade_counter']:
            self.save_state['chaff_grenade_counter'] = read_values['chaff_grenade_held']
            has_state_changed = True

        # PSG-1
        if read_values['psg1_ammo_held'] != 0xFFFF and read_values['psg1_ammo_held'] > self.save_state['psg1_counter']:
            if not self.save_state['has_psg1']:
                write_value = 65535
            else:
                write_value = self.save_state['psg1_counter']
            write_list.append((RAM.psg1_ammo_address, to_u16_bytes(write_value), 'MainRAM'))
            region_checks: dict = self.save_state['checks_per_region_tracker'][read_values['current_region_name']]
            if 'psg1' in region_checks.keys():
                if region_checks['psg1'] < region_checks['psg1_max'] and self.save_state['psg1_location_counter'] <= self.save_state['psg1_max_location_counter']:
                    location_name = self.get_next_region_location_name(read_values['current_region_name'], 'psg1')
                    if location_name is not None and self.queue_location(location_name):
                        self.save_state['psg1_location_counter'] += 1
                        region_checks['psg1'] += 1
                        has_state_changed = True
                else:
                    logger.info(f"[MGS: Masala Garden Salad] Already picked up {region_checks['psg1']} of {region_checks['psg1_max']} PSG-1 in {read_values['current_region_name']}!")
            else:
                logger.info(f"[MGS: Masala Garden Salad] PSG-1 not found in: {read_values['current_region_name']}")
        elif read_values['psg1_ammo_held'] < self.save_state['psg1_counter']:
            self.save_state['psg1_counter'] = read_values['psg1_ammo_held']
            has_state_changed = True
        return has_state_changed

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        memory_size = await bizhawk.get_memory_size(ctx.bizhawk_ctx, 'MainRAM')
        if memory_size >= RAM.psx_MainRAM_memorysize:
            # mgs_identifier_ram_address: int = 0x010724
            # 4D475300 = MGS.
            bytes_expected: bytes = bytes.fromhex("4D475300")
            try:
                # Check ROM name/patch version
                bytes_actual: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                    RAM.mgs_ROM_address, len(bytes_expected), "MainRAM"
                )]))[0]
                if bytes_actual != bytes_expected:
                    return False
            except bizhawk.RequestFailedError:
                logger.info('No valid ROM found')
                return False  # Not able to get a response, say no for now
            
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.command_processor.commands['check_goal'] = cmd_check_goal
        ctx.command_processor.commands['check_collection'] = cmd_check_collection
        ctx.command_processor.commands['kill_mantis'] = cmd_kill_mantis


        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:

        # Don't run game_watcher if not connected to an archipelago server
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None or ctx.auth is None:
            return

        # Goal completion is from receiving the locked Victory item. 
		# It didn't seem to want to pop before, so let's "force it" the same way
		# we do in RE3 basically
        await self.check_received_victory(ctx)
        
        # === HANDLE RAM READING === #
        reads_dict = {
            'cbox_a_held': (RAM.cbox_a_count_address, 2, 'MainRAM'),
            'cbox_a_on_death': (RAM.cbox_a_death_count_address, 2, 'MainRAM'),
            'cbox_b_held': (RAM.cbox_b_count_address, 2, 'MainRAM'),
            'cbox_b_on_death': (RAM.cbox_b_death_count_address, 2, 'MainRAM'),
            'cbox_c_held': (RAM.cbox_c_count_address, 2, 'MainRAM'),
            'cbox_c_on_death': (RAM.cbox_c_death_count_address, 2, 'MainRAM'),
            'night_vision_goggles_held': (RAM.nvg_count_address, 2, 'MainRAM'),
            'night_vision_goggles_on_death': (RAM.nvg_death_count_address, 2, 'MainRAM'),
            'thermal_goggles_held': (RAM.therm_g_count_address, 2, 'MainRAM'),
            'thermal_goggles_on_death': (RAM.therm_g_death_count_address, 2, 'MainRAM'),
            'gasmask_held': (RAM.gasmask_count_address, 2, 'MainRAM'),
            'gasmask_on_death': (RAM.gasmask_death_count_address, 2, 'MainRAM'),
            'body_armor_held': (RAM.b_armor_count_address, 2, 'MainRAM'),
            'body_armor_on_death': (RAM.b_armor_death_count_address, 2, 'MainRAM'),
            'camera_held': (RAM.camera_count_address, 2, 'MainRAM'),
            'camera_on_death': (RAM.camera_death_count_address, 2, 'MainRAM'),
            'rations_held': (RAM.rations_count_address, 2, 'MainRAM'),
            'rations_on_death': (RAM.rations_death_count_address, 2, 'MainRAM'),
            'rations_max': (RAM.rations_max_address, 2, 'MainRAM'),
            'medicine_held': (RAM.medicine_count_address, 2, 'MainRAM'),
            'medicine_on_death': (RAM.medicine_death_count_address, 2, 'MainRAM'),
            'diazepam_held': (RAM.diazepam_count_address, 2, 'MainRAM'),
            'diazepam_on_death': (RAM.diazepam_death_count_address, 2, 'MainRAM'),
            'diazepam_max': (RAM.diazepam_max_address, 2, 'MainRAM'),
            'pal_key_held': (RAM.pal_key_count_address, 2, 'MainRAM'),
            'pal_key_on_death': (RAM.pal_key_death_count_address, 2, 'MainRAM'),
            'key_card_held': (RAM.key_card_count_address, 2, 'MainRAM'),
            'key_card_on_death': (RAM.key_card_death_count_address, 2, 'MainRAM'),
            'time_bomb_held': (RAM.time_bomb_count_address, 2, 'MainRAM'),
            'time_bomb_on_death': (RAM.time_bomb_death_count_address, 2, 'MainRAM'),
            'mine_detector_held': (RAM.mine_d_count_address, 2, 'MainRAM'),
            'mine_detector_on_death': (RAM.mind_d_death_count_address, 2, 'MainRAM'),
            'rope_held': (RAM.rope_count_address, 2, 'MainRAM'),
            'rope_on_death': (RAM.rope_death_count_address, 2, 'MainRAM'),
            'handkerchief_held': (RAM.handkerchief_count_address, 2, 'MainRAM'),
            'handkerchief_on_death': (RAM.handkerchief_death_count_address, 2, 'MainRAM'),
            'suppressor_held': (RAM.suppressor_count_address, 2, 'MainRAM'),
            'suppressor_on_death': (RAM.suppressor_death_count_address, 2, 'MainRAM'),
            'socom_ammo_held': (RAM.socom_ammo_address, 2, 'MainRAM'),
            'socom_ammo_on_death': (RAM.socom_death_ammo_address, 2, 'MainRAM'),
            'socom_max': (RAM.socom_max_ammo_address, 2, 'MainRAM'),
            'famas_ammo_held': (RAM.famas_ammo_address, 2, 'MainRAM'),
            'famas_ammo_on_death': (RAM.famas_death_ammo_address, 2, 'MainRAM'),
            'famas_max': (RAM.famas_max_ammo_address, 2, 'MainRAM'),
            'grenade_ammo_held': (RAM.grenade_ammo_address, 2, 'MainRAM'),
            'grenade_ammo_on_death': (RAM.grenade_death_ammo_address, 2, 'MainRAM'),
            'grenade_max': (RAM.grenade_max_ammo_address, 2, 'MainRAM'),
            'nikita_ammo_held': (RAM.nikita_ammo_address, 2, 'MainRAM'),
            'nikita_ammo_on_death': (RAM.nikita_death_ammo_address, 2, 'MainRAM'),
            'nikita_max': (RAM.nikita_max_ammo_address, 2, 'MainRAM'),
            'stinger_ammo_held': (RAM.stinger_ammo_address, 2, 'MainRAM'),
            'stinger_ammo_on_death': (RAM.stinger_death_ammo_address, 2, 'MainRAM'),
            'stinger_max': (RAM.stinger_max_ammo_address, 2, 'MainRAM'),
            'claymore_ammo_held': (RAM.claymore_ammo_address, 2, 'MainRAM'),
            'claymore_ammo_on_death': (RAM.claymore_death_ammo_address, 2, 'MainRAM'),
            'claymore_max': (RAM.claymore_max_ammo_address, 2, 'MainRAM'),
            'c4_ammo_held': (RAM.c4_ammo_address, 2, 'MainRAM'),
            'c4_ammo_on_death': (RAM.c4_death_ammo_address, 2, 'MainRAM'),
            'c4_max': (RAM.c4_max_ammo_address, 2, 'MainRAM'),
            'stun_grenade_held': (RAM.stun_g_ammo_address, 2, 'MainRAM'),
            'stun_grenade_on_death': (RAM.stun_g_death_ammo_address, 2, 'MainRAM'),
            'stun_grenade_max': (RAM.stun_g_max_ammo_address, 2, 'MainRAM'),
            'chaff_grenade_held': (RAM.chaff_g_ammo_address, 2, 'MainRAM'),
            'chaff_grenade_on_death': (RAM.chaff_g_death_ammo_address, 2, 'MainRAM'),
            'chaff_grenade_max': (RAM.chaff_g_max_ammo_address, 2, 'MainRAM'),
            'psg1_ammo_held': (RAM.psg1_ammo_address, 2, 'MainRAM'),
            'psg1_ammo_on_death': (RAM.psg1_death_ammo_address, 2, 'MainRAM'),
            'psg1_max': (RAM.psg1_max_ammo_address, 2, 'MainRAM'),
            'current_region_high_offset': (RAM.current_region_high_offset_address, 2, 'MainRAM'),
            'current_region_low_offset': (RAM.current_region_low_offset_address, 2, 'MainRAM'),
            'is_game_over': (RAM.game_over_screen_counter, 2, 'MainRAM'),
        }

        # HACK MGS: Set to True for God Mode!
        is_debug = False
        # === FOR DEBUG! === #
        if is_debug:
            reads_dict['stealth_camouflage_held'] = (RAM.stealth_count_address, 2, 'MainRAM')
            reads_dict['bandana_held'] = (RAM.bandana_count_address, 2, 'MainRAM')
            reads_dict['current_health'] = (RAM.current_health, 2, 'MainRAM')
            reads_dict['current_health_alt'] = (RAM.current_health_alt, 2, 'MainRAM')
            reads_dict['current_max_health'] = (RAM.current_max_health, 2, 'MainRAM')
            reads_dict['current_o2'] = (RAM.current_oxygen_level, 2, 'MainRAM')
        # === FOR DEBUG! === #

        # Convert RAM readings into decimal numbers and store them in a dictionary
        reads_tuple = [value for value in reads_dict.values()]
        reads = await bizhawk.read(ctx.bizhawk_ctx, reads_tuple)
        # convert all the bytes into a decimal number
        reads = [int.from_bytes(reads[i], byteorder='little') for i,_ in enumerate(reads)]
        # create a dictionary where the keys from reads_dict will now pair with a decimal value
        read_values: dict[str, Any] = dict(zip(reads_dict.keys(), reads))

        # Another RAM read, but cutscene bytes can't be converted to a decimal so adding it to reads_dict causes problems
        # The additional read doesn't seem to impact performance from my testing
        current_cutscene_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(RAM.cutscene_text_address_primary, 12, 'MainRAM')]))[0]
        try:
            current_cutscene_text = current_cutscene_bytes.decode()
        except UnicodeDecodeError:
            current_cutscene_text = ''
        read_values['current_cutscene_bytes'] = current_cutscene_bytes
        read_values['current_cutscene_text'] = current_cutscene_text

        # During capture, owned inventory remains in RAM with its high bit set
        # (for example, 0x001B becomes 0x801B). Detect that state directly so
        # connecting midway through capture cannot restore Snake's equipment.
        capture_inventory_keys = (
            'cbox_a_held', 'cbox_b_held', 'cbox_c_held',
            'night_vision_goggles_held', 'thermal_goggles_held',
            'gasmask_held', 'body_armor_held', 'camera_held', 'rations_held',
            'medicine_held', 'diazepam_held', 'pal_key_held',
            'key_card_held', 'time_bomb_held', 'mine_detector_held',
            'rope_held', 'handkerchief_held', 'suppressor_held',
            'socom_ammo_held', 'famas_ammo_held', 'grenade_ammo_held',
            'nikita_ammo_held', 'stinger_ammo_held',
            'claymore_ammo_held', 'c4_ammo_held',
            'stun_grenade_held', 'chaff_grenade_held', 'psg1_ammo_held',
        )
        capture_inventory_masked = any(
            0x8000 <= read_values[key] < 0xFFFF
            for key in capture_inventory_keys
        )

        has_state_changed = False # Track if save_state has been updated. It needs to be saved to a json file if it has.
        if capture_inventory_masked and not self.save_state['is_captured']:
            self.save_state['is_captured'] = True
            has_state_changed = True
        write_list = [] # Track all the writes BizHawk should make to the game's RAM
        # The first watcher pass restores the AP client's saved inventory into RAM.
        # All reads in this pass were captured before that restore, so they must not
        # be interpreted as new pickups, deaths, or location-triggering events.
        initial_sync = self.run_once

        # === HANDLE CUTSCENE VIEW === #
        # Certain cutscenes provide items and trigger Archipeligo location checks. This is where those are handled.
        # Note: 'Game Completion' run goal is tracker here
        if not initial_sync:
            for cutscene_bytes in RAM.boss_cutscene_bytes_to_location_list.keys():
                if current_cutscene_bytes == cutscene_bytes and current_cutscene_text not in self.save_state['viewed_boss_cutscene_bytes']:
                    location_name = RAM.boss_cutscene_bytes_to_location_list[cutscene_bytes]
                    # Normal item handling is disabled when locked up in the cell, but Otacon will provide the player with items. These need to be handled.
                    if location_name == 'Otacon Gifts':
                        self.save_state['handkerchief_location_counter'] += 1
                        self.save_state['handkerchief_counter'] += 1
                        self.locations_to_send += [self.location_name_to_server_location_id['Handkerchief']]
                    
                        self.save_state['key_card_location_counter'] += 1
                        self.locations_to_send += [self.location_name_to_server_location_id['Key Card Level 6']]

                        # Otacon's scripted Level 6 card is a location check, not a
                        # progressive Key Card item. Keep the AP-owned key-card level
                        # unchanged; if this location contains a Key Card, the normal
                        # received-item path will increase it exactly once.
                        key_card_write_value = self.save_state['key_card_counter']
                        if 0x8000 <= read_values['key_card_held'] < 0xFFFF:
                            key_card_write_value |= 0x8000
                        write_list.append((
                            RAM.key_card_count_address,
                            to_u16_bytes(key_card_write_value),
                            'MainRAM'
                        ))
                        write_list.append((
                            RAM.key_card_death_count_address,
                            to_u16_bytes(self.save_state['key_card_counter']),
                            'MainRAM'
                        ))

                        # Otacon gives Snake the Medi Room ration during this cutscene.
                        # Use the region-aware location name instead of advancing the
                        # legacy global Ration counter first (which incorrectly looked
                        # for the next area's Ration 21 after the regional rename).
                        ration_region = 'medi room'
                        ration_location_name = self.get_next_region_location_name(ration_region, 'rations')
                        self.save_state['rations_counter'] += 1

                        if ration_location_name is not None and self.queue_location(ration_location_name):
                            self.save_state['rations_location_counter'] += 1
                            ration_region_checks = self.save_state['checks_per_region_tracker'][ration_region]
                            ration_region_checks['rations'] += 1
                        elif ration_location_name is None:
                            logger.info('[MGS: Masala Garden Salad] No unsent Medi Room ration location was found for Otacon Gifts.')

                        has_state_changed = True
                    
                    else:
                        self.queue_location(location_name)
                        if location_name == 'BOSS: Revolver Ocelot':
                            # Baker's Level 2 Key Card location belongs to the same
                            # story sequence. Queue it from the Ocelot cutscene itself
                            # so randomizing Progressive Key Cards cannot suppress it.
                            if self.queue_location('Key Card Level 2'):
                                self.save_state['key_card_location_counter'] = max(
                                    self.save_state['key_card_location_counter'],
                                    3,
                                )
                                if current_cutscene_text not in self.save_state['viewed_key_card_cutscene_text']:
                                    self.save_state['viewed_key_card_cutscene_text'].append(current_cutscene_text)
                                logger.info(
                                    '[MGS: Masala Garden Salad] Paired Revolver Ocelot with Key Card Level 2.'
                                )
                        elif location_name == 'BOSS: Gray Fox':
                            if self.queue_location('Key Card Level 4'):
                                self.save_state['key_card_location_counter'] = max(self.save_state['key_card_location_counter'], 5)
                                if current_cutscene_text not in self.save_state['viewed_key_card_cutscene_text']:
                                    self.save_state['viewed_key_card_cutscene_text'].append(current_cutscene_text)
                        elif location_name == 'BOSS: Vulcan Raven':
                            if self.queue_location('Key Card Level 7'):
                                self.save_state['key_card_location_counter'] = max(self.save_state['key_card_location_counter'], 8)
                                if current_cutscene_text not in self.save_state['viewed_key_card_cutscene_text']:
                                    self.save_state['viewed_key_card_cutscene_text'].append(current_cutscene_text)
                    assert isinstance(self.save_state['viewed_boss_cutscene_bytes'],list) # stops IDEs from complaining that save_state['viewed_boss_cutscene_bytes'] might not return a list.
                    self.save_state['viewed_boss_cutscene_bytes'].append(current_cutscene_text)
                    has_state_changed = True
                    if location_name == 'BOSS: Sniper Wolf I':
                        self.save_state['is_captured'] = True
                    elif location_name == 'BOSS: A Hind D?':
                        self.save_state['has_defeated_hind'] = True
                    elif location_name == 'BOSS: Metal Gear REX':
                        self.save_state['endgame_inventory_locked'] = True
                        self.save_state['endgame_rations_last_seen'] = read_values['rations_held']
                        logger.info(
                            '[MGS: Masala Garden Salad] Endgame inventory lock enabled. '
                            'Server-granted gear will be withheld through the Liquid fight and Escape Route.'
                        )

        # === HANDLE READING CURRENT REGION === #
        # When the player pauses, a region name is displayed on screen. The location of this text in RAM moves, but is pointed to by 4 bytes at a known location
        # A 'high_offset' of 8015 and 'low_offset' of 3E00 means the current region string is found at 0x153E00
        high_offset_bytestring = '{0:x}'.format(read_values['current_region_high_offset'])[2:]
        low_offset_bytestring = '{0:x}'.format(read_values['current_region_low_offset'])
        # ensure 0x00AA is represented as '00AA' and not 'AA'
        if len(low_offset_bytestring) < 4:
            pad_string = '0' * (4 - len(low_offset_bytestring))
            low_offset_bytestring = ''.join([pad_string, low_offset_bytestring])
        offset_bytestring = ''.join([high_offset_bytestring, low_offset_bytestring])
        current_region_address = int(offset_bytestring, 16)
        if current_region_address > 0:
            # Another read, this is now 3 read calls per frame. Again, it doesn't seem to hurt performance.
            current_region_read = (await bizhawk.read(ctx.bizhawk_ctx, [(current_region_address, 16, 'MainRAM')]))[0]
            try:
                current_region_name = current_region_read.split(b'\x00')[0].decode()[2:-2].lower()
            except UnicodeDecodeError: # exceptions shouldn't happen, but if they do, just bail out early
                return
            if current_region_name == 'comm twr b' and self.save_state.get('has_defeated_hind', False):
                current_region_name = 'comm twr b hind defeated'
            read_values['current_region_name'] = current_region_name
            self.current_region = current_region_name
        else:
            # HACK MGS: This is repeated code. It also appears at the end of the game_watcher function. It should be pulled out into it's own function. I'm just lazy right now!
            if len(self.locations_to_send) > 0:
                await ctx.check_locations(self.locations_to_send)
                self.locations_to_send.clear()
            if has_state_changed:
                with open(self.save_file, 'w') as save:
                    json.dump(self.save_state, save)
                has_state_changed = False
            return

        # All regions in the game should appear in the regions list, unless I've yet to discover a secret area!
        if current_region_name not in self.save_state['regions']:
            logger.debug(f'[Metal Gear Solid - DEBUG] Region: \"{current_region_name}\", not found in list of valid regions! high: {high_offset_bytestring}, low: {low_offset_bytestring}, Current Region Address: 0x{current_region_address:x}')
            return
        
        # After escaping the torture room and regaining your items, the next area you'll have access to is 'cell'
        # If the player makes it to 'cell', they are no longer captured
        if (
            current_region_name == 'cell'
            and self.save_state['is_captured']
            and not capture_inventory_masked
        ):
            self.save_state['is_captured'] = False
            # Inventory restoration and RAM writes can span several watcher
            # polls. Suppress only the misleading duplicate Ration message
            # during that short transition; normal pickup detection remains on.
            self.suppress_post_capture_ration_messages_until = time.monotonic() + 3.0
            has_state_changed = True
        # After defeating the Stealth Camouflaged Genome Soldiers, the player goes right into the Sniper Wolf II battle.
        # Allow the player to collect their BOSS: Stealth Camouflaged Genome Soldiers location check before the next fight!
        elif not initial_sync and current_region_name == 'snowfield' and not self.save_state['has_snowfield']:
            self.save_state['has_snowfield'] = True
            location_name = 'BOSS: Stealth Camouflaged Genome Soldiers'
            self.locations_to_send += [self.location_name_to_server_location_id[location_name]]
            has_state_changed = True

        # === HANDLE KILL MANTIS COMMAND === #
        # I couldn't figure out how to use 'await' (needed for BizHawk to write to RAM) outside of game_watcher(), so this lives here.
        if self.kill_mantis_command:
            if current_region_name == 'cmnder room':
                zero = 0x0000
                write_list.append((RAM.psyco_mantis_current_health, to_u16_bytes(zero), 'MainRAM'))
                if ctx.slot:
                    # Techinically a cheat. I think it should be announced just like other cheat console commands
                    await ctx.send_msgs([{
                        "cmd": "Say",
                        "text": f'I used a cheat to kill Psycho Mantis!'
                        }])
            else:
                logger.info('[MGS: Masala Garden Salad] You must be in the Commander Room to use this command!')
            self.kill_mantis_command = False


        # When loading up a save file, Write all values from Save State to RAM
        # Not doing this can cause the handle_item_pickups() function to assume the player has lost all their ammo
        if (
            self.run_once
            and not self.save_state['is_captured']
            and not self.save_state.get('endgame_inventory_locked', False)
        ):
            if self.save_state['has_cbox_a']:
                write_list.append((RAM.cbox_a_count_address, to_u16_bytes(self.save_state['cbox_a_counter']), 'MainRAM'))
                write_list.append((RAM.cbox_a_death_count_address, to_u16_bytes(self.save_state['cbox_a_counter']), 'MainRAM'))
            if self.save_state['has_cbox_b']:
                write_list.append((RAM.cbox_b_count_address, to_u16_bytes(self.save_state['cbox_b_counter']), 'MainRAM'))
                write_list.append((RAM.cbox_b_death_count_address, to_u16_bytes(self.save_state['cbox_b_counter']), 'MainRAM'))
            if self.save_state['has_cbox_c']:
                write_list.append((RAM.cbox_c_count_address, to_u16_bytes(self.save_state['cbox_c_counter']), 'MainRAM'))
                write_list.append((RAM.cbox_c_death_count_address, to_u16_bytes(self.save_state['cbox_c_counter']), 'MainRAM'))
            if self.save_state['has_night_vision_goggles']:
                write_list.append((RAM.nvg_count_address, to_u16_bytes(self.save_state['night_vision_goggles_counter']), 'MainRAM'))
                write_list.append((RAM.nvg_death_count_address, to_u16_bytes(self.save_state['night_vision_goggles_counter']), 'MainRAM'))
            if self.save_state['has_thermal_goggles']:
                write_list.append((RAM.therm_g_count_address, to_u16_bytes(self.save_state['thermal_goggles_counter']), 'MainRAM'))
                write_list.append((RAM.therm_g_death_count_address, to_u16_bytes(self.save_state['thermal_goggles_counter']), 'MainRAM'))
            if self.save_state['has_gasmask']:
                write_list.append((RAM.gasmask_count_address, to_u16_bytes(self.save_state['gasmask_counter']), 'MainRAM'))
                write_list.append((RAM.gasmask_death_count_address, to_u16_bytes(self.save_state['gasmask_counter']), 'MainRAM'))
            if self.save_state['has_body_armor']:
                write_list.append((RAM.b_armor_count_address, to_u16_bytes(self.save_state['body_armor_counter']), 'MainRAM'))
                write_list.append((RAM.b_armor_death_count_address, to_u16_bytes(self.save_state['body_armor_counter']), 'MainRAM'))
            if self.save_state['has_camera']:
                write_list.append((RAM.camera_count_address, to_u16_bytes(self.save_state['camera_counter']), 'MainRAM'))
                write_list.append((RAM.camera_death_count_address, to_u16_bytes(self.save_state['camera_counter']), 'MainRAM'))
            write_list.append((RAM.rations_count_address, to_u16_bytes(self.save_state['rations_counter']), 'MainRAM'))
            write_list.append((RAM.rations_death_count_address, to_u16_bytes(self.save_state['rations_counter']), 'MainRAM'))
            write_list.append((RAM.medicine_count_address, to_u16_bytes(self.save_state['medicine_counter']), 'MainRAM'))
            write_list.append((RAM.medicine_death_count_address, to_u16_bytes(self.save_state['medicine_counter']), 'MainRAM'))
            write_list.append((RAM.diazepam_count_address, to_u16_bytes(self.save_state['diazepam_counter']), 'MainRAM'))
            write_list.append((RAM.diazepam_death_count_address, to_u16_bytes(self.save_state['diazepam_counter']), 'MainRAM'))
            write_list.append((RAM.pal_key_count_address, to_u16_bytes(self.save_state['pal_key_counter']), 'MainRAM'))
            write_list.append((RAM.pal_key_death_count_address, to_u16_bytes(self.save_state['pal_key_counter']), 'MainRAM'))
            write_list.append((RAM.key_card_count_address, to_u16_bytes(self.save_state['key_card_counter']), 'MainRAM'))
            write_list.append((RAM.key_card_death_count_address, to_u16_bytes(self.save_state['key_card_counter']), 'MainRAM'))
            if self.save_state['has_mine_detector']:
                write_list.append((RAM.mine_d_count_address, to_u16_bytes(self.save_state['mine_detector_counter']), 'MainRAM'))
                write_list.append((RAM.mind_d_death_count_address, to_u16_bytes(self.save_state['mine_detector_counter']), 'MainRAM'))
            if self.save_state['has_rope']:
                write_list.append((RAM.rope_count_address, to_u16_bytes(self.save_state['rope_counter']), 'MainRAM'))
                write_list.append((RAM.rope_death_count_address, to_u16_bytes(self.save_state['rope_counter']), 'MainRAM'))
            write_list.append((RAM.handkerchief_count_address, to_u16_bytes(self.save_state['handkerchief_counter']), 'MainRAM'))
            write_list.append((RAM.handkerchief_death_count_address, to_u16_bytes(self.save_state['handkerchief_counter']), 'MainRAM'))
            if self.save_state['has_suppressor']:
                write_list.append((RAM.suppressor_count_address, to_u16_bytes(self.save_state['suppressor_counter']), 'MainRAM'))
                write_list.append((RAM.suppressor_death_count_address, to_u16_bytes(self.save_state['suppressor_counter']), 'MainRAM'))
            if self.save_state['has_socom']:
                write_list.append((RAM.socom_ammo_address, to_u16_bytes(self.save_state['socom_counter']), 'MainRAM'))
                write_list.append((RAM.socom_death_ammo_address, to_u16_bytes(self.save_state['socom_counter']), 'MainRAM'))
            if self.save_state['has_famas']:
                write_list.append((RAM.famas_ammo_address, to_u16_bytes(self.save_state['famas_counter']), 'MainRAM'))
                write_list.append((RAM.famas_death_ammo_address, to_u16_bytes(self.save_state['famas_counter']), 'MainRAM'))
            if self.save_state['has_grenade']:
                write_list.append((RAM.grenade_ammo_address, to_u16_bytes(self.save_state['grenade_counter']), 'MainRAM'))
                write_list.append((RAM.grenade_death_ammo_address, to_u16_bytes(self.save_state['grenade_counter']), 'MainRAM'))
            if self.save_state['has_nikita']:
                write_list.append((RAM.nikita_ammo_address, to_u16_bytes(self.save_state['nikita_counter']), 'MainRAM'))
                write_list.append((RAM.nikita_death_ammo_address, to_u16_bytes(self.save_state['nikita_counter']), 'MainRAM'))
            if self.save_state['has_stinger']:
                write_list.append((RAM.stinger_ammo_address, to_u16_bytes(self.save_state['stinger_counter']), 'MainRAM'))
                write_list.append((RAM.stinger_death_ammo_address, to_u16_bytes(self.save_state['stinger_counter']), 'MainRAM'))
            if self.save_state['has_claymore']:
                write_list.append((RAM.claymore_ammo_address, to_u16_bytes(self.save_state['claymore_counter']), 'MainRAM'))
                write_list.append((RAM.claymore_death_ammo_address, to_u16_bytes(self.save_state['claymore_counter']), 'MainRAM'))
            if self.save_state['has_c4']:
                write_list.append((RAM.c4_ammo_address, to_u16_bytes(self.save_state['c4_counter']), 'MainRAM'))
                write_list.append((RAM.c4_death_ammo_address, to_u16_bytes(self.save_state['c4_counter']), 'MainRAM'))
            if self.save_state['has_stun_grenade']:
                write_list.append((RAM.stun_g_ammo_address, to_u16_bytes(self.save_state['stun_grenade_counter']), 'MainRAM'))
                write_list.append((RAM.stun_g_death_ammo_address, to_u16_bytes(self.save_state['stun_grenade_counter']), 'MainRAM'))
            if self.save_state['has_chaff_grenade']:
                write_list.append((RAM.chaff_g_ammo_address, to_u16_bytes(self.save_state['chaff_grenade_counter']), 'MainRAM'))
                write_list.append((RAM.chaff_g_death_ammo_address, to_u16_bytes(self.save_state['chaff_grenade_counter']), 'MainRAM'))
            if self.save_state['has_psg1']:
                write_list.append((RAM.psg1_ammo_address, to_u16_bytes(self.save_state['psg1_counter']), 'MainRAM'))
                write_list.append((RAM.psg1_death_ammo_address, to_u16_bytes(self.save_state['psg1_counter']), 'MainRAM'))
            # === FOR DEBUG! === #
            if is_debug:
                logger.info('[MGS: Masala Garden Salad] DEBUG MODE ENABLED!')
                logger.info('[MGS: Masala Garden Salad] Stealth Camouflage, Bandana, Infinite Oxygen, and Infinite Health added!')
                one = 1
                write_list.append((RAM.stealth_count_address,  to_u16_bytes(one), 'MainRAM'))
                write_list.append((RAM.bandana_count_address,  to_u16_bytes(one), 'MainRAM'))
                write_list.append((RAM.current_health,  to_u16_bytes(read_values['current_max_health']), 'MainRAM'))
            # Write these immediately before handle_item_pickups() is called
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
            write_list.clear()
            self.run_once = False
        elif self.run_once:
            # Capture blocked the initial inventory restore, but the first-pass
            # synchronization guard must still expire so Otacon and later
            # cutscene checks can be observed while Snake remains captured.
            self.run_once = False

        # === FOR DEBUG! === #
        if is_debug:
            if read_values['current_health'] < read_values['current_max_health']:
                write_list.append((RAM.current_health, to_u16_bytes(read_values['current_max_health']), 'MainRAM'))
            # Health is tracked at a different location in RAM during the helicopter rappel. It's also somewhere different during the torture scene but I haven't found it yet.
            # This doesn't make failing the torture scene impossible. Just slow emulation speed to 75%!
            if read_values['current_region_name'] == 'twr wall a' or read_values['current_region_name'] == 'medi room':
                if read_values['current_health_alt'] < read_values['current_max_health']:
                    write_list.append((RAM.current_health_alt, to_u16_bytes(read_values['current_max_health']), 'MainRAM'))
            if read_values['stealth_camouflage_held'] < 1:
                one = 1
                write_list.append((RAM.stealth_count_address,  to_u16_bytes(one), 'MainRAM'))
            if read_values['bandana_held'] < 1:
                one = 1
                write_list.append((RAM.bandana_count_address,  to_u16_bytes(one), 'MainRAM'))
            if read_values['current_o2'] < 0x400:
                four_hundred_hex = 0x400
                write_list.append((RAM.current_oxygen_level,  to_u16_bytes(four_hundred_hex), 'MainRAM'))

        # === ENSURE MAX ITEMS ARE HIGHER THAN NORMAL === #
        # The player cannot pickup an item if they're already carrying the maximum amount.
        # Having full FA-MAS ammo means the player cannot check any more FA-MAS locations!
        # Ensure that doesn't happen by upping the max item count to a large number
        if read_values['rations_max'] != self.max_items:
            write_list.append((RAM.rations_max_address, to_u16_bytes(self.max_items), 'MainRAM'))
        if read_values['diazepam_max'] != self.max_items:
            write_list.append((RAM.diazepam_max_address, to_u16_bytes(self.max_items), 'MainRAM'))
        if read_values['socom_max'] != self.max_items:
            write_list.append((RAM.socom_max_ammo_address, to_u16_bytes(self.max_items), 'MainRAM'))
        if read_values['famas_max'] != self.max_items:
            write_list.append((RAM.famas_max_ammo_address, to_u16_bytes(self.max_items), 'MainRAM'))
        if read_values['grenade_max'] != self.max_items:
            write_list.append((RAM.grenade_max_ammo_address, to_u16_bytes(self.max_items), 'MainRAM'))
        if read_values['nikita_max'] != self.max_items:
            write_list.append((RAM.nikita_max_ammo_address, to_u16_bytes(self.max_items), 'MainRAM'))
        if read_values['stinger_max'] != self.max_items:
            write_list.append((RAM.stinger_max_ammo_address, to_u16_bytes(self.max_items), 'MainRAM'))
        if read_values['claymore_max'] != self.max_items:
            write_list.append((RAM.claymore_max_ammo_address, to_u16_bytes(self.max_items), 'MainRAM'))
        if read_values['c4_max'] != self.max_items:
            write_list.append((RAM.c4_max_ammo_address, to_u16_bytes(self.max_items), 'MainRAM'))
        if read_values['stun_grenade_max'] != self.max_items:
            write_list.append((RAM.stun_g_max_ammo_address, to_u16_bytes(self.max_items), 'MainRAM'))
        if read_values['chaff_grenade_max'] != self.max_items:
            write_list.append((RAM.chaff_g_max_ammo_address, to_u16_bytes(self.max_items), 'MainRAM'))
        if read_values['psg1_max'] != self.max_items:
            write_list.append((RAM.psg1_max_ammo_address, to_u16_bytes(self.max_items), 'MainRAM'))

        
        if not initial_sync:
            pickup_state_changed = self.handle_item_pickups(read_values, write_list)
            has_state_changed = has_state_changed or pickup_state_changed

        # == HANDLE DEATH == #
        # When entering a new area, the player's stats are copied to another part of RAM
        # Upon death, those values are used to reset the player's stats
        # I use the same technique! Upon death, reset the Client's counts to the values the game saved into the 'on_death' part of RAM
        if (
            not initial_sync
            and read_values['is_game_over']
            and not self.save_state['is_captured']
            and not self.save_state.get('endgame_inventory_locked', False)
        ):
            # A count of 0xFFFF means item is disabled. The save_state should not be updated
            if read_values['cbox_a_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['cbox_a_counter'] = read_values['cbox_a_on_death']
                write_list.append((RAM.cbox_a_count_address, to_u16_bytes(read_values['cbox_a_on_death']), 'MainRAM'))
            if read_values['cbox_b_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['cbox_b_counter'] = read_values['cbox_b_on_death']
                write_list.append((RAM.cbox_b_count_address, to_u16_bytes(read_values['cbox_b_on_death']), 'MainRAM'))
            if read_values['cbox_c_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['cbox_c_counter'] = read_values['cbox_c_on_death']
                write_list.append((RAM.cbox_c_count_address, to_u16_bytes(read_values['cbox_c_on_death']), 'MainRAM'))
            if read_values['night_vision_goggles_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['night_vision_goggles_counter'] = read_values['night_vision_goggles_on_death']
                write_list.append((RAM.nvg_count_address, to_u16_bytes(read_values['night_vision_goggles_on_death']), 'MainRAM'))
            if read_values['thermal_goggles_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['thermal_goggles_counter'] = read_values['thermal_goggles_on_death']
                write_list.append((RAM.therm_g_count_address, to_u16_bytes(read_values['thermal_goggles_on_death']), 'MainRAM'))
            if read_values['gasmask_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['gasmask_counter'] = read_values['gasmask_on_death']
                write_list.append((RAM.gasmask_count_address, to_u16_bytes(read_values['gasmask_on_death']), 'MainRAM'))
            if read_values['body_armor_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['body_armor_counter'] = read_values['body_armor_on_death']
                write_list.append((RAM.b_armor_count_address, to_u16_bytes(read_values['body_armor_on_death']), 'MainRAM'))
            if read_values['camera_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['camera_counter'] = read_values['camera_on_death']
                write_list.append((RAM.camera_count_address, to_u16_bytes(read_values['camera_on_death']), 'MainRAM'))
            if read_values['rations_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['rations_counter'] = read_values['rations_on_death']
                write_list.append((RAM.rations_count_address, to_u16_bytes(read_values['rations_on_death']), 'MainRAM'))
            if read_values['medicine_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['medicine_counter'] = read_values['medicine_on_death']
                write_list.append((RAM.medicine_count_address, to_u16_bytes(read_values['medicine_on_death']), 'MainRAM'))
            if read_values['diazepam_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['diazepam_counter'] = read_values['diazepam_on_death']
                write_list.append((RAM.diazepam_count_address, to_u16_bytes(read_values['diazepam_on_death']), 'MainRAM'))
            if read_values['pal_key_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['pal_key_counter'] = read_values['pal_key_on_death']
                write_list.append((RAM.pal_key_count_address, to_u16_bytes(read_values['pal_key_on_death']), 'MainRAM'))
            if read_values['key_card_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['key_card_counter'] = read_values['key_card_on_death']
                write_list.append((RAM.key_card_count_address, to_u16_bytes(read_values['key_card_on_death']), 'MainRAM'))
            if read_values['mine_detector_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['mine_detector_counter'] = read_values['mine_detector_on_death']
                write_list.append((RAM.mine_d_count_address, to_u16_bytes(read_values['mine_detector_on_death']), 'MainRAM'))
            if read_values['rope_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['rope_counter'] = read_values['rope_on_death']
                write_list.append((RAM.rope_count_address, to_u16_bytes(read_values['rope_on_death']), 'MainRAM'))
            if read_values['handkerchief_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['handkerchief_counter'] = read_values['handkerchief_on_death']
                write_list.append((RAM.handkerchief_count_address, to_u16_bytes(read_values['handkerchief_on_death']), 'MainRAM'))
            if read_values['suppressor_on_death'] != 0xFFFF:
                has_state_changed = True
                self.save_state['suppressor_counter'] = read_values['suppressor_on_death']
                write_list.append((RAM.suppressor_count_address, to_u16_bytes(read_values['suppressor_on_death']), 'MainRAM'))
            if self.save_state['has_socom']:
                has_state_changed = True
                self.save_state['socom_counter'] = read_values['socom_ammo_on_death']
                write_list.append((RAM.socom_ammo_address, to_u16_bytes(read_values['socom_ammo_on_death']), 'MainRAM'))
            if self.save_state['has_famas']:
                has_state_changed = True
                self.save_state['famas_counter'] = read_values['famas_ammo_on_death']
                write_list.append((RAM.famas_ammo_address, to_u16_bytes(read_values['famas_ammo_on_death']), 'MainRAM'))
            if self.save_state['has_grenade']:
                has_state_changed = True
                self.save_state['grenade_counter'] = read_values['grenade_ammo_on_death']
                write_list.append((RAM.grenade_ammo_address, to_u16_bytes(read_values['grenade_ammo_on_death']), 'MainRAM'))
            if self.save_state['has_nikita']:
                has_state_changed = True
                self.save_state['nikita_counter'] = read_values['nikita_ammo_on_death']
                write_list.append((RAM.nikita_ammo_address, to_u16_bytes(read_values['nikita_ammo_on_death']), 'MainRAM'))
            if self.save_state['has_stinger']:
                has_state_changed = True
                self.save_state['stinger_counter'] = read_values['stinger_ammo_on_death']
                write_list.append((RAM.stinger_ammo_address, to_u16_bytes(read_values['stinger_ammo_on_death']), 'MainRAM'))
            if self.save_state['has_claymore']:
                has_state_changed = True
                self.save_state['claymore_counter'] = read_values['claymore_ammo_on_death']
                write_list.append((RAM.claymore_ammo_address, to_u16_bytes(read_values['claymore_ammo_on_death']), 'MainRAM'))
            if self.save_state['has_c4']:
                has_state_changed = True
                self.save_state['c4_counter'] = read_values['c4_ammo_on_death']
                write_list.append((RAM.c4_ammo_address, to_u16_bytes(read_values['c4_ammo_on_death']), 'MainRAM'))
            if self.save_state['has_stun_grenade']:
                has_state_changed = True
                self.save_state['stun_grenade_counter'] = read_values['stun_grenade_on_death']
                write_list.append((RAM.stun_g_ammo_address, to_u16_bytes(read_values['stun_grenade_on_death']), 'MainRAM'))
            if self.save_state['has_chaff_grenade']:
                has_state_changed = True
                self.save_state['chaff_grenade_counter'] = read_values['chaff_grenade_on_death']
                write_list.append((RAM.chaff_g_death_ammo_address, to_u16_bytes(read_values['chaff_grenade_on_death']), 'MainRAM'))
            if self.save_state['has_psg1']:
                has_state_changed = True
                self.save_state['psg1_counter'] = read_values['psg1_ammo_on_death']
                write_list.append((RAM.psg1_ammo_address, to_u16_bytes(read_values['psg1_ammo_on_death']), 'MainRAM'))

        # === SEND LOCATION CHECKS === #
        if len(self.locations_to_send) > 0:
            await ctx.check_locations(self.locations_to_send)
            self.locations_to_send.clear()

        if (
            not self.save_state['is_captured']
            and not self.save_state.get('endgame_inventory_locked', False)
            and self.release_pending_missable_items(write_list)
        ):
            has_state_changed = True

        # === HANDLE RECEIVED ITEMS === #
        # When receiving an item from the server, update the client's count for that item and write it to the game's RAM in both the current and 'on death' locations.
        # not writing it to the 'on death' section means received items can be permanently lost if the player receives an item and then dies before moving to a new area
        # The amount of items rewarded depends on the item received. I tried to be generous to prevent softlocking!
        # Receiving a certain number of 'Dogtag' or 'Boss Dogtag' items can trigger a victory.
        # TODO MGS: Add the option to vary the item counts received?
        if (
            not self.save_state['is_captured']
            and self.save_state['received_item_counter'] < len(ctx.items_received)
        ):
            has_state_changed = True
            start_index = self.save_state['received_item_counter']
            for i in range(start_index, len(ctx.items_received)):
                item = ctx.items_received[i]
                local_item_name = ctx.item_names.lookup_in_game(code=item.item, game_name='MGS: Masala Garden Salad')
                self.save_state['received_item_counter'] += 1

                # Liquid removes Snake's inventory after REX. Keep processing
                # goal-only items so Boss Blitz/Dogtag goals and Victory still
                # work, but do not write any inventory-bearing AP item back into
                # the game during the final fight and Escape Route.
                if (
                    self.save_state.get('endgame_inventory_locked', False)
                    and local_item_name not in {'Dogtag', 'Boss Dogtag', 'Victory'}
                ):
                    self.save_state.setdefault('pending_endgame_items', []).append(local_item_name)
                    logger.info(
                        f'[MGS: Masala Garden Salad] Endgame inventory lock: '
                        f'{local_item_name} was received but not granted in-game.'
                    )
                    continue

                if self.hold_missable_item(local_item_name):
                    self.save_state.setdefault('pending_missable_items', []).append(local_item_name)
                    logger.info(f'[MGS: Masala Garden Salad] Holding AP item until its location is checked: {local_item_name}')
                    continue

                match local_item_name:
                    case 'Cardboard Box A' | 'Cardboard Box B' | 'Cardboard Box C' | 'Night Vision Goggles' | 'Thermal Goggles' | 'Gas Mask' | 'Body Armor' | 'Camera':
                        self.give_missable_item(local_item_name, write_list)
                    case 'Ration':
                        self.save_state['rations_counter'] = min(0xFFFF, self.save_state['rations_counter'] + 2)
                        write_list.append((RAM.rations_count_address, to_u16_bytes(self.save_state['rations_counter']), 'MainRAM'))
                        write_list.append((RAM.rations_death_count_address, to_u16_bytes(self.save_state['rations_counter']), 'MainRAM'))
                    case 'Medicine':
                        self.save_state['medicine_counter'] = min(0xFFFF, self.save_state['medicine_counter'] + 3)
                        write_list.append((RAM.medicine_count_address, to_u16_bytes(self.save_state['medicine_counter']), 'MainRAM'))
                        write_list.append((RAM.medicine_death_count_address, to_u16_bytes(self.save_state['medicine_counter']), 'MainRAM'))
                    case 'Diazepam':
                        self.save_state['diazepam_counter'] = min(0xFFFF, self.save_state['diazepam_counter'] + 3)
                        write_list.append((RAM.diazepam_count_address, to_u16_bytes(self.save_state['diazepam_counter']), 'MainRAM'))
                        write_list.append((RAM.diazepam_death_count_address, to_u16_bytes(self.save_state['diazepam_counter']), 'MainRAM'))
                    case 'Pal Key':
                        self.save_state['pal_key_counter'] = 1
                        write_list.append((RAM.pal_key_count_address, to_u16_bytes(self.save_state['pal_key_counter']), 'MainRAM'))
                        write_list.append((RAM.pal_key_death_count_address, to_u16_bytes(self.save_state['pal_key_counter']), 'MainRAM'))
                    case 'Progressive Key Card':
                        self.save_state['key_card_counter'] = min(0xFFFF, self.save_state['key_card_counter'] + 1)
                        write_list.append((RAM.key_card_count_address, to_u16_bytes(self.save_state['key_card_counter']), 'MainRAM'))
                        write_list.append((RAM.key_card_death_count_address, to_u16_bytes(self.save_state['key_card_counter']), 'MainRAM'))
                    case 'Mine Detector' | 'Rope':
                        self.give_missable_item(local_item_name, write_list)
                    case 'Handkerchief':
                        self.save_state['handkerchief_counter'] = 1
                        write_list.append((RAM.handkerchief_count_address, to_u16_bytes(self.save_state['handkerchief_counter']), 'MainRAM'))
                        write_list.append((RAM.handkerchief_death_count_address, to_u16_bytes(self.save_state['handkerchief_counter']), 'MainRAM'))
                    case 'Suppressor':
                        self.give_missable_item(local_item_name, write_list)
                    case 'SOCOM':
                        self.save_state['has_socom'] = True
                        self.save_state['socom_counter'] = min(0xFFFF, self.save_state['socom_counter'] + 24)
                        write_list.append((RAM.socom_ammo_address, to_u16_bytes(self.save_state['socom_counter']), 'MainRAM'))
                        write_list.append((RAM.socom_death_ammo_address, to_u16_bytes(self.save_state['socom_counter']), 'MainRAM'))
                    case 'FA-MAS':
                        self.save_state['has_famas'] = True
                        self.save_state['famas_counter'] = min(0xFFFF, self.save_state['famas_counter'] + 35)
                        write_list.append((RAM.famas_ammo_address, to_u16_bytes(self.save_state['famas_counter']), 'MainRAM'))
                        write_list.append((RAM.famas_death_ammo_address, to_u16_bytes(self.save_state['famas_counter']), 'MainRAM'))
                    case 'Grenade':
                        self.save_state['has_grenade'] = True
                        self.save_state['grenade_counter'] = min(0xFFFF, self.save_state['grenade_counter'] + 3)
                        write_list.append((RAM.grenade_ammo_address, to_u16_bytes(self.save_state['grenade_counter']), 'MainRAM'))
                        write_list.append((RAM.grenade_death_ammo_address, to_u16_bytes(self.save_state['grenade_counter']), 'MainRAM'))
                    case 'Nikita':
                        self.save_state['has_nikita'] = True
                        self.save_state['nikita_counter'] = min(0xFFFF, self.save_state['nikita_counter'] + 10)
                        write_list.append((RAM.nikita_ammo_address, to_u16_bytes(self.save_state['nikita_counter']), 'MainRAM'))
                        write_list.append((RAM.nikita_death_ammo_address, to_u16_bytes(self.save_state['nikita_counter']), 'MainRAM'))
                    case 'Stinger':
                        self.save_state['has_stinger'] = True
                        self.save_state['stinger_counter'] = min(0xFFFF, self.save_state['stinger_counter'] + 10)
                        write_list.append((RAM.stinger_ammo_address, to_u16_bytes(self.save_state['stinger_counter']), 'MainRAM'))
                        write_list.append((RAM.stinger_death_ammo_address, to_u16_bytes(self.save_state['stinger_counter']), 'MainRAM'))
                    case 'Claymore':
                        self.save_state['has_claymore'] = True
                        self.save_state['claymore_counter'] = min(0xFFFF, self.save_state['claymore_counter'] + 10)
                        write_list.append((RAM.claymore_ammo_address, to_u16_bytes(self.save_state['claymore_counter']), 'MainRAM'))
                        write_list.append((RAM.claymore_death_ammo_address, to_u16_bytes(self.save_state['claymore_counter']), 'MainRAM'))
                    case 'C4':
                        self.save_state['has_c4'] = True
                        self.save_state['c4_counter'] = min(0xFFFF, self.save_state['c4_counter'] + 10)
                        write_list.append((RAM.c4_ammo_address, to_u16_bytes(self.save_state['c4_counter']), 'MainRAM'))
                        write_list.append((RAM.c4_death_ammo_address, to_u16_bytes(self.save_state['c4_counter']), 'MainRAM'))
                    case 'Stun Grenade':
                        self.save_state['has_stun_grenade'] = True
                        self.save_state['stun_grenade_counter'] = min(0xFFFF, self.save_state['stun_grenade_counter'] + 3)
                        write_list.append((RAM.stun_g_ammo_address, to_u16_bytes(self.save_state['stun_grenade_counter']), 'MainRAM'))
                        write_list.append((RAM.stun_g_death_ammo_address, to_u16_bytes(self.save_state['stun_grenade_counter']), 'MainRAM'))
                    case 'Chaff Grenade':
                        self.save_state['has_chaff_grenade'] = True
                        self.save_state['chaff_grenade_counter'] = min(0xFFFF, self.save_state['chaff_grenade_counter'] + 5)
                        write_list.append((RAM.chaff_g_ammo_address, to_u16_bytes(self.save_state['chaff_grenade_counter']), 'MainRAM'))
                        write_list.append((RAM.chaff_g_death_ammo_address, to_u16_bytes(self.save_state['chaff_grenade_counter']), 'MainRAM'))
                    case 'PSG-1':
                        self.save_state['has_psg1'] = True
                        self.save_state['psg1_counter'] = min(0xFFFF, self.save_state['psg1_counter'] + 12)
                        write_list.append((RAM.psg1_ammo_address, to_u16_bytes(self.save_state['psg1_counter']), 'MainRAM'))
                        write_list.append((RAM.psg1_death_ammo_address, to_u16_bytes(self.save_state['psg1_counter']), 'MainRAM'))
                    case 'Dogtag':
                        self.save_state['dogtag_counter'] += 1
                        if self.save_state['dogtag_counter'] == self.dogtag_goal and self.run_goal == 2: # option 2 is dogtag collection
                            await ctx.send_msgs([{
                                "cmd": "StatusUpdate",
                                "status": ClientStatus.CLIENT_GOAL
                            }])
                            ctx.finished_game = True
                    case 'Boss Dogtag':
                        self.save_state['dogtag_counter'] += 1
                        if self.save_state['dogtag_counter'] == self.boss_goal and self.run_goal == 1: # option 1 is boss blitz
                            await ctx.send_msgs([{
                                "cmd": "StatusUpdate",
                                "status": ClientStatus.CLIENT_GOAL
                            }])
                            ctx.finished_game = True
                    case 'Victory':
                        # Basically force goal to send, since it was refusing sometimes
                        if self.run_goal == 0 and not ctx.finished_game: # option 0 is game completion
                            await ctx.send_msgs([{
                                "cmd": "StatusUpdate",
                                "status": ClientStatus.CLIENT_GOAL
                            }])
                            ctx.finished_game = True
                    case _:
                        logger.debug(f'[Metal Gear Solid - DEBUG] No item handler for item named \'{local_item_name}\'')

        # === WRITE TO RAM === #
        if len(write_list) > 0:
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
            write_list.clear()
        
        # === SAVE CURRENT STATE TO JSON === #
        if has_state_changed:
            with open(self.save_file, 'w') as save:
                json.dump(self.save_state, save)
            has_state_changed = False
