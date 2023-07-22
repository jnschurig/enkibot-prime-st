import streamlit as st
import pandas as pd
import yaml
import os, json

SIDEBAR_COL_COUNT = 2
MAIN_COL_COUNT = 4

# @st.cache_data
def fetch_yaml_data(file_name:str=None):

    # Need a non-relative path.
    script_dir = os.path.dirname(__file__)
    blue_dir = os.path.join(script_dir, 'data', 'blue_magic')

    if file_name is None:
        blue_file = os.path.join(blue_dir, '_grimoire.yml')
    else:
        blue_file = os.path.join(blue_dir, file_name)

    try:
        with open(blue_file, 'r') as f:
            blue_data = yaml.safe_load(f)
    except:
        return {'Message': 'Unable to load data.', 'path': blue_file}

    return blue_data

@st.cache_data
def blue_data():
    blue_index = fetch_yaml_data()

    all_spell_detail = []
    for file_name in blue_index['spells']:
        spell_detail = fetch_yaml_data(file_name)
        spell_name = next(iter(spell_detail))
        spell_detail = {
            'name': spell_name,
            'entry': spell_detail[spell_name]
        }
        all_spell_detail.append(spell_detail)

    blue_index['spells'] = all_spell_detail

    return blue_index

def display_notes(note_list:list, use_narrow_space:bool=True):
    # st.info('Blue Magic Tips')
    max_cols = MAIN_COL_COUNT
    if use_narrow_space:
        max_cols = SIDEBAR_COL_COUNT

    # col_count = len(note_list)
    if len(note_list) < max_cols:
        max_cols = len(note_list)
    
    info_cols = st.columns(max_cols)

    for idx, note in enumerate(note_list):
        use_col = info_cols[idx % max_cols]

        note_title = next(iter(note))

        use_col.text(note_title, help=note[note_title])
        
    return 

def monster_info(monster_dict:dict):
    monster_name = next(iter(monster_dict))
    monster_info = monster_dict[monster_name]

    return monster_name, monster_info

def format_blue_entry(row_data, idx_data:int=None, use_narrow_spacing:bool=True):
    with st.container():
        # Make sure we have an actual dict on our hands.
        if type(row_data['entry']) is str:
            row_data['entry'] = json.loads(row_data['entry'])

        blue_entry = row_data['entry']

        # Create a unified display name
        display_name = row_data['name']
        if 'Display Name' in blue_entry:
            display_name = blue_entry['Display Name']

        # Columns for the header info
        col1, col2, col3 = st.columns(3)

        col1.markdown(f'### {display_name}')
        if 'Alternate Name' in blue_entry:
            col2.caption('#### ' + blue_entry['Alternate Name'])
        else:
            col2.caption('')

        if blue_entry['FJF Recommended']:
            col3.markdown('#### :green[Good for FJF]')

        # Description
        st.info(blue_entry['Description'])

        # Larger detail information columns
        if use_narrow_spacing:
            detail_col1, detail_col2 = st.columns([3, 2], gap='medium')
        else:
            detail_col1, detail_col2 = st.columns(2, gap='medium')

        # List of stats
        stats = '- MP Cost: ' + str(blue_entry['MP Cost']) + '\n'
        if 'Spell Power' in blue_entry:
            stats += '- Spell Power: ' + str(blue_entry['Spell Power']) + '\n'

        detail_col1.markdown(stats)

        # Earliest Acquisition
        early_get_name, early_get_location = monster_info(blue_entry['Earliest Acquisition'])
        detail_col1.markdown(f'''
            **Earliest Acquisition:**
            - {early_get_name} - {early_get_location}
        ''')

        # Best Sources
        best_sources = '**Best Sources:** \n'
        for monster_entry in blue_entry['Best Source']:
            source_name, source_location = monster_info(monster_entry)
            best_sources += f'- {source_name} - {source_location}\n'
        detail_col1.markdown(best_sources)

        # Show all sources
        all_sources = '**Learned From:**\n'
        for monster_entry in blue_entry['Learned From']:
            if type(monster_entry) is dict:
                source_name, source_conditions = monster_info(monster_entry)
                all_sources += f'- {source_name} \n'
                for condition in source_conditions:
                    all_sources += f'  * {condition} \n'
            else:
                all_sources += f'- {monster_entry} \n'
        detail_col2.caption(all_sources)

        # Note text, if any
        if 'Note' in blue_entry:
            st.caption('Note: ' + blue_entry['Note'])

        # Warning text, if any
        if 'Warning' in blue_entry:
            st.warning('Warning: ' + blue_entry['Warning'])

        st.divider()

    return

def go(use_narrow_space:bool=True):
    st.title('!Blue Grimoire')

    blue_magic_lookup = blue_data()

    blue_df = pd.DataFrame.from_dict(blue_magic_lookup['spells'], orient='columns')

    # Blue search
    blue_search_value = st.text_input(
        'Search', 
        value='', 
        placeholder='Search Blue Spells', 
        label_visibility='collapsed', 
        help='Search blue magic for key terms or values'
    )

    # Show the Blue class notes.
    display_notes(blue_magic_lookup['Notes'], use_narrow_space)
    st.divider()

    if blue_search_value:
        blue_df = blue_df[blue_df.apply(lambda row: row.astype(str).str.contains(blue_search_value, case=False).any(), axis=1)]

    for idx, entry in blue_df.iterrows():
        format_blue_entry(entry, idx, use_narrow_space)

    st.markdown('Sources | [Blue Magic](' + blue_magic_lookup['sources']['Blue Magic'] + ') | [Bestiary](' + blue_magic_lookup['sources']['Bestiary'] + ')')
    
    return 

if __name__ == '__main__':
    st.set_page_config(
        page_title='Blue Resources',
        page_icon='👾',
        layout='centered',
    )
    use_sidebar = st.checkbox('Show in Sidebar', value=True)
    if st.button('Clear Cache'):
        st.cache_data.clear()
    if use_sidebar:
        with st.sidebar:
            go(use_sidebar)
    else:
        go(use_sidebar)
