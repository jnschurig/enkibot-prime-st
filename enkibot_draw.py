import streamlit as st
import os
from time import sleep
# import re
from enkibot_db import Enkibot
from enkibot_db import status_icon_lookup, element_icon_lookup, enemy_type_icon_lookup, mix_category_colors
from enkibot_dataclasses import BlueMagic, Mix

from typing import List, Dict, Any

valid_draw_modes = [
    'standard',
    'advanced',
]

_section_nav_anchors = {
    'Post-Wind Shrine': 'World 1',
    'World 2 Intro': 'World 2',
    'Antlion': 'World 3',
}

_valid_icon_categories = [
    'all',
    'element',
    'status',
    'type',
]

_boss_data_caption = '''
* There may be listed here hint sections that do not exist in the Hint data.
    This is to allow lookups of bosses that are not normally recommended for FJF.
* If there are any inaccuracies or additions, feel free to contact me: @Reaif on Discord
    or email [jnschurig@gmail.com](mailto:jnschurig@gmail.com)
'''

# Going to use this to possibly do smart replacement for URLs to make them dynamically show up in a popover.
# Stolen from here: https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string
# url_regex = re.compile("""(http|ftp|https):\\/\\/([\\w_-]+(?:(?:\.[\\w_-]+)+))([\\w.,@?^=%&:\\/~+#-]*[\\w@?^=%&\\/~+#-])""", flags=re.IGNORECASE)

class DrawModeException(Exception):
    pass

