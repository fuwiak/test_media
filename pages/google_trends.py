import streamlit as st
import pandas as pd
# import plotly.express as px
from pytrends.request import TrendReq
from st_aggrid import GridOptionsBuilder, AgGrid

st.set_page_config(layout="centered", page_icon="🎓", page_title="AI")
st.title("Google Trends")

# Select date range
start_date, end_date = st.date_input('Select date range', [pd.to_datetime('2023-07-01'), pd.to_datetime('2023-07-30')])

# Convert date range to string format
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# Select language (English or Russian)
lang = st.selectbox("Select language", ("English", "Russian"))
if lang == "English":
    st.write("You selected English")
    pytrends = TrendReq(hl='en-US', tz=360)
else:
    st.write("You selected Russian")
    pytrends = TrendReq(hl='ru-RU', tz=360)

# Select keywords using multi-select
select_packages_kw = st.multiselect("Select keywords", ("machine learning", "artificial intelligence", "data science", "deep learning", "python"), default=("machine learning"))
kw_list = select_packages_kw

# # Build payload
# pytrends.build_payload(kw_list, cat=0, timeframe=f'{start_date_str} {end_date_str}')
#
# # 1 Interest over Time
# data = pytrends.interest_over_time()
# data = data.reset_index()
#
# # Plotting the data
# # fig = px.line(data, x="date", y=kw_list, title='Keyword Web Search Interest Over Time')
# # st.plotly_chart(fig, use_container_width=True)
#
# # Show related queries in Streamlit
# related_queries = pytrends.related_queries()
# for keyword in kw_list:
#     st.write(f"Top related queries for '{keyword}':")
#     AgGrid(related_queries[keyword]['top'])
#     st.write(f"Rising related queries for '{keyword}':")
#     AgGrid(related_queries[keyword]['rising'])
