import streamlit as st
from st_tasks import task2

st.set_page_config(page_title="Task2")

st.markdown("# Task2. Track in real time the activity of a particular user or a set of users")


users = st.text_input('Enter a user or a set of users (example: user1, user2, user3):')
users_to_track = users.split(', ')

if st.button('Start tracking'):
    task2(users_to_track)

if st.button('Rerun script'):
    st.experimental_rerun()



