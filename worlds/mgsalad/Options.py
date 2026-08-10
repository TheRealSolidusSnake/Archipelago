from dataclasses import dataclass

from Options import Range, Choice, PerGameCommonOptions

class LogicDifficulty(Choice):
    """Determines which progression items are required by the world's access logic.
    This strictly just affects what is considered "in logic" with certain loadouts
    you may have at any given time. Universal Tracker is your friend.

    Easy: C4 or the Stinger can be used to destroy any Armory blast wall, including the wall leading to Ocelot.
    The Mine Detector is required to cross the minefield to reach the tank fight. 
    The M1 Tank can be defeated with Grenades or the Stinger. 
    Medicine is required to access the Communication Towers.

    Crossing the minefield without Mine Detector and accessing Comm. Towers without
    Medicine will be considered out of logic. 

    Hard: C4 is required to destroy every Armory blast wall, including the wall leading to Ocelot.
    The Mine Detector is not required to cross the minefield.
    You can be expected to defeat the M1 Tank with just a single pack of grenades. (3 ammo)
    Medicine is not required to access the Communication Towers, so if you didn't save
    Meryl you can be expected to play with a Cold for the rest of the game.

    You can still end up getting the Stinger early and use it physically, but it will not satisfy
    Hard logic for any Armory blast wall. It can still help with the Tank Fight.

    Default: Easy
    """

    display_name = 'Logic Difficulty'
    option_easy = 0
    option_hard = 1
    default = 0

class RunGoal(Choice):
    """Choose the victory condition for this world.
    Game Completion: The goal will be to defeat Liquid and escape Shadow Moses Island.
    Boss Blitz: The goal will be to defeat a specific number of Bosses.
    Dogtag Collection: The goal will be to collect a specific number of 'Dogtag' items which can be awarded for any location check.
    Default: Game Completion
    """
    display_name = 'Goal'
    option_game_completion = 0
    option_boss_blitz = 1
    option_dogtag_collection = 2
    default = 0

class DogtagGoal(Range):
    """Choose Dogtag Target.
    If the goal of the run is Dogtag Collection, this will be the number of 'Dogtag' items required to win.
    Default value: 30
    """

    display_name = 'Dogtags Required'
    range_start = 1
    range_end = 50
    default = 30

class ExtraDogtags(Range):
    """Assign extra Dogtags to be added to item pool.
    If the goal of the run is Dogtag Collection, this will be the number of additional 'Dogtag' items added to the pool.
    It's recommended to have a few to prevent softlocking.
    Default value: 10
    """

    display_name = 'Additional Dogtags'
    range_start = 2
    range_end = 50
    default = 10

class BossGoal(Range):
    """Choose Boss Target.
    If the goal of the run is Boss Blitz, this will be the number of Bosses required to beat in order to win.
    There are 14 Bosses in total: Heavily Armed Genome Soldiers, Revolver Ocelot, M1 Tank, Gray Fox, Psycho Mantis, Sniper Wolf I, Black-outfitted Genome Soldiers I, A Hind D?, 
    Stealth Camouflaged Genome Soldiers, Sniper Wolf II, Black-outfitted Genome Soldiers II, Vulcan Raven, Metal Gear REX, and Liquid Snake.
    Default Value: 14
    """

    display_name = 'Bosses Required'
    range_start = 1
    range_end = 14
    default = 14

@dataclass
class MGSOptions(PerGameCommonOptions):
    logic_difficulty: LogicDifficulty
    run_goal: RunGoal
    dogtag_goal: DogtagGoal
    extra_dogtags: ExtraDogtags
    boss_goal: BossGoal
