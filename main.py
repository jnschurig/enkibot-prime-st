import constants, general as gen, parse_hint_db as ph
import streamlit as st
import random as rd
import pandas as pd
import os

@st.cache_data
def get_raw_data():
    return pd.DataFrame(ph.easy_df_parse())

def format_section(section_data, class_codes_list:list=None, expanded_setting:bool=False, debug:bool=False):
    section_dict = section_data[1]
    with st.expander(section_dict['section_name'], expanded=expanded_setting):
        st.markdown(gen.class_match_sections(section_dict['section_parts'], class_codes_list, debug=debug))

    return

def go():
    header_col1, header_col2 = st.columns([9,1])
    with header_col1:
        st.title('Enkibot Prime ST')

    with header_col2:
        st.image(os.path.join('images', 'enkidu.png'), width=60)

    # header_col1, header_col2 = st.columns([8, 1])
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

        st.markdown(constants.ABOUT_TEXT)

        

    # st.write('RAW SELECTION')
    # st.json(class_selection)

    class_codes = gen.get_codes_from_selection(class_selection)

    # st.json(class_codes)
    hint_data = get_raw_data()
    if search_value:
        hint_data = hint_data[hint_data.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]

    # st.table(hint_data)


    # st.json(hint_data)
    for section_row in hint_data.iterrows():
        format_section(section_row, class_codes, expanded, debug)
        pass

    return 

if __name__ == '__main__':
    st.set_page_config(
        page_title='Enkibot Prime ST',
        page_icon=rd.choice(constants.PAGE_ICONS),
        layout='wide',
    )
    go()