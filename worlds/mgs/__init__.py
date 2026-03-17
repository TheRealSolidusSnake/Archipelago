import settings
import typing
from . import Options
from . import Items
from . import Locations
from . import Regions
from . import Rules
from . import Client # Unused, but required to register with BizHawkClient
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, ItemClassification

class MGSWorld(World):
    """Metal Gear Solid: Stealth Espionage Action"""
    game = 'Metal Gear Solid'
    options_dataclass = Options.MGSOptions 
    options: Options.MGSOptions  # type: ignore # typing hints for option results
    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location
    base_id = Items.base_mgs_item_id

    # The following two dicts are required for the generation to know which items exist.
    item_name_to_id = Items.item_name_to_id_table
    location_name_to_id = Regions.build_location_name_to_id_table()

    def __init__(self, multiworld: MultiWorld, player: int):
        self.item_pool: typing.List[Items.MGSItems] = []
        self.short_location_name_to_full: dict[str, str] = {}
        super(MGSWorld, self).__init__(multiworld, player)

    def get_full_location_name(self, short_name: str) -> str:
        return self.short_location_name_to_full.get(short_name, short_name)

    def generate_early(self) -> None:
        # read player options to world instance
        self.run_goal = self.options.run_goal.value
        # option_game_completion = 0
        # option_boss_blitz = 1
        # option_dogtag_collection = 2
        self.boss_goal = self.options.boss_goal.value
        self.dogtag_goal = self.options.dogtag_goal.value
        self.dogtag_extra = self.options.extra_dogtags.value

    # Helper functions for creating different classes of items
    def create_item(self, name: str) -> Items.MGSItems:
        item_id = Items.item_name_to_id_table[name]
        classification = ItemClassification.progression

        item = Items.MGSItems(name, classification, item_id, self.player)
        return item
    
    def create_item_useful(self, name: str) -> Items.MGSItems:
        item_id = Items.item_name_to_id_table[name]
        classificaton = ItemClassification.useful

        item = Items.MGSItems(name, classificaton, item_id, self.player)
        return item
    
    def create_item_filler(self, name: str) -> Items.MGSItems:
        item_id = Items.item_name_to_id_table[name]
        classificaton = ItemClassification.filler

        item = Items.MGSItems(name, classificaton, item_id, self.player)
        return item
    
    def create_event(self, name: str) -> Items.MGSItems:
        item_id = None
        classification = ItemClassification.progression

        item = Items.MGSItems(name, classification, item_id, self.player)
        return item
    
    def create_regions(self) -> None:
        Regions.create_regions(self)
    
    def set_rules(self) -> None:
        Rules.set_rules(self)
    
    def create_items(self) -> None:
        # Start off by creating all the items that absolutely need to be in the run
        if self.run_goal == 2: # dog tag collection
            for _ in range(self.dogtag_goal + self.dogtag_extra):
                self.item_pool.append(self.create_item('Dogtag'))
        self.item_pool.append(self.create_item('Key Card'))
        self.item_pool.append(self.create_item('Key Card'))
        self.item_pool.append(self.create_item('Key Card'))
        self.item_pool.append(self.create_item('Key Card'))
        self.item_pool.append(self.create_item('Key Card'))
        self.item_pool.append(self.create_item('Key Card'))
        self.item_pool.append(self.create_item('Key Card'))
        self.item_pool.append(self.create_item('SOCOM'))
        self.item_pool.append(self.create_item_useful('Cardboard Box A'))
        self.item_pool.append(self.create_item_useful('Cardboard Box B'))
        self.item_pool.append(self.create_item_useful('Cardboard Box C'))
        self.item_pool.append(self.create_item_useful('Night Vision Goggles'))
        self.item_pool.append(self.create_item_useful('Thermal Goggles'))
        self.item_pool.append(self.create_item_useful('Gas Mask'))
        self.item_pool.append(self.create_item_useful('Body Armor'))
        self.item_pool.append(self.create_item('Pal Key'))
        self.item_pool.append(self.create_item('Mine Detector'))
        self.item_pool.append(self.create_item('Rope'))
        self.item_pool.append(self.create_item_useful('Handkerchief'))
        self.item_pool.append(self.create_item_useful('Suppressor'))
        self.item_pool.append(self.create_item('Nikita'))
        self.item_pool.append(self.create_item('Stinger'))
        self.item_pool.append(self.create_item('Stinger'))
        self.item_pool.append(self.create_item('C4'))
        self.item_pool.append(self.create_item('Chaff Grenade'))
        self.item_pool.append(self.create_item('Grenade'))
        self.item_pool.append(self.create_item('PSG-1'))
        self.item_pool.append(self.create_item('PSG-1'))
        self.item_pool.append(self.create_item('Medicine'))
        # Calculate how many more items need to be added to the item_pool
        if self.run_goal == 1: # Boss Blits, remove 14 filler items for Boss Dogtag items created in Rules.py
            filler_count = len(self.multiworld.get_unfilled_locations(self.player)) - len(self.item_pool) - 15 - 2 # Two events need to be subtracted as well!
        else:
            filler_count = len(self.multiworld.get_unfilled_locations(self.player)) - len(self.item_pool) - 1 - 2
        # Fill the item pool with additional items, weighted towards SOCOM, FA-MAS, and Rations, then Stinger, PSG-1, and Chaff Grenades, then everything else.
        for _ in range(filler_count):
            match self.random.randint(0, 2):
                case 0 | 1:
                    match self.random.randint(0,2):
                        case 0:
                            self.item_pool.append(self.create_item_useful('SOCOM'))
                        case 1:
                            self.item_pool.append(self.create_item_useful('FA-MAS'))
                        case 2:
                            self.item_pool.append(self.create_item_useful('Ration'))
                case 2:
                    match self.random.randint(0,11):
                        case 0 | 1:
                            self.item_pool.append(self.create_item_useful('Stinger'))
                        case 2 | 3:
                            self.item_pool.append(self.create_item_useful('PSG-1'))
                        case 4 | 5:
                            self.item_pool.append(self.create_item_useful('Chaff Grenade'))
                        case 6:
                            self.item_pool.append(self.create_item_filler('Stun Grenade'))
                        case 7:
                            self.item_pool.append(self.create_item_filler('Diazepam'))
                        case 8:
                            self.item_pool.append(self.create_item_useful('C4'))
                        case 9:
                            self.item_pool.append(self.create_item_filler('Grenade'))
                        case 10:
                            self.item_pool.append(self.create_item_useful('Nikita'))
                        case 11:
                            self.item_pool.append(self.create_item_filler('Claymore'))
                    
                    
        self.multiworld.itempool += self.item_pool

    def fill_slot_data(self) -> typing.Mapping[str, settings.Any]:
        return {
            'run_goal': self.options.run_goal.value,
            'boss_goal': self.options.boss_goal.value,
            'dogtag_goal': self.options.dogtag_goal.value,
        }

# def run_client(*args):
#     import CommonClient
#     launch_subprocess(CommonClient.run_as_textclient, name="TextClient", args=args)

# NOTE: Probably not needed but this is how to add a component to the Archipelago GUI
# components.append(
#     Component('MGS Client', func=run_client, component_type=Type.CLIENT, description='This is a test.')
# )