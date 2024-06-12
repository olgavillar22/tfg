import streamlit as st

def main():
    html_temp = """
    <div style="background-color:gray;padding:0px">
    <h4 style="color:white;text-align:center;">HomePage</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    # Title and Introduction
    st.markdown("<h2>ETSAB Energy Consumption and Air Quality Analysis of 2023</h2>", unsafe_allow_html=True)
    st.write("""
    Welcome to the ETSAB Energy Consumption and Air Quality Analysis app. This application provides a visual analysis of the energy consumption and air quality data from various classrooms at ETSAB during the year 2023. The goal of this tool is to evaluate and draw conclusions about both the well-being of students and the sustainability of the campus, while providing an interface that allows for easy data analysis.
    """)

    # Overview of the Analysis
    st.markdown("<h4 style='color: #FF4B4B; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px'>Overview of the Analysis</h4>", unsafe_allow_html=True)
    st.write("""
    The analysis is divided into two main sections:

    - **Energy Consumption:** This section examines the energy usage of the three ETSAB buildings to identify patterns and potential areas for improvement in energy efficiency. Additionally, energy data is compared to the temperature of some classrooms to check for a relationship.
    - **Air Quality:** This larger section analyzes the air quality of classrooms in building A (Segarra) using data from their sensors. The analysis includes three variables: Temperature, CO₂ concentration, and humidity percentage. The section is further divided into five subsections:
        - **Temperature:** Analysis of temperature data to ensure a comfortable learning environment.
        - **CO₂ Concentration:** Monitoring CO₂ concentrations to assess air quality and ventilation effectiveness.
        - **Humidity:** Evaluating humidity percentages to maintain a healthy indoor climate.
        - **Detailed Classroom Comparison:** Obtain detailed data of the desired classes for all three variables.
        - **Quality Metrics Summary:** Get final quality metrics based on all three variables to evaluate and compare all the classes in building A.
    """)

    # Creator Information
    st.markdown("<h4 style='color: #FF4B4B; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px'>About the Creator</h4>", unsafe_allow_html=True)
    st.write("""
    This app was designed by Olga Villar Cairó as a final degree project for Data Science and Engineering in collaboration with Universitat Politècnica de Catalunya. The project aims to provide valuable insights into the environmental conditions of ETSAB's classrooms, contributing to the overall goal of enhancing student well-being and campus sustainability.
    """)
