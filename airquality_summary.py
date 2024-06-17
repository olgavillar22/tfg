import streamlit as st
import pandas as pd
import altair as alt

from common_functions import *

def heatmap_aules_quality_chart(source):
    col1, col2, col3 = st.columns(3)

    with col1:
        # TEMPERATURA
        # Configure heatmap
        heatmap = alt.Chart(source).mark_rect().encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            color = alt.Color('temp_excessiva:Q', scale = alt.Scale(scheme = 'reds', domain=[15,62]), title = '% of temperatures out of comfort')
        )

        # Configure text
        text = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        chart1 = heatmap + text
        chart1 = chart1.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = '% Class hours out of comfort temperature in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart1, use_container_width=True, theme='streamlit')

    with col2:
        # CO2
        # Configure heatmap
        heatmap2 = alt.Chart(source).mark_rect().encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            color = alt.Color('co2_excessiu:Q', scale=alt.Scale(scheme='greens',domain=[0,8]), title = '% of CO₂ out of comfort')
        )

        # Configure text
        text2 = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        chart2 = heatmap2 + text2
        chart2 = chart2.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = '% Class hours out of comfort CO₂ in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart2, use_container_width=True, theme='streamlit')

    with col3:
        # HHUMITAT
        # Configure heatmap
        heatmap3 = alt.Chart(source).mark_rect().encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            color = alt.Color('humitat_excessiva:Q', scale=alt.Scale(domain=[0,24.5]), title = '% of humidity out of comfort')
        )

        # Configure text
        text3 = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        chart3 = heatmap3 + text3
        chart3 = chart3.configure_legend(orient='bottom', labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = '% Class hours out of comfort humidity in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart3, use_container_width=True, theme='streamlit')

@st.experimental_fragment
def heatmap_aules_quality():
    groupby_options = ['All year', 'Q1 (september - january)', 'Q2 (february - june)']
    select_epoch_var= st.radio("Choose the time aggregation", groupby_options, key = "filter_epoch_heatmap", horizontal = True)

    if select_epoch_var == 'All year':
        source = get_qualitataulesnovacation_data()
    elif select_epoch_var == 'Q1 (september - january)':
        source = pd.read_csv('qualitat_aules_Q1.csv')
    else:
        source = pd.read_csv('qualitat_aules_Q2.csv')

    heatmap_aules_quality_chart(source)


@st.experimental_fragment
def heatmap_quality_metrics(source):
    col1, col2, col3 = st.columns(3)

    with col1:
        # TEMPERATURA
        # Configure heatmap
        heatmap = alt.Chart(source).mark_rect().encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            color = alt.Color('Temperature_Quality:Q', scale=alt.Scale(scheme='reds', domain=[0.12,0.32]), title = 'Ratio temperature deviation from comfort')
        )

        # Configure text
        text = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        chart1 = heatmap + text
        chart1 = chart1.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = 'Temperature deviation from comfort in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart1, use_container_width=True, theme='streamlit')

    with col2:
        # CO2
        # Configure heatmap
        heatmap2 = alt.Chart(source).mark_rect().encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            color = alt.Color('CO2_Quality:Q', scale=alt.Scale(scheme='greens', domain=[0,0.024]), title = 'Ratio of CO₂ deviation from comfort')
        )

        # Configure text
        text2 = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        chart2 = heatmap2 + text2
        chart2 = chart2.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = 'CO₂ deviation from comfort in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart2, use_container_width=True, theme='streamlit')

        with col3:
            # HHUMITAT
            # Configure heatmap
            heatmap3 = alt.Chart(source).mark_rect().encode(
                x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
                color = alt.Color('Humidity_Quality:Q', scale = alt.Scale(domain=[0,0.028]), title = 'Ratio of humidity deviation from comfort')
            )

            # Configure text
            text3 = alt.Chart(source).mark_text(baseline='middle').encode(
                x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
                text = alt.Text('Aula:N'),
            )

            # Draw the chart
            chart3 = heatmap3 + text3
            chart3 = chart3.configure_legend(orient='bottom', labelFontSize=10,titleFontSize=10).properties(width = 250, height = 500, title = 'Humidity deviation from comfort in 2023').configure_title(fontSize=13).configure_axis(labelFontSize=10,titleFontSize=10)
            st.altair_chart(chart3, use_container_width=True, theme='streamlit')


@st.experimental_fragment
def heatmap_aules_quality_metrics():
    groupby_options = ['All year', 'Q1 (september - january)', 'Q2 (february - june)']
    select_epoch_var= st.radio("Choose the time aggregation", groupby_options, key = "filter_epoch_heatmap2", horizontal = True)

    if select_epoch_var == 'All year':
        source = pd.read_csv('class_quality_measures.csv')
        heatmap_quality_metrics(source)

    elif select_epoch_var == 'Q1 (september - january)':
        source = pd.read_csv('class_quality_measuresQ1.csv')
        heatmap_quality_metrics(source)

    else:
        source = pd.read_csv('class_quality_measuresQ2.csv')
        heatmap_quality_metrics(source)


def main():
    st.markdown("<h2>Classroom Quality Metrics</h2>", unsafe_allow_html=True)
    st.write("""
    This section provides an overview of the air quality metrics for each classroom. We consider the percentage of hours each classroom is out of the comfort zone for various variables like temperature, humidity, and CO₂ concentrations.
    """)

    st.markdown("<h4 >Percentage of Class Hours Outside Comfort</h4>", unsafe_allow_html=True)
    st.write("""
    The heatmap below shows the percentage of hours each classroom is outside the comfort zone for each variable. It helps identify classrooms that consistently have poor air quality.
    """)
    heatmap_aules_quality()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>Temperature is the variable most frequently out of the comfort zone, with all classes experiencing deviations for 20% to 60% of the class hours.</li>
            <li>Each variable shows different patterns, there's no evidence in terms of overall air quality.</li>
            <li>First quarter has the highest percentage of class hours outside the comfort zone for all variables.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4 >Normalized Deviation from Comfort</h4>", unsafe_allow_html=True)
    st.write("""
    The next heatmap shows the normalized mean deviations from the comfort zone for each classroom and each variable. This metric provides a more nuanced view of how far the readings deviate from the optimal range.
    """)
    heatmap_aules_quality_metrics()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>The third floor has the worst quality classrooms in terms of temperature and CO₂ Concentration.</li>
            <li>Classroom A-36 deviates the most in temperature during the first quarter and is also one of the worst for CO₂ Concentration in the same period.</li>
            <li>A-31 has the highest CO₂ Concentration deviations from comfort in the first quarter. In the second quarter, A-33 is the most deviated for CO₂, while the others remain low deviated.
        </ul>
    </div>
    """, unsafe_allow_html=True)
