import streamlit as st
import os
import random
from enkibot_db import Enkibot, dump_modes, class_codes, unknown_options
from enkibot_draw import EnkiDraw

from typing import List

ABOUT_TEXT = '''
A [Four Job Fiesta](https://www.fourjobfiesta.com/) hint generator.

Hint data was helpfully provided from [Enkibot Prime](https://enkibot-prime.herokuapp.com/), and
credit goes to the original creators.

This version was made using Python and Streamlit and has additional content and functionality over
the original. Additions include boss info, !Blue, and !Mix sections. Check out the
[Github Repo](https://github.com/jnschurig/enkibot-prime-st).
'''

PAGE_ICONS = [
    '⚔️',
    '🗡️',
    '🛡️',
    '🔪',
    '🏹',
    '🎀',
    '🪄',
    '🔔',
    '🎶',
    '⛺',
    '⚗️',
    '🔨',
    '🪓',
    '💃',
    '🕺',
    # '⏱️',
    '⏳',
    # '📖',
    # '🤜🏽',
    # '📜',
    # '🧪',
    '❄️',
    '🔥',
    '⚡',
    '💧',
    # '🍃',
    # '⛰️',
    # '🫧',
    # '✨',
    # '🌈',
    '🧟',
    '🐲',
    '🦄',
    '🐸',
    '💀',
    '🕶️',
]

@st.cache_data
def get_hint_dump(_enkibot: Enkibot, jobs: List, format: str, indent: int = None) -> str:
    f"""
    Fetch hint data as a large string, formatted in varying styles.

    Args:
        _enkibot (Enkibot): An enkibot object.
        jobs (List): The list of jobs for the hints. This arg is not used functionally, but aids in caching.
        format (str): The output format of the hint string. Valid options: {", ".join(dump_modes)}
        indent (int): The number of spaces to use for hint indentation. Markdown and text have default
                      of 0, yaml formats have a default of 2, and json has a default of 4.

    Returns:
        str: A large string containing compiled hint data.
    """
    return _enkibot.dumps(format=format, indent=indent)

def initialize_session_state():
    """
    Sets the session state at the beginning of each application loop.
    This will utilize query parameters and session state.
    """
    if st.session_state.get('experimental_display') is None:
        display_param = True if st.query_params.get('experimental_display', 'false').lower() == 'true' else False
        st.session_state['experimental_display'] = display_param
    
    if st.session_state.get('debug') is None:
        debug_param = True if st.query_params.get('debug', 'false').lower() == 'true' else False
        st.session_state['debug'] = debug_param
        
    if st.session_state.get('class_selection') is None:
        # Initialize with a unique list
        st.session_state['class_selection'] = list(set(st.query_params.get_all('job')))
        
    return

