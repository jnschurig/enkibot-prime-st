import subprocess
from pathlib import Path
import shutil
import yaml
import json

from enkibot_dataclasses import BlueMagic, Boss, Hint, FF5Job, Mix
from typing import List, Dict

class_codes = {
    'Bard': {'code': 'BRD', 'crystal': 'FIRE'},
    'Beastmaster': {'code': 'BST', 'crystal': 'FIRE'},
    'Berserker': {'code': 'BER', 'crystal': 'WATER'},
    'Black-Mage': {'code': 'BLM', 'crystal': 'WIND'},
    'Blue-Mage': {'code': 'BLU', 'crystal': 'WIND'},
    'Cannoneer': {'code': 'CAN', 'crystal': 'ADVANCE'},
    'Chemist': {'code': 'CHM', 'crystal': 'EARTH'},
    'Dancer': {'code': 'DNC', 'crystal': 'EARTH'},
    'Dragoon': {'code': 'DRG', 'crystal': 'EARTH'},
    'Freelancer': {'code': 'FRE', 'crystal': 'INNATE'},
    'Geomancer': {'code': 'GEO', 'crystal': 'FIRE'},
    'Gladiator': {'code': 'GLD', 'crystal': 'ADVANCE'},
    'Knight': {'code': 'KGT', 'crystal': 'WIND'},
    'Mime': {'code': 'MIM', 'crystal': 'WATER'},
    'Monk': {'code': 'MNK', 'crystal': 'WIND'},
    'Mystic-Knight': {'code': 'MYS', 'crystal': 'WATER'},
    'Ninja': {'code': 'NIN', 'crystal': 'FIRE'},
    'Oracle': {'code': 'ORC', 'crystal': 'ADVANCE'},
    'Ranger': {'code': 'RAN', 'crystal': 'FIRE'},
    'Red-Mage': {'code': 'RDM', 'crystal': 'WATER'},
    'Samurai': {'code': 'SAM', 'crystal': 'EARTH'},
    'Summoner': {'code': 'SUM', 'crystal': 'WATER'},
    'Thief': {'code': 'THF', 'crystal': 'WIND'},
    'Time-Mage': {'code': 'TIM', 'crystal': 'WATER'},
    'White-Mage': {'code': 'WHM', 'crystal': 'WIND'},
}

job_lookup = {
    'Bard'          : FF5Job(name='Bard'         , code='BRD', crystal='FIRE'   ),
    'Beastmaster'   : FF5Job(name='Beastmaster'  , code='BST', crystal='FIRE'   ),
    'Berserker'     : FF5Job(name='Berserker'    , code='BER', crystal='WATER'  ),
    'Black-Mage'    : FF5Job(name='Black-Mage'   , code='BLM', crystal='WIND'   ),
    'Blue-Mage'     : FF5Job(name='Blue-Mage'    , code='BLU', crystal='WIND'   ),
    'Cannoneer'     : FF5Job(name='Cannoneer'    , code='CAN', crystal='ADVANCE'),
    'Chemist'       : FF5Job(name='Chemist'      , code='CHM', crystal='EARTH'  ),
    'Dancer'        : FF5Job(name='Dancer'       , code='DNC', crystal='EARTH'  ),
    'Dragoon'       : FF5Job(name='Dragoon'      , code='DRG', crystal='EARTH'  ),
    'Freelancer'    : FF5Job(name='Freelancer'   , code='FRE', crystal='INNATE' ),
    'Geomancer'     : FF5Job(name='Geomancer'    , code='GEO', crystal='FIRE'   ),
    'Gladiator'     : FF5Job(name='Gladiator'    , code='GLD', crystal='ADVANCE'),
    'Knight'        : FF5Job(name='Knight'       , code='KGT', crystal='WIND'   ),
    'Mime'          : FF5Job(name='Mime'         , code='MIM', crystal='WATER'  ),
    'Monk'          : FF5Job(name='Monk'         , code='MNK', crystal='WIND'   ),
    'Mystic-Knight' : FF5Job(name='Mystic-Knight', code='MYS', crystal='WATER'  ),
    'Ninja'         : FF5Job(name='Ninja'        , code='NIN', crystal='FIRE'   ),
    'Oracle'        : FF5Job(name='Oracle'       , code='ORC', crystal='ADVANCE'),
    'Ranger'        : FF5Job(name='Ranger'       , code='RAN', crystal='FIRE'   ),
    'Red-Mage'      : FF5Job(name='Red-Mage'     , code='RDM', crystal='WATER'  ),
    'Samurai'       : FF5Job(name='Samurai'      , code='SAM', crystal='EARTH'  ),
    'Summoner'      : FF5Job(name='Summoner'     , code='SUM', crystal='WATER'  ),
    'Thief'         : FF5Job(name='Thief'        , code='THF', crystal='WIND'   ),
    'Time-Mage'     : FF5Job(name='Time-Mage'    , code='TIM', crystal='WATER'  ),
    'White-Mage'    : FF5Job(name='White-Mage'   , code='WHM', crystal='WIND'   ),
}

