import temperature_page
import co2_page
import humidity_page
import global_classroom
import airquality_summary
import streamlit as st


def main():
    html_temp = """
    <div style="background-color:gray;padding:0px">
        <h4 style="color:white;text-align:center;">Air Quality</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    st.markdown("<h2>Air quality analysis of Building A Classrooms</h2>", unsafe_allow_html=True)

    st.write("""
    In this section, you will find an analysis of various air quality parameters in the classrooms at ETSAB. The results are encapsulated in different tabs, which you can access by clicking on each of them.
    """)

    temp, co2, hum, classs, summary = st.tabs(['Temperature', 'Concentration of CO2', 'Percentage of humidity', 'Detailed classroom comparison', 'Quality metrics summary'])

    with temp:
        temperature_page.main()

    with co2:
        co2_page.main()

    with hum:
        humidity_page.main()

    with classs:
        global_classroom.main()

    with summary:
        airquality_summary.main()
