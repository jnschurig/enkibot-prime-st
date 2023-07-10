import constants, general as gen, parse_hint_db as ph
import streamlit as st
import pandas as pd
import os, json, random

@st.cache_data
def get_raw_data():
    # The dataframe is cached to improve performance.
    return pd.DataFrame(ph.easy_df_parse())

def format_section(section_data, class_codes_list:list=None, expanded_setting:bool=False, debug:bool=False, simplified_display:bool=False):
    # Function to draw the section data.
    section_dict = section_data[1]
    new_section_list = json.loads(section_dict['section_parts'])

    md_body = gen.class_match_sections(new_section_list, class_codes_list, debug=debug)

    if simplified_display:
        md_body = '## ' + section_dict['section_name'] + '\n\n' + md_body
        st.markdown(md_body)
    else:
        with st.expander(section_dict['section_name'], expanded=expanded_setting):
            st.markdown(md_body)

    return

def go():
    header_col1, header_col2 = st.columns(2)
    with header_col1:
        st.title('Enkibot Prime ST')

    with header_col2:
        st.image(os.path.join('images', 'enkidu.png'), width=60)

    with st.sidebar:
        st.image(os.path.join('images', 'FFV_logo.png'))
        st.markdown('## Class Selection and Options')
        selection_container = st.container()

        # with header_col2:
        box_col1, box_col2 = st.columns(2)
        with box_col1:
            debug = st.checkbox('Debug', value=False, help='See debug data for all classes')
        with box_col2:
            expanded = st.checkbox('Expand All', value=True, help='Auto expand/collapse all sections')

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

        with st.expander('About', expanded=True):
            st.markdown(constants.ABOUT_TEXT)

        with st.expander('Additional Options', expanded=False):
            # An optional checkbox to set debug functionality for the app.
            # debug_functionality = st.checkbox('Enable Debug Functionality', value=False, help='Enable debug levels of output')

            # Reload the hint database
            if st.button('Clear Cache', help='The hint database is normally chached for quick use. Clear the cache and reload.'):
                st.cache_data.clear()

            show_original_md = st.checkbox('Show Original Markdown', value=False, help='Show the original markdown data instead of the expanders.')

    # Get the codes (KNT, MNK, etc)
    class_codes = gen.get_codes_from_selection(class_selection)

    # Added another functional layer so as to include caching.
    hint_data = get_raw_data()

    # If a search value is set, filter the entire database on the search result.
    if search_value:
        hint_data = hint_data[hint_data.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]

    # Draw the sections
    for section_row in hint_data.iterrows():
        format_section(section_row, class_codes, expanded, debug, show_original_md)

    return 

if __name__ == '__main__':
    st.set_page_config(
        page_title='Enkibot Prime ST',
        page_icon=random.choice(constants.PAGE_ICONS),
        layout='wide',
    )
    go()