import streamlit as st
import pandas as pd
import os

@st.cache_data
def fetch_mix_data():
    # Need a non-relative path.
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, 'data', 'mix_recipes.csv')
    return pd.read_csv(csv_path, keep_default_na=False)

def format_mix_entry(mix_row):
    with st.container():
        mix_name = mix_row['recipe_name_gba']

        mix_col1, mix_col2, mix_col3 = st.columns([3, 3, 2])
        mix_col1.markdown('#### ' + mix_name)
        if mix_row['recipe_name_snes'] != mix_name:
            mix_col2.caption('#### ' + mix_row['recipe_name_snes'])
        mix_col3.caption('#### ' + mix_row['category'])

        recipe = '- ' + mix_row['mix_1']

        if mix_row['mix_2']:
            recipe += '\n- ' + mix_row['mix_2']

        st.markdown(recipe)

        if mix_row['star'] == 1:
            st.success(mix_row['effect'])
        else:
            st.info(mix_row['effect'])

        st.divider()

    return

def go(key:str = 'sidebar'):
    st.title('!Mix Library')

    # Fetch mix data.
    mix_data = fetch_mix_data()

    # Mix search
    mixes_search_value = st.text_input(
        'Search', 
        value='', 
        placeholder='Search Mix Recipes', 
        label_visibility='collapsed', 
        help='Search mix recipes for key terms or values',
        key=f'mix_search_{key}',
    )

    if mixes_search_value:
        mix_data = mix_data[mix_data.apply(lambda row: row.astype(str).str.contains(mixes_search_value, case=False).any(), axis=1)]

    # Checkboxes and options
    category_filters = []
    cat_col1, cat_col2 = st.columns(2)
    with cat_col1:
        if st.checkbox('Healing', value=False, key=f'is_healing_{key}',):
            category_filters.append('HEALING')
        if st.checkbox('Support', value=False, key=f'is_support_{key}',):
            category_filters.append('SUPPORT')
    with cat_col2:
        if st.checkbox('Status Ailment', value=False, key=f'is_status_{key}',):
            category_filters.append('STATUS AILMENT')
        if st.checkbox('Offense', value=False, key=f'is_offense_{key}',):
            category_filters.append('OFFENSE')

    if len(category_filters) > 0:
        mix_data = mix_data[mix_data['category'].isin(category_filters)]

    with cat_col1:
        if st.checkbox('Sort by Favorite', help='Show particularly useful mixes first.', key=f'sort_by_fav_{key}',):
            mix_data = mix_data.sort_values(by=['category'])
            mix_data = mix_data.sort_values(by=['star'], ascending=False)

    st.markdown('Mixes: **_' + str(len(mix_data.index)) + '_**')

    # Draw each mix
    for idx, mix_row in mix_data.iterrows():
        format_mix_entry(mix_row)

    # Site your sources
    st.caption('Mix Recipe Resource: [Final Fantasy Wiki](https://finalfantasy.fandom.com/wiki/Mix_(Final_Fantasy_V))')
    return

if __name__ == '__main__':
    st.set_page_config(
        page_title='Mix Resources',
        page_icon='⚗️',
        layout='centered',
    )

    if st.checkbox('Show in Sidebar', value=True):
        with st.sidebar:
            go()
    else:
        go()
