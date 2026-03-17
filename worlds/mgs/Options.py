from dataclasses import dataclass

from Options import Range, Choice, PerGameCommonOptions

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
    run_goal: RunGoal
    dogtag_goal: DogtagGoal
    extra_dogtags: ExtraDogtags
    boss_goal: BossGoal