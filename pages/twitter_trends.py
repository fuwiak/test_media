import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import snscrape.modules.twitter as sntwitter

st.set_page_config(layout="centered", page_icon="🎓", page_title="AI")
st.title("Twitter Analysis")

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

# query = "Kazachstan until:2022-01-01 since:2021-01-01"

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


#run button
if st.button("Run"):
    tweets_list2 = []
    #show query
    st.write(query)
    try:
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i>limit:
                break
            tweets_list2.append([tweet.date, tweet.content, tweet.user.username])

        # Creating a dataframe from the tweets list above
        global tweets_df2
        tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Text', 'Username'])

        # Display first 5 entries from dataframe
        st.write(tweets_df2.head())
        show_table_grid(tweets_df2)
        #st balloons
        st.balloons()
    except:
        st.write("No tweets found")
        st.stop()