unknown_options = [
    'UNKNOWN WIND',
    'UNKNOWN WATER',
    'UNKNOWN FIRE',
    'UNKNOWN EARTH',
    'UNKNOWN ADVANCE',
]

dump_modes = [
    'markdown',
    'md',
    'yaml',
    'yml',
    'json',
    'text',
]

valid_display_styles = [
    'emoji',
    'text',
]

status_icon_lookup = {
    'Death': '💀',
    'Break': '🗿',
    'Mute': '🔇',
    'Not Heavy': '🪶',
    'Sleep': '💤',
    'Slow': '⏳',
    'Berserk': '😡',
    'Confuse': '💫',
    'Blind': '🕶️',
    'Stop': '🛑',
    'Paralyze': '♿',
    'Toad': '🐸',
    # 'Mini': '🐭', # 🐛
}

element_icon_lookup = {
    'Ice': '❄️',
    'Fire': '🔥',
    'Lightning': '⚡',
    'Water': '💧',
    'Wind': '🍃',
    'Earth': '⛰️',
    'Poison': '🫧', # ☠️
    'Holy': '✨',
    'All': '🌈',
    'Random': '🎲',
}

enemy_type_icon_lookup = {
    'Heavy': '🚛',
    'Humanoid': '👤', # 🧑🚶
    'Undead': '🧟',
    'Dragon': '🐲',
    'Magic Beast': '🦄',
    'Desert': '🌵',
}

mix_category_colors = {
    'OFFENSE': 'blue',
    'HEALING': 'green',
    'SUPPORT': 'orange',
    'STATUS': 'violet',
}

class JobException(Exception):
    pass

class NodeException(Exception):
    pass

class DumpModeException(Exception):
    pass

class DisplayStyleException(Exception):
    pass

