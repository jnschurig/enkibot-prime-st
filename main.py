import streamlit as st
import pandas as pd
import os, json, random
import constants, general as gen, parse_hint_db as ph
from class_resources import blue_resources

@st.cache_data
def get_raw_data():
    # The dataframe is cached to improve performance.
    return pd.DataFrame(ph.easy_df_parse())

def format_section(section_data, class_codes_list:list=None, expanded_setting:bool=False, debug:bool=False, simplified_display:bool=False):
    # Function to draw the section data.

    new_section_list = json.loads(section_data['section_parts'])

    md_body = gen.class_match_sections(new_section_list, class_codes_list, debug=debug)

    if not simplified_display:
        # Add world-specific section anchors.
        if section_data['section_name'] in constants.SECTION_NAV_ANCHORS.keys():
            anchor_text = constants.SECTION_NAV_ANCHORS[section_data['section_name']]
            st.info(f'#### {anchor_text}')

        # Draw Section
        with st.expander(section_data['section_name'], expanded=expanded_setting):
            st.markdown(md_body)

    # Restore the body header sections...
    md_body = '## ' + section_data['section_name'] + '\n\n' + md_body
    if simplified_display:
        st.markdown(md_body)

    return md_body

def go():
    #---------------#
    # Title Section #
    #---------------#
    header_col1, header_col2 = st.columns(2)
    with header_col1:
        st.title('Enkibot Prime ST')

    with header_col2:
        st.image(os.path.join('images', 'enkidu.png'), width=50)

    #---------#
    # Sidebar #
    #---------#
    with st.sidebar:
        st.image(os.path.join('images', 'FFV_logo.png'))
        st.markdown('## Class Selection and Options')
        selection_container = st.container()

        box_col1, box_col2 = st.columns(2)
        with box_col1:
            debug = st.checkbox('Debug', value=False, help='See debug data for all classes')
        with box_col2:
            expanded = st.checkbox('Expand All', value=False, help='Auto expand/collapse all sections')

        with selection_container:
            class_selection = st.multiselect(
                'Class Selection', 
                constants.UNKNOWN_OPTIONS + list(constants.CLASS_CODE_LOOKUP.keys()),
                help='',
                disabled=debug,
                label_visibility='collapsed',
                )

        search_value = st.text_input(
            'Search', 
            value='', 
            placeholder='Search Hint Data', 
            label_visibility='collapsed', 
            help='Search database for key terms or values'
        )

        st.divider()

        #-----------------#
        # Class Resources #
        #-----------------#
        # BLUE MAGE
        if 'Blue-Mage' in class_selection:
            with st.expander('Blue Resources'):
                blue_resources.go(True)

        # CHEMIST
        if 'Chemist' in class_selection:
            # We don't need to load this most of the time most likely,
            # so only do it when the chemist option is actually selected.
            from class_resources import mix_resources
            with st.expander('Chemist Resources'):
                mix_resources.go()

        with st.expander('About', expanded=True):
            st.markdown(constants.ABOUT_TEXT)

        #--------------------#
        # Additional Options #
        #--------------------#
        with st.expander('Additional Options', expanded=False):
            # An optional checkbox to set debug functionality for the app.
            # debug_functionality = st.checkbox('Enable Debug Functionality', value=False, help='Enable debug levels of output')

            button_col1, button_col2 = st.columns(2)

            with button_col1:
                # Reload the hint database
                if st.button('Clear Cache', help='The hint database is normally chached for quick use. Clear the cache and reload.'):
                    st.cache_data.clear()

            with button_col2:
                if st.button('Reset Session', help='This will reset the browser session state (Warning: Experimental!)'):
                    gen.reset_session()
                    st.experimental_rerun()
            
            show_original_md = st.checkbox('Simplified Display', value=False, help='Show the original markdown data instead of the expanders.')

    # Get the codes (KNT, MNK, etc)
    class_codes = gen.get_codes_from_selection(class_selection)

    with st.spinner('Fetching Data...'):
        # Added another functional layer so as to include caching.
        hint_data = get_raw_data()

    # If a search value is set, filter the entire database on the search result.
    if search_value:
        hint_data = hint_data[hint_data.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]

    # Declare the page tabs
    enki_main_tab, enki_raw_output_tab, enki_blue_tab, enki_changelog_tab = st.tabs(['Enkibot', 'Raw Output', '!Blue Grimoire', 'Changelog'])

    #-------------------#
    # MAIN HINT SECTION #
    #-------------------#
    with enki_main_tab:
        if show_original_md:
            st.markdown('[World 1](#post-wind-shrine) | [World 2](#world-2-intro) | [World 3](#antlion)')
        else:
            st.markdown('[World 1](#world-1) | [World 2](#world-2) | [World 3](#world-3)')

        # Draw the sections
        full_body = ''
        for idx, section_row in hint_data.iterrows():
            full_body += format_section(
                section_data=section_row, 
                class_codes_list=class_codes, 
                expanded_setting=expanded, 
                debug=debug, 
                simplified_display=show_original_md, 
            ) + '\n'

    #------------#
    # Raw Output #
    #------------#
    with enki_raw_output_tab:
        if len(class_codes) > 0:
            file_classes = gen.format_class_list_as_str(class_codes, '_')
        elif debug:
            file_classes = 'all'
        else:
            file_classes = 'no_classes'

        st.download_button(
            'Export to File', 
            data=full_body, 
            file_name=f'enkibot_hints_{file_classes}.md', 
            help='Download raw text to file.'
        )
        st.code(full_body, language='markdown')

    #---------------#
    # Blue Grimoire #
    #---------------#
    with enki_blue_tab:
        blue_resources.go(False)

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
        page_icon=random.choice(constants.PAGE_ICONS),
        layout='wide',
        menu_items={
            "About": '''Check out the [Github Repo](https://github.com/jnschurig/enkibot-prime-st). 
            For issues, help, bugs, etc you can raise an issue on Github, [send me an email](mailto:jnschurig@gmail.com), 
            or come to the Discord mentioned in the intro text.''',
        }
    )
    go()