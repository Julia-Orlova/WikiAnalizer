import streamlit as st
from main import task3a

st.set_page_config(page_title="Task3a")

st.markdown("# Task3.a. Retrieve a statistic of a particular user which include "
            "information about user contribution as a series of points over time.")

#username = "Bluejay14"
user = st.text_input('Enter a username:')
nums = int(st.number_input('Enter the number of days:', min_value=1, max_value=1000))

if st.button('Retrieve a statistic'):
    task3a(user, nums)

if st.button('Rerun script'):
    st.experimental_rerun()