class Enkibot:
    def __init__(
        self,
        jobs: str|list[str] = None,
        debug: bool = False,
        display_style: str = 'text',
    ) -> None:
        self.debug = debug

        self.hints_path = Path("Enkibot")
        self.hints_repo_url = "https://github.com/Kyrosiris/Enkibot/"
        self._hints_raw = dict()
        self.hints = list()
        self.hint_nodes = list()
        self.hint_titles = list()

        self.jobs = list()
        self.tags = list()
        
        self.display_style = str(None)

        self.boss_root_path = Path("resources", "data", "boss_detail")
        self.bosses = list()
        self.bosses_detail = list()
        self.boss_sources = list()

        self.blue_root_path = Path("resources", "data", "blue_magic")
        self.blue_spell_detail = list()
        self.blue_spells = list()
        self.blue_sources = dict()
        self.blue_notes = dict()
        
        self.mix_root_path = Path("resources", "data", "mix")
        self.mixes = list()
        self.mix_detail = list()
        self.mix_categories = list()

        self.toggle_debug(debug=debug)
        if debug:
            jobs = list(class_codes.keys())

        self.load_boss_data(display_style=display_style)

        if not self.hints_path.is_dir():
            self.refresh_hint_data()

        self.parse_hint_data()

        if jobs is not None:
            self.set_jobs(jobs=jobs)
            self.compile_hints()

        self.load_blue_data()
        self.load_mix_data()
    
    def toggle_debug(self, debug: bool = None) -> bool:
        """
        Change the app debug setting. This method can set the current debug setting
        to a specific true/false setting by passing in a value, or the existing
        state can be toggled without needing to know the current state by leaving
        empty or passing in None.

        Args:
            debug (bool): If true/false, will set the current state to passed in value.
                          If empty or None, will toggle current state to the opposite.

        Returns:
            boolean: The current debug state after being changed.
        """
        if debug is None:
            debug = not self.debug

        self.debug = debug

        if debug:
            debug_jobs = list(class_codes.keys())
            self.set_jobs(debug_jobs)

        return self.debug

    def refresh_hint_data(self):
        """
        This method erase any existing hint data and re-obtain from source.
        """
        if self.hints_path.is_dir():
            shutil.rmtree(self.hints_path)

        self._download_repo()

    def _download_repo(self):
        """
        This method will clone the original enkibot prime code for the main purpose
        of having the hint data available.
        """
        subprocess.run(["git", "clone", "--depth", "1", self.hints_repo_url])
        
    def _resolve_job_name(self, job_name:str) -> List[str]:
        """
        A method to resolve any input FF5 job or unknown job option and return all associated actual jobs.

        Args:
            job_name (str): The name of the FF5 job class or unknown option to resolve to full name.

        Returns:
            list: A list of all matched jobs. This will often be a list of one item.

        Raises:
            JobException: If any input job_name is not a valid job or unknown option.
        """
        if job_name not in unknown_options and job_name not in class_codes.keys():
            raise JobException(
                f"Job name '{job_name}' not in list of valid options\nUnknown: {unknown_options} \nJobs: {list(class_codes.keys())}"
            )
        
        if job_name.startswith('UNKNOWN'):
            crystal = job_name.replace('UNKNOWN ', '')
            
            resolved_jobs = [
                n
                for n in class_codes.keys()
                if class_codes[n]['crystal'] == crystal
            ]
        else:
            resolved_jobs = [job_name]
        
        return resolved_jobs

    def set_jobs(self, jobs: str|List[str]) -> list[str]:
        # TODO: Implement job dataclass objects instead of strings.
        """
        A method which will take a job or unknown option or a list thereof and return a resolved
        list of all jobs.

        Args:
            job_name (str|List[str]): The name of the FF5 job class or unknown option to resolve to full name.

        Returns:
            list: A list of all resolved jobs.

        Raises:
            JobException: If any input job_name is not a valid job or unknown option.
        """
        if type(jobs) is str:
            jobs = [jobs]
        resolved_jobs = []
        for job in jobs:
            resolved_jobs += self._resolve_job_name(job)
            
        valid_jobs = list(class_codes.keys())
        # Final check that ALL the jobs given are in the class list.
        all_jobs_valid = all(n in valid_jobs for n in resolved_jobs)
        if not all_jobs_valid:
            raise JobException(
                f"Invalid Job input detected. Check input Jobs. \nInput: {jobs} \nValid Jobs: {valid_jobs}"
            )
            
        self.job_codes = [
            class_codes[n]['code']
            for n in resolved_jobs
        ]

        self.jobs = [*resolved_jobs]
        self.set_tags()
        self.compile_hints()
        return resolved_jobs

    def set_tags(self) -> List[str]:
        """
        A method to parse the job tags and set tags for each job

        Returns:
            list: A list of all matched jobs. This will often be a list of one item.
        """
        jobs_path = Path(self.hints_path, "data", "jobs.yaml")
        with jobs_path.open("r") as f:
            jobs_yml = yaml.safe_load(f)

        self.valid_jobs = list(jobs_yml["Jobs"].keys())
        tags = list()

        for job in self.jobs:
            for tag in jobs_yml["Jobs"][job]:
                if tag not in tags:
                    tags.append(tag)

        self.tags = [*tags]

        return tags

    def parse_hint_data(self) -> Dict[str,str]:
        # TODO: Implement hint and hint_section dataclass objects. These things are actually kind of complicated.
        """
        A method to load hint data from files and return as a dictionary with node titles as keys
        and the hint body text as the value.

        Returns:
            Dict: A dictionary containing raw hint data.
        """
        data_path = Path(self.hints_path, "data")
        node_root = Path(data_path, "nodes.yaml")
        with node_root.open("r") as f:
            nodes_yml = yaml.safe_load(f)

        self.hint_nodes = nodes_yml["Manifest"]

        hints_raw = {}
        for node in self.hint_nodes:
            node_path = Path(data_path, "nodes", f"{node}.yaml")
            with node_path.open("r") as f:
                hints_raw[node] = yaml.safe_load(f)

        self._hints_raw = {**hints_raw}

        return hints_raw

    def compile_hints(
        self,
        nodes: str|List[str] = None,
    ) -> List[Dict[str, str]]:
        """
        A method to compile hint data based on specific jobs set in the object and job tags.
        Each hint will contain information most relevant to jobs set in the class.

        Args:
            nodes (str|List[str]): Optional. A node or list of node titles to compile. If
                                   none are specified, all hints will be compiled.

        Returns:
            list: A list of all compiled hints as dictionaries.
        """
        compiled = []
        if nodes is not None:
            if type(nodes) is str:
                nodes = [nodes]
            
            for node in nodes:
                if node not in self.hint_nodes:
                    raise NodeException(f"Node '{node}' not found in {self.hint_nodes}")

            use_nodes = [*nodes]
        else:
            use_nodes = [*self.hint_nodes]

        for node in use_nodes:
            compiled_node = []
            
            for node_title, hint_data in self._hints_raw[node].items():

                bosses = [
                    {**boss}
                    for boss in self.bosses_detail
                    if boss['Section'] == node_title
                ]
                # There should only be one key at this level
                if "Generic" in hint_data:
                    compiled_node += hint_data["Generic"]

                for hint_section, hint_items in hint_data.items():
                    compiled_node += self._format_job_hints(hint_section, hint_items)

                if "Generic`" in hint_data:
                    compiled_node += hint_data["Generic`"]
                compiled.append({
                    "section_title": node_title,
                    "section_hints": compiled_node,
                    "section_bosses": bosses,
                })
                break  # Because there really SHOULD be only one key at the root level.

        self.hints = compiled
        self.hint_titles = [
            n['section_title']
            for n in compiled
        ]

        return compiled

    def _format_job_hints(self, job_header: str, job_hints: List[str]) -> List[str]:
        """
        A method which will format individual hint lines in a hint section (node).

        Args:
            job_header (str): Contains a codified string representing how the jobs or line
            should be parsed. Generally this is related to applying "and/or" logic to the
            classes listed.

        Returns:
            list: A formatted list of hints for a node.
        """
        job_header = job_header.replace("`", "")
        if job_header in ["Generic", "Metadata"]:
            return list()

        # Class headers look like this:
        # NOT(opt) UNION|INTERSECTION(opt) <job name> <job name>(opt)
        # Default behavior for single classes is INTERSECTION.
        # NOT is required to negate the jobs.
        # UNION is required when all jobs in the header must be in the list of jobs.

        specified_tags = job_header.split(" ")
        # proceed. Check if this is one of the special cases...
        formatted_header = self._format_hint_header(specified_tags)

        invert_status = False
        if specified_tags[0] == "NOT":
            # Then we want to reverse the next action.
            # Default action is intersection, but it could be specified explicitly.
            invert_status = True
            specified_tags.pop(0)

        mode = "INTERSECTION"
        if specified_tags[0] in ["UNION", "INTERSECTION"]:
            mode = specified_tags.pop(0)

        if self.debug:
            do_include = True

        elif mode == "INTERSECTION":
            do_include = self._jobs_do_intersect(specified_tags)

        elif mode == "UNION":
            do_include = self._jobs_are_union(specified_tags)

        if not self.debug and invert_status:
            do_include = not do_include

        if do_include:
            return [f"{formatted_header} {n}".strip() for n in job_hints]

        return list()

    def _format_hint_header(self, specified_tags: List[str]) -> str:
        """
        A method to format the header of a hint based on jobs and the conditional "and/or" logic.

        Args:
            specified_tags (List[str]): A list of tags which should be applied and used as formatting rules.

        Returns:
            str: A formatted header based on included logic.
        """
        use_tags = [*specified_tags]
        not_indicator = ""

        if len(use_tags) == 0:
            return str()

        if use_tags[0] == "NOT":
            not_indicator = "!"
            use_tags.pop(0)

        string_join = "|"
        if use_tags[0] == "UNION":
            string_join = "+"

        if use_tags[0] in ["UNION", "INTERSECTION"]:
            use_tags.pop(0)

        if (not not_indicator):  # Display only the specified jobs unless "NOT" is specified.
            use_tags = [
                n
                for n in specified_tags
                if n in self.jobs
            ]

        shortcut_tags = [
            class_codes[n]["code"]
            for n in use_tags
            if n in class_codes.keys()
        ]
        
        if len(shortcut_tags) == 0:
            return str()

        header_string = f"[{not_indicator}{string_join.join(shortcut_tags)}]"
        return header_string

    def _jobs_do_intersect(self, jobs_to_compare: List[str]) -> bool:
        """
        A method to check if ANY of the jobs provided as imput are the same as the jobs
        set for the class.

        Args:
            jobs_to_compare (List[str]): The jobs which will be compared to the class jobs.

        Returns:
            bool: True if any of the jobs_to_compare are set in the class. False otherwise.
        """
        # This is the default. This checks to see if any one of the specified jobs
        # is in the list of the set jobs.
        return not set([*self.jobs] + [*self.tags]).isdisjoint(jobs_to_compare)

    def _jobs_are_union(self, jobs_to_compare: List[str]) -> bool:
        """
        A method to check if ALL of the jobs provided as imput are in included in the jobs
        set for the class.

        Args:
            jobs_to_compare (List[str]): The jobs which will be compared to the class jobs.

        Returns:
            bool: True if ALL of the jobs_to_compare are set in the class. False otherwise.
        """
        return all(n in ([*self.jobs] + [*self.tags]) for n in jobs_to_compare)
    
    def dumps(
        self,
        format: str = 'markdown',
        indent: int = None,
    ) -> str|None:
        f"""
        Return hint data as a large string, formatted in varying styles.

        Args:
            format (str): The output format of the hint string. Valid options: {", ".join(dump_modes)}
            indent (int): The number of spaces to use for hint indentation. Markdown and text have default
                          of 0, yaml formats have a default of 2, and json has a default of 4.

        Returns:
            str: A large string containing compiled hint data.
        """
        if format: format = format.lower()
        if format not in dump_modes:
            raise DumpModeException(f'Dump String mode {format} not found in valid dump modes: {dump_modes}')
        
        if format in ['yaml', 'yml']:
            return self._dumps_yaml(indent=indent)
        
        elif format in ['markdown', 'md']:
            return self._dumps_md(indent=indent)
        
        elif format == 'json':
            return self._dumps_json(indent=indent)
        
        elif format == 'text':
            return self._dumps_text(indent=indent)

        return None
    
    def _dumps_md(self, indent: int) -> str:
        if indent is None:
            indent = 0
            
        markdown_text = ''
        for hint in self.hints:
            hints_text = f'{" " * indent}* ' + '\n* '.join(hint['section_hints'])
            markdown_text += f'## {hint["section_title"]}\n{hints_text}\n\n'
        
        return markdown_text
    
    def _dumps_json(self, indent: int|None) -> str:
        if indent is None:
            indent = 4
        return json.dumps(self._hints_with_titles_as_keys(), indent=indent)
    
    def _dumps_yaml(self, indent: int|None) -> str:
        if indent is None:
            indent = 2
        return yaml.safe_dump(self._hints_with_titles_as_keys(), indent=indent)

    def _dumps_text(self, indent: int) -> str:
        if indent is None:
            indent = 0
            
        text = ''
        for hint in self.hints:
            hints_text = f'{" " * indent}' + '\n'.join(hint['section_hints'])
            text += f'{hint["section_title"]}\n{hints_text}\n\n'
        
        return text
    
    def _hints_with_titles_as_keys(self) -> List[Dict[str,List[str]]]:
        return [
            {
                n['section_title']: n['section_hints']
            }
            for n in self.hints
        ]
    
    def load_boss_data(self, display_style: str = 'text'):
        # TODO: add the string
        if display_style: display_style = display_style.lower()
        if display_style not in valid_display_styles:
            raise DisplayStyleException(f'Display style {display_style} not in valid styles {valid_display_styles}')
        
        self.display_style = display_style
        
        boss_root_node = Path(self.boss_root_path, "_bosses.yml")
        
        with boss_root_node.open('r') as f:
            boss_index = yaml.safe_load(f)
        
        self.bosses = boss_index.get('bosses', [])
        self.boss_sources = boss_index.get('sources', [])
        
        bosses_detail = []
        for boss_file in self.bosses:
            boss_node_path = Path(self.boss_root_path, f'{boss_file}.yml')
            with boss_node_path.open('r') as f:
                boss_node = yaml.safe_load(f)
            
            for boss in boss_node['Bosses']:
                
                boss_name = list(boss.keys())[0]
                
                if display_style == 'emoji':
                    boss_types = boss[boss_name].get('Types', [])
                    if boss_types:
                        boss[boss_name]['Types'] = [
                            icon
                            for key, icon in enemy_type_icon_lookup.items()
                            if key in boss_types
                        ]
                    
                    boss_weaknesses = boss[boss_name].get('Elemental Weaknesses', [])
                    if boss_weaknesses:
                        boss[boss_name]['Elemental Weaknesses'] = [
                            icon
                            for key, icon in element_icon_lookup.items()
                            if key in boss_weaknesses
                        ]

                    boss_vulnerabilities = boss[boss_name].get('Vulnerable', [])
                    if boss_vulnerabilities:
                        boss[boss_name]['Vulnerable'] = [
                            icon
                            for key, icon in status_icon_lookup.items()
                            if key in boss_vulnerabilities
                        ]
                
                boss = {
                    'Sort ID': boss_node['Sort ID'],
                    'Section': boss_node['Section'],
                    'Name': boss_name,
                    **boss[boss_name]
                }
                
                # Cleaning these up because they just get in the way right now.
                for key in ['Bestiary', 'Type', 'Description']:
                    if key in boss:
                        del boss[key]
                bosses_detail.append(boss)
        
        bosses_detail.sort(key=lambda x: x['Sort ID']) 
        self.bosses_detail = [*bosses_detail]
        
        return bosses_detail
    
    def load_blue_data(self) -> List[BlueMagic]:
        # TODO: add the string
        blue_root_node = Path(self.blue_root_path, '_grimoire.yml')
        with blue_root_node.open('r') as f:
            blue_index = yaml.safe_load(f)
        
        blue_spell_detail = []
        for spell_file in blue_index['spells']:
            spell_path = Path(self.blue_root_path, spell_file)
            with spell_path.open('r') as f:
                spell = yaml.safe_load(f)

            spell_name = list(spell.keys())[0]
            
            spell_detail = {**spell[spell_name]}

            blue_spell = BlueMagic(
                name = spell_detail.get('Display Name') if 'Display Name' in spell_detail else spell_name,
                alternate_name = spell_detail.get('Alternate Name', None),
                mp_cost = spell_detail.get('MP Cost', 0),
                spell_power = spell_detail.get('Spell Power', None),
                learned_from = [*spell_detail.get('Learned From', [])],
                earliest_acquisition = {**spell_detail.get('Earliest Acquisition', {})},
                best_source = [*spell_detail.get('Best Source', [])],
                description = spell_detail.get('Description', ''),
                note = spell_detail.get('Note', None),
                warning = spell_detail.get('Warning', None),
                fiesta_recommended = spell_detail.get('FJF Recommended', False),
            )

            blue_spell_detail.append(blue_spell)

        self.blue_spell_detail = [*blue_spell_detail]
        self.blue_spells = [
            n.name
            for n in blue_spell_detail
        ]
        self.blue_sources = {**blue_index['sources']}
        self.blue_notes = {**blue_index.get('Notes', {})}
        
        return blue_spell_detail
    
    def load_mix_data(self) -> List[Mix]:
        # TODO: add the string
        mix_path = Path(self.mix_root_path, "mix.yml")
        with mix_path.open('r') as f:
            mix_data:List[Dict] = yaml.safe_load(f)
        
        mix_detail:list[Mix] = []
        for mix in mix_data:
            combos = [mix.get('combo_1')]
            combo_2 = mix.get('combo_2')
            if combo_2 is not None: combos.append(combo_2)
            
            mix_obj = Mix(
                name = mix.get('recipe_name_gba'),
                category = mix.get('category', None),
                recipe_name_snes = mix.get('recipe_name_snes'),
                recipe_name_gba = mix.get('recipe_name_gba'),
                combos = [*combos],
                effect = mix.get('effect', None),
                tags = mix.get('tags', []),
                favorite = mix.get('favorite', False),
            )
            
            mix_detail.append(mix_obj)

        self.mix_detail = [*mix_detail]
        self.mixes = [
            n.name
            for n in mix_detail
        ]
        self.mix_categories = list(set([
            n.category
            for n in mix_detail
        ]))
        
        return mix_detail

# if __name__ == "__main__":
#     bot = Enkibot()
#     print(bot.blue_spell_detail[0])
#     print(bot.blue_spells[0])
#     print(bot.blue_sources)
    # print(bot.hints_path)
    # print(bot.hints_repo_url)
    # print(bot.hint_nodes)
    # print(bot.hints_raw['versions'])
    # print(bot.set_jobs(["UNKNOWN WIND"]))
    # print(bot.set_jobs("Thief"))
    # print(bot.set_jobs(['Monk']))
    # print(bot.set_jobs(['Monk', 'UNKNOWN FIRE', 'Thief', 'Thief']))
    # print(bot.debug)
    # print(bot.toggle_debug())
    # print(bot.jobs)
    # print(bot.tags)
    # print(yaml.dump(bot.compile_hints("moore")))
    # print(yaml.dump(bot.compile_hints("meatcastle")))
    
    # print(yaml.dump(bot.hints))
    # bot.compile_hints()
    # print(yaml.dump(bot.hints))
    
    # debug_bot = Enkibot(debug=True)
    # print(debug_bot.jobs)
    # print(debug_bot.debug)
    # print(debug_bot.compile_hints('versions'))

# command = 'git clone --depth 1 --no-checkout'
