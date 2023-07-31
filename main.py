import streamlit as st
import pandas as pd
from dataframes import parse_posts, get_comments, get_members
from dataclasses import dataclass
import nltk
import re
from googlesearch import search

from sklearn.pipeline import Pipeline

import warnings
warnings.filterwarnings("ignore")

from st_pages import Page, show_pages, add_page_title
from utils import load_data, save_dataframe


@st.cache_data
def convert_df(df=None):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def resolve_url(url, vk):
    screen_name = url.split('/')[-1]
    try:
        ids = vk.utils.resolveScreenName(screen_name=screen_name)
        return ids['object_id']
    except Exception as e:
        print(e)
        return None

st.session_state['df'] = None
st.session_state['posts'] = None
st.session_state['members'] = None
st.session_state['comments'] = None
st.session_state['labels'] = None
st.session_state['group_name'] = None

def main():
    st.set_page_config(layout="wide")
    st.sidebar.title("Social Media Analysis")
    st.sidebar.markdown("This application allows you to analyze posts, comments, and members of social media groups.")
    #change name of the page
    st.sidebar.title("Choose a Page")

    with st.sidebar:
        count = st.text_input("Enter the number of posts:", value=10)
        user_input = st.text_input("Enter of query:", value="Politics")




    if st.sidebar.button("Save Data"):
        pass

    data = search(user_input, tld='co.in', lang='en', num=int(count), start=0, stop=int(count), pause=2)
    for url in data:
        st.write(url)


if __name__ == '__main__':


    main()


