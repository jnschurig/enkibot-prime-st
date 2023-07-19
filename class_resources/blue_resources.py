import streamlit as st
import pandas as pd
import os

@st.cache_data
def fetch_blue_data():
    # Need a non-relative path.
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, 'data', 'mix_recipes.csv')
    return #pd.read_csv(csv_path, keep_default_na=False)

def go():
    st.title('!Blue Grimoire')

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