def main():
    """
    The main function. This will run from top to bottom for every action that can
    change the app content.
    """
    initialize_session_state()

    #---------------#
    # Title Section #
    #---------------#
    header_col1, header_col2 = st.columns(2)
    with header_col1:
        st.title('Enkibot Prime ST')

    with header_col2:
        st.image(os.path.join('images', 'enkidu_no_shadow.png'), width=64)

    # url = f"[Share](?job={(st.query_params.get('job'))})"
    # st.markdown(url)

    #---------#
    # Sidebar #
    #---------#
    with st.sidebar:
        st.image(os.path.join('images', 'FFV_logo.png'))
        st.markdown('## Class Selection and Options')
        selection_container = st.container()

        box_col1, box_col2 = st.columns(2)
        with box_col1:
            debug = st.checkbox(
                'Debug',
                value=st.session_state['debug'],
                help='See hint data for _**all**_ classes',
                key='debug',
            )
            
        with box_col2:
            expanded = st.checkbox('Expand All', value=True, help='Auto expand/collapse all sections')

        class_options = [
            *unknown_options,
            *list(class_codes.keys())
        ]

        with selection_container:
            class_selection = st.multiselect(
                label='Class Selection', 
                options=class_options,
                default=st.session_state.get('class_selection', []),
                help='',
                disabled=debug,
                label_visibility='collapsed',
                key='class_selection',
                )
            
            st.query_params['job'] = [*class_selection]

        st.divider()

        #-----------------#
        # Class Resources #
        #-----------------#
        # BLUE MAGE
        blue_sidebar_container = st.container()

        # CHEMIST
        chemist_sidebar_container = st.container()

        with st.expander('About', expanded=False):
            st.markdown(ABOUT_TEXT)

        #--------------------#
        # Additional Options #
        #--------------------#
        with st.expander('Additional Options', expanded=False):
            # Reload the hint database
            if st.button('Clear Cache', help='The hint database is normally chached for quick use. Clear the cache and reload.'):
                st.cache_data.clear()

            use_boss_emoji = st.toggle('Use Icons', value=True, help='Enabled = Show emoji or pictures for icons in hint data where available. Disabled = show text only.')
            display_style = 'emoji' if use_boss_emoji else 'text'
            
            use_experimental_hints = st.toggle(
                label='Experimental Hint Display',
                value=st.session_state['experimental_display'],
                help='Enkibot hints will be displayed using experimental rendering options.',
            )
            hint_draw_mode = 'advanced' if use_experimental_hints else 'standard'

    # Initialize Enkibot
    bot = EnkiDraw(
        jobs=class_selection,
        debug=debug,
        display_style=display_style,
    )
    
    # Add Blue sidebar option
    if 'Blue-Mage' in class_selection or debug:
        with blue_sidebar_container.expander('Blue Resources'):
            bot.render_all_blue(columns=1, key='sidebar')
    
    # Add Chemist sidebar option
    if 'Chemist' in class_selection or debug:
        with chemist_sidebar_container.expander('Chemist Resources'):
            bot.render_all_mixes(columns=1, key='sidebar')

    # Declare the page tabs
    enki_main_tab, enki_raw_output_tab, enki_blue_tab, enki_mix_tab, enki_boss_tab, enki_changelog_tab = st.tabs(
        [
            'Enkibot',
            'Raw Output',
            '!Blue',
            '!Mix',
            'Bosses',
            'Changelog',
        ]
    )

    #--------#
    # Bosses #
    #--------#
    with enki_boss_tab:
        bot.render_all_bosses()

    #-------------------#
    # MAIN HINT SECTION #
    #-------------------#
    with enki_main_tab:
        bot.render_hints(
            draw_mode=hint_draw_mode,
            expanded=expanded,
        )

    #------------#
    # Raw Output #
    #------------#
    with enki_raw_output_tab:
        download_col, selector_col = st.columns([1, 1])
        
        with selector_col:
            output_format = st.selectbox(
                'Format',
                options=[n for n in dump_modes if n not in ['markdown', 'yml']],
                label_visibility='collapsed',
            )
        
        text_body = get_hint_dump(bot, jobs=bot.jobs, format=output_format)
        
        jobs_descriptor = 'all' if debug else "_".join(bot.jobs)

        with download_col:
            st.download_button(
                'Export to File', 
                data=text_body, 
                file_name=f'enkibot_hints_{jobs_descriptor}.{output_format}', 
                help='Download raw text to file.',
            )
            
        st.code(text_body, language=output_format)

    #---------------#
    # Blue Grimoire #
    #---------------#
    with enki_blue_tab:
        bot.render_all_blue(columns=3)

    #-------------#
    # Mix Library #
    #-------------#
    with enki_mix_tab:
        # mix_resources.go(key='tab')
        bot.render_all_mixes(columns=3, key='main')

    #-----------#
    # Changelog #
    #-----------#
    with enki_changelog_tab:
        st.markdown('## Changelog')

        with open('changelog.md', 'r') as f:
            changelog_text = f.read()
        st.markdown(changelog_text)

    # Footer URL to go back to the top.
    st.markdown('[Top](#enkibot-prime-st)')

    return 

if __name__ == '__main__':
    st.set_page_config(
        page_title='Enkibot Prime ST',
        page_icon=random.choice(PAGE_ICONS),
        layout='wide',
        menu_items={
            "About": '''Check out the [Github Repo](https://github.com/jnschurig/enkibot-prime-st). 
            For issues, help, bugs, etc you can raise an issue on Github, [send me an email](mailto:jnschurig@gmail.com), 
            or come to the Discord mentioned in the intro text.''',
        }
    )
    main()