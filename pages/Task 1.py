import streamlit as st
from main import task1

st.set_page_config(page_title="Task1")

st.markdown("# Task1. Get all Recent Changes as a real-time stream")

if st.button('Rerun script'):
    st.experimental_rerun()

if st.button('Get all Recent Changes as a real-time stream'):
    task1()




