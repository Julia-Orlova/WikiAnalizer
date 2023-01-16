import streamlit as st
from st_tasks import task3b

st.set_page_config(page_title="Task3b")

st.markdown("# Task3.b. Retrieve a statistic of a particular user which include "
            "topics to which the user has contributed the most.")

if st.button('Rerun script'):
    st.experimental_rerun()
    
user = st.text_input('Enter a username:')
nums = int(st.number_input('Enter the number of days:', min_value=1, max_value=1000))

if st.button('Retrieve a statistic'):
    task3b(user, nums)
