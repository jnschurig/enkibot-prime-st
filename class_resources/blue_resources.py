import streamlit as st
import pandas as pd
import yaml
import os

def scan_yaml_dir(directory_path:str):
    file_list = os.listdir(directory_path)

    # st.write(file_list)

    all_spell_detail = {}

    for file in file_list:
        if file[0:1] == '_':
            # Skip this file...
            continue
        qualified_path = os.path.join(directory_path, file)

        with open(qualified_path, 'r') as f:
            spell_detail= yaml.safe_load(f)

        all_spell_detail.update(spell_detail)

        # st.write(spell_detail)
        

    return all_spell_detail

@st.cache_data
def fetch_blue_data():
    
    # Need a non-relative path.
    script_dir = os.path.dirname(__file__)
    # csv_path = os.path.join(script_dir, 'data', 'mix_recipes.csv')
    blue_dir = os.path.join(script_dir, 'data', 'blue_magic')
    blue_start_file = os.path.join(blue_dir, '_grimoire.yml')

    with open(blue_start_file, 'r') as f:
        root_file_data = yaml.safe_load(f)


    all_file_data = scan_yaml_dir(blue_dir)
    # st.json(all_file_data)

    return root_file_data, all_file_data

def go():
    st.title('!Blue Grimoire')

    the_data = fetch_blue_data()
    st.json(the_data)

    return 

if __name__ == '__main__':
    st.set_page_config(
        page_title='Blue Resources',
        page_icon='👾',
        layout='centered',
    )

    if st.checkbox('Show in Sidebar', value=True):
        with st.sidebar:
            go()
    else:
        go()
