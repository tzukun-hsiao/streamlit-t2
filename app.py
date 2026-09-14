import streamlit as st

page_1 = st.Page('pages/page_1.py')
page_2 = st.Page('pages/page_2.py')

pages = st.navigation([page_1, page_2])
pages.run()