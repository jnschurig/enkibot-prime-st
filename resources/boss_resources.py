import streamlit as st
import pandas as pd
import yaml
import os
try:
    import icon_lookup as icons
except:
    from resources import icon_lookup as icons

def load_yaml_data(file_name:str=None):

    # Need a non-relative path.
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, 'data', 'boss_detail')

    if file_name is None:
        yaml_file = os.path.join(data_dir, '_bosses.yml')
    else:
        yaml_file = os.path.join(data_dir, file_name)

    try:
        with open(yaml_file, 'r') as f:
            yaml_data = yaml.safe_load(f)
    except Exception as err:
        st.error(f'Unable to load file {yaml_file}')
        raise err

    return yaml_data

@st.cache_data
def fetch_boss_data():
    # Get the list of files to load
    boss_index = load_yaml_data()

    # Initialize some data objects
    all_boss_details = []
    boss_name_list = []

    # Iterate through each file, which represents a hint section
    for file_name in boss_index['bosses']:
        boss_detail = load_yaml_data(file_name)

        # We want to make sure things are formatted correctly, so check for the "Section" part.
        try:
            boss_name_list.append(boss_detail['Section'])
        except Exception as err:
            st.error(f'{file_name} missing or improperly formatted!')
            raise err

        # Some bosses have multiple parts, so we need to iterate through each of them.
        for idx, boss in enumerate(boss_detail['Bosses']):
            boss_name = next(iter(boss))
            # Return one row per boss part, so collect the inforation and later append to the list.
            boss_row = {
                'section_name': boss_detail['Section'],
                'boss_number': idx+1,
                'boss_name': boss_name,
                'boss_level': boss[boss_name]['Level']
            }

            # Check for optional elemental section and add it.
            element_icons = []
            if 'Elemental Weaknesses' in boss[boss_name]:
                for element in boss[boss_name]['Elemental Weaknesses']:
                    if element in icons.ELEMENTS:
                        element_icons.append(icons.ELEMENTS[element])
            boss_row['elements'] = element_icons

            # Check for optional status section and add it.
            status_icons = []
            if 'Vulnerable' in boss[boss_name]:
                for status in boss[boss_name]['Vulnerable']:
                    if status in icons.STATUSES:
                        status_icons.append(icons.STATUSES[status])
            boss_row['statuses'] = status_icons

            # Append the compiled row to the list.
            all_boss_details.append(boss_row)

    # Replace ugly file names with pretty section names.
    boss_index['bosses'] = boss_name_list

    # Convert the list object to a dataframe.
    all_boss_df = pd.DataFrame(all_boss_details)

    col_config = {
        'boss_name': 'Boss Name',
        'boss_level': st.column_config.NumberColumn('Level', help="The boss's level"),
        'statuses': st.column_config.ListColumn('Statuses', help=format_icon_legend('status')),
        'elements': st.column_config.ListColumn('Elements', help=format_icon_legend('element')),
        'boss_number': st.column_config.NumberColumn('Boss Number', help='Some bosses have more than one entity to fight. This number helps to identify each entity in the fight.'),
        'section_name': 'Hint Section'
    }

    return boss_index, all_boss_df, col_config

@st.cache_data
def format_icon_legend(icon_type:str='all'):
    # Takes the icon lookup data and formats it as a markdown-style list string.
    valid_icon_types = ['all', 'element', 'status']
    if icon_type is None or icon_type.lower() not in valid_icon_types:
        return None 
    
    icon_type = icon_type.lower()
    
    text_body = ''
    
    if icon_type in ['all', 'element']:
        for key in icons.ELEMENTS:
            val = icons.ELEMENTS[key]
            text_body += f'- {val} {key} \n'

    if icon_type in ['all', 'status']:
        for key in icons.STATUSES:
            val = icons.STATUSES[key]
            text_body += f'- {val} {key} \n'

    return text_body

# def display_sources(note_list:list, use_narrow_space:bool=True):

#     for idx, note in enumerate(note_list):
#         use_col = info_cols[idx % max_cols]

#         note_title = next(iter(note))

#         use_col.text(note_title, help=note[note_title])
        
#     return 
def go(show_json:bool=False):
    st.title('Boss Compendium')

    boss_index, boss_detail, col_config = fetch_boss_data()

    if show_json:
        st.json(boss_index, expanded=False)

    boss_search_value = st.text_input(
        'Search', 
        value='', 
        placeholder='Search Bosses', 
        label_visibility='collapsed', 
        help='Search boss data for key terms or values',
        # key=f'blue_search_{series_key}'
    )

    if boss_search_value:
        boss_detail = boss_detail[boss_detail.apply(lambda row: row.astype(str).str.contains(boss_search_value, case=False).any(), axis=1)]

    bosses_col, legend_col = st.columns([3, 1])

    with bosses_col:
        st.data_editor(
            boss_detail, 
            column_config=col_config, 
            disabled=True, 
            height=600, 
            hide_index=True,
            use_container_width=True,
        )

        st.caption('''* There may be listed here Hint Sections that do not actually exist. 
                This is to allow lookups of bosses that are not normally recommended for FJF.''')
        
        st.caption('''* If there are any inaccuracies or additions, feel free to contact me: @Reaif on Discord 
                   or email [jnschurig@gmail.com](mailto:jnschurig@gmail.com)''')
        
    with legend_col:
        st.markdown('#### Legend')
        st.markdown('Elements:\n' + format_icon_legend('element') + '\nStatuses:\n' + format_icon_legend('status'))

    with bosses_col:
        source_text = 'Sources:\n'
        for source in boss_index['sources']:
            source_name = next(iter(source))
            source_value = source[source_name]

            source_text += f'- [{source_name}]({source_value}) \n'

        st.caption(source_text)

    return boss_detail, col_config

if __name__ == '__main__':
    st.set_page_config(
        page_title='Boss Resources',
        page_icon='⚗️',
        layout='centered',
    )

    with st.sidebar:
        if st.button('Clear Cache'):
            st.cache_data.clear()

        # Display an easy legend I suppose.
        with st.expander('Legend', expanded=True):
            legend_col1, legend_col2 = st.columns(2)
            with legend_col1:
                st.markdown('Elements\n' + format_icon_legend('element'))
            with legend_col2:
                st.markdown('Statuses\n' + format_icon_legend('status'))

    if st.checkbox('Show in Sidebar', value=False):
        with st.sidebar:
            go()
    else:
        go()
