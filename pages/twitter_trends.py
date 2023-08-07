import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import snscrape.modules.twitter as sntwitter
from tweety import Twitter
import pandas as pd

st.set_page_config(layout="centered", page_icon="🎓", page_title="AI")
st.title("Keyword Twitter Analysis")

if st.button("Reset"):
    st.experimental_rerun()

#reset IP address to avoid getting banned streamlit

st.write("Enter the keyword you want to search for")
keyword = st.text_input("Keyword", "bitcoin")

st.write("Enter the number of tweets you want to search for")
limit = st.number_input("Limit", 5)
#select lang and date range buttons
st.write("Select the language of the tweets you want to search for")
lang = st.radio("Language", ("en", "ru"))
st.write("Select the date range of the tweets you want to search for")
start_date = st.date_input("Start date", value=None, min_value=None, max_value=None, key=None)
end_date = st.date_input("End date", value=None, min_value=None, max_value=None, key=None)

query = keyword + f" lang:{lang} until:{end_date} since:{start_date}"


def show_table_grid(data):
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()
    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        enable_enterprise_modules=True,
        height=350,
        width='100%',
        reload_data=True
    )
    return grid_response


def fetch_tweets(query: str, limit: int = 100) -> pd.DataFrame:
    """
    Fetch tweets based on a query up to a given limit.

    Parameters:
    - query (str): Query string for the tweets search.
    - limit (int): Maximum number of tweets to return.

    Returns:
    - pd.DataFrame: DataFrame containing fetched tweets' datetime, text, and username.
    """
    tweets_list = []
    try:
        for i, tweet in enumerate(
                sntwitter.TwitterSearchScraper(query).get_items()):
            if i > limit:
                break
            tweets_list.append(
                [tweet.date, tweet.content, tweet.user.username])
        tweets_df = pd.DataFrame(tweets_list,
                                 columns=['Datetime', 'Text', 'Username'])
        return tweets_df
    except Exception as e:
        # st.write(e)
        st.write("No tweets found")
        st.stop()


if st.button("Run"):
    # Show query
    st.write(query)
    try:
        tweets_df2 = fetch_tweets(query)
        # Display first 5 entries from dataframe
        st.write(tweets_df2.head())
        show_table_grid(tweets_df2)
        # Show balloons
        st.balloons()
    except Exception as e:
        st.write(e)
        st.write("No tweets found")
        st.stop()

st.markdown(""" # Get posts from a specific user""")
st.write("Enter the username you want to search for")
username = st.text_input("Username", "elonmusk")

def fetch_and_print_tweets(username: str) -> dict:
    app = Twitter("session")

    # Fetch tweets
    all_tweets = app.get_tweets(username)
    tweets = pd.DataFrame(list(all_tweets))
    return tweets

if st.button("Find tweets for a specific user"):
    try:
        tweets = fetch_and_print_tweets(username)
        st.write(tweets)
        show_table_grid(tweets)
        # Show balloons
        st.balloons()
    except Exception as e:
        st.write(e)
        st.write("No tweets found")
        st.stop()