class EnkiDraw(Enkibot):
    def __init__(
        self,
        enkibot: Enkibot = None,
        jobs: str|list[str] = None,
        debug: bool = False,
        display_style: str = 'text',
    ):
        if enkibot is None:
            enkibot = Enkibot(
                jobs=jobs,
                debug=debug,
                display_style=display_style
            )

        # Set all the self properties the same as the original class.            
        self.__dict__ = {**enkibot.__dict__}
            
        self._boss_col_config = {
            'Vulnerable': st.column_config.ListColumn(
                label='Statuses',
                help=self.icon_legend('status'),
            ),
            'Elemental Weaknesses': st.column_config.ListColumn(
                label='Weak to Element',
                help=self.icon_legend('element'),
            ),
            'Types': st.column_config.ListColumn(
                label='Types',
                help=self.icon_legend('type'),
            ),
        }
        
        self._is_colored_text = False
        
        return
    
    def toggle_colorized_text(self, use_colors: bool = None):
        if use_colors is None:
            use_colors = not self._is_colored_text

        if use_colors != self._is_colored_text:
            # toggle the colors...
            
            
            self._is_colored_text = use_colors
        
        return self._is_colored_text
    
    def render_hints(
        self,
        draw_mode: str = 'standard',
        expanded: bool = False,
    ):
        if draw_mode not in valid_draw_modes:
            raise DrawModeException(f'Draw mode {draw_mode} not found in valid draw modes: {valid_draw_modes}')

        draw_mode = draw_mode.lower()
        if draw_mode == 'advanced':
            self.advanced_render()
        elif draw_mode == 'standard':
            st.markdown('[World 1](#world-1) | [World 2](#world-2) | [World 3](#world-3)')
            for node in self.hints:
                self._standard_render(
                    hint_node=node,
                    expanded=expanded,
                )
        
        return
    
    def advanced_render(
        self,
        hints: list[dict]|dict = None,
        max_display_nodes: int = 10,
    ) -> None:
        if hints is None:
            hints = [*self.hints]
        elif type(hints) is dict:
            hints = [hints]
            
        if 'section_history' not in st.session_state:
            st.session_state['section_history'] = [0]

        current_node = self.hint_titles[st.session_state['section_history'][0]]
        previous_node = self.hint_titles[0] if len(st.session_state['section_history']) <= 1 else self.hint_titles[st.session_state['section_history'][1]]
        next_node = self.hint_titles[st.session_state['section_history'][0]+1]
        
        # The earliest thing should always be 0.
        if len(st.session_state['section_history']) > 20:
            st.session_state['section_history'][-1] = 0
        
        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([2, 2, 2, 1])

        with nav_col4:
            if st.button(
                'Reset',
                use_container_width=True,
                help='Reset the navigation and history and return to the beginning.',
            ):
                st.session_state['section_history'] = [0]
                st.rerun()
        
        with nav_col2:
            if st.button(
                'Back',
                use_container_width=True,
                help=f"Return to **{previous_node}**",
            ) and len(st.session_state['section_history']) > 1:
                st.session_state['section_history'].pop(0)
                # st.toast(f"Restoring {previous_node}")
                # sleep(1.5)
                st.rerun()
            
        with nav_col3:
            if st.button(
                'Next',
                use_container_width=True,
                help=f"Close section and show **{next_node}** at the top."
            ):
                st.session_state['section_history'].insert(
                    0,
                    st.session_state['section_history'][0]+1
                )
                st.rerun()
                
        future_nodes = st.session_state['section_history'][0] + max_display_nodes
        
        with nav_col1:
            with st.popover('Navigation', use_container_width=True):
                st.markdown('##### **Jump to:**')
                jump_to_node = st.radio(
                    label='**Jump to:**',
                    options=self.hint_titles,
                    index=self.hint_titles.index(current_node),
                    label_visibility='collapsed',
                )
                
                if self.hint_titles.index(jump_to_node) != st.session_state['section_history'][0]:
                    st.session_state['section_history'].insert(0, self.hint_titles.index(jump_to_node))
                    st.rerun()

        for idx, hint in enumerate(hints):
            if idx < st.session_state['section_history'][0]:
                continue
            
            if max_display_nodes is not None and max_display_nodes > 0:
                if idx > future_nodes:
                    continue
            
            self._render_advanced_node(
                node=hint,
                index=idx,
            )
            
        return
    
    def _render_advanced_node(
        self,
        node: dict,
        index: int = None,
    ):
        # hint_header_col1, hint_header_col2, dead_col = st.columns(3)

        # with hint_header_col2:
        #     if st.button(
        #         'Next',
        #         key=f'top_hint_complete_{index}',
        #         use_container_width=True
        #     ):
        #         st.session_state['section_history'].insert(0, index+1)
        #         st.rerun()

        # with hint_header_col1:
        st.markdown(f"#### {node['section_title']}")
            
        section_bosses = [
            self._boss_column_selection(boss_node=n)
            for n in node.get('section_bosses', None)
        ]
        if section_bosses:
            st.dataframe(
                data=section_bosses,
                use_container_width=True,
                column_config=self._boss_col_config,
            )
        
        st.markdown('* ' + '\n* '.join(node['section_hints']))

        # hint_footer_col1, hint_footer_col2, dead_col = st.columns(3)
        
        # with hint_footer_col2:
        #     if st.button(
        #         'Next',
        #         key=f'bottom_hint_complete_{index}',
        #         use_container_width=True
        #     ):
        #         st.session_state['section_history'].insert(0, index+1)
        #         st.rerun()
            
        st.divider()
        return
    
    def _standard_render(
        self,
        hint_node: dict,
        expanded: bool = False,
    ) -> None:
        section_title = hint_node.get('section_title')
        section_hints = hint_node.get('section_hints')
        section_bosses = [
            self._boss_column_selection(boss_node=n)
            for n in hint_node.get('section_bosses', None)
        ]

        if section_title in _section_nav_anchors:
            anchor_text = _section_nav_anchors[section_title]
            st.info(f'##### {anchor_text}')
            
        with st.expander(label=section_title, expanded=expanded):
            if section_bosses:
                st.dataframe(
                    data=section_bosses,
                    use_container_width=True,
                    column_config=self._boss_col_config,
                )
                
            st.markdown('* ' + '\n* '.join(section_hints))
        
            # Section Customizations
            if section_title == 'Bridgamesh':
                self._bridgamesh_popover()

            elif section_title == 'Neo Ex Cactuar':
                self._ned_popover()

        return
    
    def _boss_column_selection(
        self,
        boss_node: dict,
        simplified: bool = True,
    ) -> dict:
        del boss_node['Sort ID']
        if simplified:
            # if boss_node['Section'] != boss_node['Name']:
            #     boss_node['Name'] = f"{boss_node['Section']} - {boss_node['Name']}"
            del boss_node['Section']

        return boss_node
    
    def _bridgamesh_popover(self):
        with st.popover('Big Bridge Encounters'):
            img1_col, img2_col = st.columns(2)

            with img1_col:
                st.caption('Section 1 - pre Gilgamesh')
                st.image(os.path.join('images', 'bigbridge_section1.png'))
            with img2_col:
                st.caption('Section 2 - post Gilgamesh')
                st.image(os.path.join('images', 'bigbridge_section2.png'))
        return
    
    def _ned_popover(self):
        with st.popover('Image Guide'):
            st.image('https://i.imgur.com/newtN7c.png')
        return

    def icon_legend(self, category: str = 'all') -> str:
        if category: category = category.lower()
        if category not in _valid_icon_categories:
            raise DrawModeException(f'Category {category} not found in valid categories: {_valid_icon_categories}')
        
        legend_body = ''
        
        if category in ['all', 'element']:
            for name, icon in element_icon_lookup.items():
                legend_body += f'- {icon} {name}\n'
        
        if category in ['all', 'status']:
            for name, icon in status_icon_lookup.items():
                legend_body += f'- {icon} {name}\n'
        
        if category in ['all', 'type']:
            for name, icon in enemy_type_icon_lookup.items():
                legend_body += f'- {icon} {name}\n'
        
        return legend_body
    
    def render_all_bosses(
        self,
        simplified: bool = False,
    ):
        column_sizes = [3, 1]
        if self.display_style == 'text':
            column_sizes = [100, 1]
        
        bosses_col, legend_col = st.columns(column_sizes)
        
        with bosses_col:
            
            st.dataframe(
                data=[
                    self._boss_column_selection(
                        boss_node=n,
                        simplified=simplified,
                    )
                    for n in self.bosses_detail
                ],
                column_config=self._boss_col_config,
                height=600,
                hide_index=True,
                use_container_width=True,
            )
        
            st.caption(_boss_data_caption)
        
        if self.display_style == 'emoji':
            with legend_col:
                st.markdown('#### Legend')
                
                legend_sub_col1, legend_sub_col2 = st.columns(2)
                
                with legend_sub_col1:
                    st.markdown(f'**Types**:\n{self.icon_legend("type")}')
            
                    st.markdown(f'**Elements**:\n{self.icon_legend("element")}')

                with legend_sub_col2:        
                    st.markdown(f'**Statuses**:\n{self.icon_legend("status")}')
        
        return

    def render_all_mixes(self, search_value: str = None, columns: int = 1, key: str='main'):
        st.subheader('!Mix Library')
        
        if search_value is None:
            search_value = st.text_input(
                label='Search', 
                value=None,
                placeholder='Search !Mix', 
                label_visibility='collapsed', 
                help='Search mix recipes for key terms or values',
                key=f'mix_search_{key}',
                # disabled=True,
            )
        search_value = search_value.strip().lower() if search_value is not None and search_value.strip() != '' else None

        header_cols = st.columns(columns)
        
        with header_cols[0 % columns]:
            favorites_only = st.toggle(
                label='Favorites Only',
                value=False,
                key=f'mix_faves_toggle_{key}',
                help='Only show Fiesta favorites',
            )
        
        selected_categories = []
        for idx, category in enumerate(self.mix_categories):
            with header_cols[(idx+1) % columns]:
                if st.toggle(
                    label=category.title(),
                    value=True,
                    key=f'mix_toggle_{category.lower()}_{key}',
                    help=f'Include/Exclude Mixes categorized as "{category.lower()}"',
                ):
                    selected_categories.append(category)
        
        display_mixes:List[Mix] = self.search_list_members(search_value=search_value, subject_list=self.mix_detail)
        
        display_mixes = [
            n
            for n in display_mixes
            if n.category in selected_categories
            and (not favorites_only or n.favorite)
        ]
        
        st.markdown(f'Mixes Shown: __*{len(display_mixes)}*__ of {len(self.mixes)}')
        
        st.divider()
        for mix in display_mixes:
            self.render_mix(mix=mix, columns=columns)
            st.divider()
        return
    
    def search_list_members(
        self,
        search_value: str|None,
        subject_list: List[Mix|BlueMagic|List|Dict],
    ) -> List:
        return [
            n
            for n in subject_list
            if search_value is None or self.search_object(search_value=search_value.lower(), search_object=n)
        ]

    def search_object(
        self,
        search_value: str,
        search_object: Any,
    ) -> bool:
        search_dict = {}
        if type(search_object) in [Mix, BlueMagic]:
            search_dict = {**search_object.__dict__}
        elif type(search_object) is dict:
            search_dict = {**search_object}
        elif type(search_object) is list:
            for item in search_object:
                if self.search_object(search_value=search_value, search_object=item):
                    return True
        elif type(search_object) is str and search_value in search_object.lower():
            return True
        
        for value in search_dict.values():
            if type(value) is not str:
                result = self.search_object(search_value=search_value, search_object=value)
                if result: return result
            elif search_value in value.lower():
                return True
        return False
    
    def render_all_blue(self, search_value: str = None, columns: int = 1, key: str='main'):
        title_cols = st.columns(columns)
        with title_cols[0 % columns]:
            st.subheader('!Blue Grimoire')
            
        with title_cols[1 % columns]:
            with st.popover('Help with !Blue'):
                self.render_help_dict(self.blue_notes, columns=columns)
        
        # options_cols = st.columns(columns)
        with st.container():
        # with options_cols[0 % columns]:
            search_value = st.text_input(
                label='Search !Blue',
                value=None,
                placeholder='Search !Blue',
                label_visibility='collapsed',
                key=f'blue_search_{key}',
            )
            
        # with options_cols[1 % columns]:
            filter_recommended = st.toggle(
                label='Favorites Only',
                value=False,
                key=f'blue_recommended_{key}',
                help='Show only Fiesta favorites',
            )
        
        search_value = search_value.strip().lower() if search_value is not None and search_value.strip() != '' else None
        
        # display_blue = self.search_blue(search_value=search_value)
        display_blue:List[BlueMagic] = self.search_list_members(search_value=search_value, subject_list=self.blue_spell_detail)
        
        if filter_recommended:
            display_blue = [
                n
                for n in display_blue
                if n.fiesta_recommended
            ]
        
        st.markdown(f'Spells Shown: __*{len(display_blue)}*__ of {len(self.blue_spells)}')
        
        st.divider()
        
        for b in display_blue:
            self.render_blue_spell(blue_spell=b, columns=columns)
            st.divider()
        self.render_url_bar('Sources', self.blue_sources)
        return
    
    def render_mix(self, mix: Mix, columns: int = 3):
        recommended = '⭐ ' if mix.favorite else ''
        
        title_cols = st.columns(columns)
        title_cols[0 % columns].markdown(f'{recommended}__{mix.name}__')
        
        if mix.recipe_name_snes is not None:
            title_cols[1 % columns].caption(f'__{mix.recipe_name_snes}__')
        
        title_cols[2 % columns].markdown(f'__:{mix_category_colors[mix.category]}[{mix.category}]__')
        
        body_cols = st.columns(columns)
        with body_cols[0 % columns]:
            pass
            recipe_text = '\n- '.join(mix.combos)
            st.markdown(f'- {recipe_text}')
            
        with body_cols[1 % columns]:
            pass
            st.info(mix.effect)
        
        if self.debug and mix.tags:
            st.caption(f'Tags: {", ".join(mix.tags)}')
        
        return

    def render_blue_spell(self, blue_spell: BlueMagic, columns: int = 3):
        recommended = '⭐ ' if blue_spell.fiesta_recommended else ''
        title_cols = st.columns(columns)
        
        title_cols[0 % columns].markdown(f'{recommended}__{blue_spell.name}__')
            
        if blue_spell.alternate_name is not None:
            title_cols[1 % columns].caption(f'__{blue_spell.alternate_name}__')
        
        # if blue_spell.fiesta_recommended:
        #     title_cols[2 % columns].markdown(f'__:green[Fiesta Recommended]__')
            
        st.info(blue_spell.description)
        
        stats_section = f'- MP Cost: {blue_spell.mp_cost}'
        if blue_spell.spell_power is not None: stats_section += f'\n- Spell Power: {blue_spell.spell_power}'
        
        body_cols = st.columns(columns)
        
        with body_cols[0 % columns]:
            st.markdown(stats_section)
            with st.popover(label='Learned From'):
                st.markdown(self._blue_bestiary_dict_to_markdown(markdown_title='Learned From:', bestiary_list=blue_spell.learned_from))

        earliest_ack_idx = 1
        with body_cols[earliest_ack_idx % columns]:
            st.markdown(
                self._blue_bestiary_dict_to_markdown(
                    markdown_title='Earliest Acquisition:',
                    bestiary_list=blue_spell.earliest_acquisition
                )
            )

        # When we have many columns, stretch this out. Otherwise it should be
        # in the same column as earliest acquisition
        best_source_idx = earliest_ack_idx if columns <= 2 else earliest_ack_idx + 1
        with body_cols[best_source_idx % columns]:
            st.markdown(
                self._blue_bestiary_dict_to_markdown(
                    markdown_title='Best Sources:',
                    bestiary_list=blue_spell.best_source
                )
            )
            
        if blue_spell.note:
            st.caption(f'Note: {blue_spell.note}')
            
        if blue_spell.warning:
            st.warning(f'Warning: {blue_spell.warning}')
        
        return
    
    def _blue_bestiary_dict_to_markdown(self, markdown_title: str, bestiary_list: list) -> str:
        markdown_text = markdown_title
        
        for entry in bestiary_list:
            if type(entry) is str:
                markdown_text += f'\n- {entry}'
            elif type(entry) is dict:
                for key, value in entry.items():
                    markdown_text += f'\n- {key}'
                    if type(value) is not list:
                        markdown_text += f' - {value}'
                    else:
                        for item in value:
                            markdown_text += f'\n  - {item}'
        
        return markdown_text
    
    def render_help_dict(self, notes:dict, columns: int = 1):
        # display_cols = st.columns(columns)
        
        # for idx, title in enumerate(notes.keys()):
            # use_col = display_cols[idx % columns]
            
            # # use_col.text(title, help=notes[title])
            # with use_col.popover(title):
            #     st.markdown(notes[title])
        for title, body in notes.items():
            st.markdown(f'__{title}__ - {body}')
            
            
    def render_url_bar(self, bar_title: str, url_dict: dict):
        url_bar_text = bar_title
        for url_title, url in url_dict.items():
            url_bar_text += f' | [{url_title}]({url})'
            
        st.markdown(url_bar_text)
        
        return
