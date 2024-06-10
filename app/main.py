import streamlit as st
import pandas as pd

import temperature_page
import energy_page
import homepage
import co2_page
import humidity_page
import airquality_page

def main():
    st.set_page_config(layout="wide")
    PAGES = {
        "Homepage": homepage,
        "Energy consumption": energy_page,
        "Air quality": airquality_page
    }

    st.sidebar.title('Navigation')

    # CSS to style the navigation boxes and text
    st.markdown(
        """
        <style>
        .nav-box {
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            text-align: center;
            color: white;
        }
        .nav-box:hover {
            background-color: #6c757d;
        }
        .nav-box-active {
            background-color: #343a40;
        }
        .nav-box-inactive {
            background-color: #495057;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create clickable navigation boxes
    for page_name, page in PAGES.items():
        if st.sidebar.button(page_name):
            st.session_state.current_page = page_name

    # Default to the first page if no page is selected
    if 'current_page' not in st.session_state:
        st.session_state.current_page = list(PAGES.keys())[0]

    # Display the current page
    current_page = st.session_state.current_page
    #st.markdown(f'<div class="nav-box nav-box-active">{current_page}</div>', unsafe_allow_html=True)

    # Render the selected page's content
    PAGES[current_page].main()

main()
