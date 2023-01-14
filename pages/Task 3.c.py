import streamlit as st
from main import task3c

st.set_page_config(page_title="Task3c")

st.markdown("# Task3.c. Retrieve a statistic of a particular user which include "
            "type of contribution (typos editing | content addition).")

if st.button('Rerun script'):
    st.experimental_rerun()

if st.button('Retrieve a statistic'):
    task3c()




