import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from streamlit_plotly_events import plotly_events


from common_functions import *

@st.experimental_fragment
def heatmap_aules_quality_chart(source):
    #source = source.groupby('Aula').mean().reset_index()
    col1, col2, col3 = st.columns(3)

    with col1:
        # TEMPERATURA
        # Configure heatmap
        heatmap = alt.Chart(source).mark_rect().encode(
            x=alt.X('posicio:O', title='Class position'),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            color = alt.Color('temp_excessiva:Q', title = 'Ratio of temperature deviation from comfort')
        )

        # Configure text
        text = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position'),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        chart1 = heatmap + text
        chart1 = chart1.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = '% Times out of comfort temperature in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart1, use_container_width=True, theme='streamlit')

    with col2:
        # CO2
        # Configure heatmap
        heatmap2 = alt.Chart(source).mark_rect().encode(
            x=alt.X('posicio:O', title='Class position'),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            color = alt.Color('co2_excessiu:Q', title = 'Ratio of CO₂ deviation from comfort')
        )

        # Configure text
        text2 = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position'),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        chart2 = heatmap2 + text2
        chart2 = chart2.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = '% Times out of comfort CO₂ in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart2, use_container_width=True, theme='streamlit')

    with col3:
        # HHUMITAT
        # Configure heatmap
        heatmap3 = alt.Chart(source).mark_rect().encode(
            x=alt.X('posicio:O', title='Class position'),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            color = alt.Color('humitat_excessiva:Q', title = 'Ratio of humidity deviation from comfort')
        )

        # Configure text
        text3 = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position'),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        chart3 = heatmap3 + text3
        chart3 = chart3.configure_legend(orient='bottom', labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = '% Times out of comfort humidity in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart3, use_container_width=True, theme='streamlit')

@st.experimental_fragment
def heatmap_aules_quality():
    groupby_options = ['All year', 'Q1 (september - january)', 'Q2 (february - june)']
    select_epoch_var= st.radio("Choose the time aggregation", groupby_options, key = "filter_epoch_heatmap", horizontal = True)

    if select_epoch_var == 'All year':
        source = pd.read_csv('/home/olga/Desktop/tfg/qualitat_aules_globalnovacation.csv')
        heatmap_aules_quality_chart(source)

    elif select_epoch_var == 'Q1 (september - january)':
        source = pd.read_csv('/home/olga/Desktop/tfg/qualitat_aules_Q1.csv')
        heatmap_aules_quality_chart(source)

    else:
        source = pd.read_csv('/home/olga/Desktop/tfg/qualitat_aules_Q2.csv')
        heatmap_aules_quality_chart(source)


    #chart = alt.hconcat(chart1, chart2, chart3).resolve_scale(color='independent').configure_legend(orient='bottom').properties(title = '# times exceeding comfort in 2023')


    #st.altair_chart(chart, use_container_width=True, theme='streamlit')

@st.experimental_fragment
def heatmap_quality_metrics(source):
    col1, col2, col3 = st.columns(3)

    with col1:
        # TEMPERATURA
        # Configure heatmap
        heatmap = alt.Chart(source).mark_rect().encode(
            x=alt.X('posicio:O', title='Class position'),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            color = alt.Color('Temperature_Quality:Q', title = 'Ratio of temperature deviation from comfort')
        )

        # Configure text
        text = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position'),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        chart1 = heatmap + text
        chart1 = chart1.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = 'Quality of classes based on temperature in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart1, use_container_width=True, theme='streamlit')

    with col2:
        # CO2
        # Configure heatmap
        heatmap2 = alt.Chart(source).mark_rect().encode(
            x=alt.X('posicio:O', title='Class position'),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            color = alt.Color('CO2_Quality:Q', title = 'Ratio of CO₂ deviation from comfort')
        )

        # Configure text
        text2 = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position'),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        chart2 = heatmap2 + text2
        chart2 = chart2.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = 'Quality of classes based on CO₂ in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart2, use_container_width=True, theme='streamlit')

        with col3:
            # HHUMITAT
            # Configure heatmap
            heatmap3 = alt.Chart(source).mark_rect().encode(
                x=alt.X('posicio:O', title='Class position'),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
                color = alt.Color('Humidity_Quality:Q', title = 'Ratio of humidity deviation from comfort')
            )

            # Configure text
            text3 = alt.Chart(source).mark_text(baseline='middle').encode(
                x=alt.X('posicio:O', title='Class position'),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
                text = alt.Text('Aula:N'),
            )

            # Draw the chart
            chart3 = heatmap3 + text3
            chart3 = chart3.configure_legend(orient='bottom', labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = 'Quality of classes based on humidity in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
            st.altair_chart(chart3, use_container_width=True, theme='streamlit')


@st.experimental_fragment
def heatmap_aules_quality_metrics():
    groupby_options = ['All year', 'Q1 (september - january)', 'Q2 (february - june)']
    select_epoch_var= st.radio("Choose the time aggregation", groupby_options, key = "filter_epoch_heatmap2", horizontal = True)

    if select_epoch_var == 'All year':
        source = pd.read_csv('/home/olga/Desktop/tfg/class_quality_measures.csv')
        heatmap_quality_metrics(source)

    elif select_epoch_var == 'Q1 (september - january)':
        source = pd.read_csv('/home/olga/Desktop/tfg/class_quality_measuresQ1.csv')
        heatmap_quality_metrics(source)

    else:
        source = pd.read_csv('/home/olga/Desktop/tfg/class_quality_measuresQ2.csv')
        heatmap_quality_metrics(source)


def main():
    st.markdown("<h2>Classroom Quality Metrics</h2>", unsafe_allow_html=True)
    st.write("""
    This section provides an overview of the air quality metrics for each classroom. We consider the percentage of hours each classroom is out of the comfort zone for various variables like temperature, humidity, and CO₂ levels.
    """)

    st.write("""
    The heatmap below shows the percentage of hours each classroom is outside the comfort zone for each variable. It helps identify classrooms that consistently have poor air quality.
    """)
    heatmap_aules_quality()

    st.write("""
    The next heatmap shows the normalized mean deviations from the comfort zone for each classroom and each variable. This metric provides a more nuanced view of how far the readings deviate from the optimal range.
    """)
    heatmap_aules_quality_metrics()
