from dataclasses import dataclass
from typing import List, Dict

# Removing this for now because keeping up an enemy data class gets complicated with !blue
# @dataclass
# class Enemy:
#     '''Enemy Class
#     This is a simplified enemy class that is not as detailed as a bestiary
#     entry would be. This is due, in part, to enemies having different levels
#     and stats and skills depending on where they are found.'''
#     def __init__(
#         self,
#         name: str,
#     ):
#         self.name = name

@dataclass
class Mix:
    '''Mix Class'''
    def __init__(
        self,
        name: str,
        recipe_name_snes: str,
        recipe_name_gba: str,
        category: str,
        combos: List[str],
        effect: str,
        tags: List[str],
        favorite: bool,
    ):
        self.name = name
        self.recipe_name_snes = recipe_name_snes
        self.recipe_name_gba = recipe_name_gba
        self.category = category
        self.combos = [*combos]
        self.effect = effect
        self.tags = [*tags]
        self.favorite = favorite

@dataclass
class BlueMagic:
    '''Blue Magic Class'''
    def __init__(
        self,
        name: str,
        alternate_name: str,
        mp_cost: int,
        spell_power: int,
        # learned_from: list[Enemy],
        # earliest_acquisition: tuple[Enemy, str],
        # best_source: list[tuple[Enemy, str]],
        learned_from: List[str|Dict[str, List[str]]],
        earliest_acquisition: Dict[str, str],
        best_source: List[Dict[str, str]],
        description: str,
        note: str,
        warning: str,
        fiesta_recommended: bool,
    ):
        self.name = name
        self.alternate_name = alternate_name
        self.mp_cost = mp_cost
        self.spell_power = spell_power
        self.learned_from = [*learned_from]
        self.earliest_acquisition = {**earliest_acquisition}
        self.best_source = [*best_source]
        self.description = description
        self.note = note
        self.warning = warning
        self.fiesta_recommended = fiesta_recommended
        
    # def __dict__(self, pretty_keys: bool = False) -> Dict:
    #     if pretty_keys:
    #         return {
    #             'Name': self.name,
    #             'Alternate Name': self.alternate_name,
    #             'MP Cost': self.mp_cost,
    #             'Spell Power': self.spell_power,
    #             'Learned From': [*self.learned_from],
    #             'Earliest Acquisition': {**self.earliest_acquisition},
    #             'Best Source': [*self.best_source],
    #             'Description': self.description,
    #             'FJF Recommended': self.fiesta_recommended,
    #         }
    #     else:
    #         return {
    #             'name': self.name,
    #             'alternate_name': self.alternate_name,
    #             'mp_cost': self.mp_cost,
    #             'spell_power': self.spell_power,
    #             'learned_from': [*self.learned_from],
    #             'earliest_acquisition': {**self.earliest_acquisition},
    #             'best_source': [*self.best_source],
    #             'description': self.description,
    #             'fiesta_recommended': self.fiesta_recommended,
    #         }
    
@dataclass
class Boss:
    '''Boss Class'''
    def __init__(
        self,
        name: str,
        hint_section: str,
    ):
        self.name = name
        self.hint_section = hint_section

@dataclass
class Hint:
    '''Hint Class'''
    def __init__(
        self,
        name: str,
        hint_text: List[str],
        job_code_string: str = None,
    ):
        self.name = name
        self.hint_text = [*hint_text]
        self.job_code_string = job_code_string

@dataclass
class HintSection:
    '''Hint Section Class'''
    def __init__(
        self,
        name: str,
        hints: List[Hint],
        bosses: List[Boss],
        world: int,
    ):
        self.name = name
        self.hints = [*hints]
        self.bosses = [*bosses]
        self.world = world

@dataclass
class FF5Job:
    '''FF5 Job Class'''
    def __init__(
        self,
        name: str,
        code: str,
        crystal: str,
        tags: List[str] = [],
    ):
        self.name = name
        self.code = code
        self.crystal = crystal
        self.tags = [*tags]
