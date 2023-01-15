import streamlit as st

st.set_page_config(
    page_title="Main",
)

st.markdown(
    """
    # WikiAnalyzer

    An integration and processing system for Wikipedia / Wikimedia.
    
    - Task1. Get all Recent Changes as a real-time stream
    - Task2. Track in real time the activity of a particular user or a set of users 
    - Task3. Retrieve a statistic of a particular user which include:
        * a. Information about user contribution as a series of points over time.
        * b. Topics to which the user has contributed the most
        * c. Type of contribution (typos editing | content addition). 
    - Task4. Retrieve the most active user during the (YEAR|MONTH|DAY)
    - Task5. Retrieve the top 10 topics which have the most number of typo editings
"""
)

if st.button("Rerun script"):
    st.experimental_rerun()