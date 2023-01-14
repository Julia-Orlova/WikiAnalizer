import streamlit as st
from main import task4

st.set_page_config(page_title="Task4")

st.markdown("# Task4. Retrieve the most active user during the (YEAR|MONTH|DAY)")

if st.button('Rerun script'):
    st.experimental_rerun()

startB = st.button('Retrieve the most active user')
if startB:
    task4()
    startB = False





