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


def get_energy_data(festius = True):
    energia = pd.read_csv('/home/olga/Desktop/tfg/energia_activaETSAB2023_clean.csv')
    if not festius:
        energia = energia[energia['festiu'] == False]

    energia['CS B elec [kWh] [ETSAB]'] = pd.to_numeric(energia['CS B elec [kWh] [ETSAB]'], errors='coerce')
    energia = energia.rename(columns = {'CS B elec [kWh] [ETSAB]': 'CS B', 'CS A elec [kWh] [ETSAB]': 'CS A', 'CS C elec [kWh] [ETSAB]': 'CS C', 'Electricitat Total [kWh] [ETSAB]': 'Electricitat Total'})
    energia['Date'] = pd.to_datetime(energia['Date'], format='%Y-%m-%d %H:%M:%S')

    return energia


def plot_energia_total():
    energia_total = 854543.41
    energiaA = 486078.51 * 100 / energia_total
    energiaB = 143444.78 * 100 / energia_total
    energiaC = 225037.85 * 100 / energia_total

    # Prepare the dataframe
    df = pd.DataFrame({
        'Percentage': [energiaA, energiaB, energiaC],
        'Building': ['A (Segarra)', 'B', 'C (Codach)']
    })

    # Define the color palette
    color_palette = alt.Scale(domain=['A (Segarra)', 'B', 'C (Codach)'],
                              range=['#318ce7', '#1cac78', '#ad4379'])

    # Create the pie chart
    pie_chart = alt.Chart(df).mark_arc().encode(
        theta=alt.Theta(field='Percentage', type='quantitative'),
        color=alt.Color(field='Building', type='nominal', scale=color_palette),
        tooltip=['Building:N', 'Percentage:Q']
    ).properties(
        width = 350
    )
    st.write('**Distribution of energy consumption between buildings**')
    # Display the chart in Streamlit
    st.altair_chart(pie_chart)


@st.experimental_fragment
def plot_energia():
    start_date, end_date = get_time_filter('energy')

    col1, col2 = st.columns(2)
    with col1:
        select_groupby_var = get_time_groupby_selection('energy')
    with col2:
        select_vacation = get_festius_energy_selection('energy')

    if select_vacation == 'Show vacation days':
        energia = get_energy_data(festius = True)
    else:
        energia = get_energy_data(festius = False)

    energia = groupby_time(energia, select_groupby_var)
    energia['Date'] = energia['Date'].dt.to_timestamp()

    # Filter data based on selected time interval
    filtered_data = energia[(energia['Date'] >= start_date) & (energia['Date'] <= end_date)]

    # Melt the dataframe to long format for easier plotting with Altair
    energia_melted = energia.melt('Date', var_name='Edifici', value_name='Value')

    # Filter the data to include only the relevant categories
    filtered_energia = energia_melted[energia_melted['Edifici'].isin(['CS A', 'CS B', 'CS C', 'Electricitat Total'])]

    # Define a selection that can be empty
    selection = alt.selection_multi(fields=['Edifici'], bind='legend', init=[{'Edifici': 'CS A'}, {'Edifici': 'CS B'}, {'Edifici': 'CS C'}, {'Edifici': 'Electricitat Total'}])

    color_palette = alt.Scale(domain=['CS A', 'CS B', 'CS C', 'Electricitat Total'], range=['#318ce7', '#1cac78', '#ad4379', '#da9100'])

    # Create the line chart with selection
    chart = alt.Chart(filtered_energia).mark_line().encode(
        x='Date:T',
        y='Value:Q',
        color = alt.Color('Edifici:N', scale=color_palette),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        tooltip=[alt.Tooltip('Date:T', title='Date'), alt.Tooltip('Value:Q', title='Value'), alt.Tooltip('Edifici:N', title='Edifici')]
    ).add_selection(
        selection
    ).properties(
        width=800,
        height=400,
        title="Energy consumption of ETSAB in 2023"
    )

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)


@st.experimental_fragment
def plot_temp_energy():
    # PB: HEM FILTRAT NO WEEKENDS EN ENERGIA PERÒ EN TEMP SI Q HI SON
    campus_temp = pd.read_csv('/home/olga/Desktop/tfg/tempCAMPUS2023_clean.csv')
    campus_temp['Date'] = pd.to_datetime(campus_temp['Date'], format='%Y-%m-%d %H:%M:%S')

    #select_vacation = get_festius_energy_selection('entemp')
    #if select_vacation == 'Mostra els festius':
    energia = get_energy_data(festius = True)
    #else:
    #    energia = get_energy_data(festius = False)
    # en aquest plot ens interessa eliminar si o si els caps de setmana --> NO SÉ SI CAL FILTRE DE VACANCES el trec
    energia = energia[energia['is_weekend']==False]

    class_temp = get_temperatureA_data()

    #PROVISIONAL GROUP BY
    campus_temp = campus_temp.groupby(campus_temp['Date'].dt.to_period('d')).mean().reset_index()
    class_temp = class_temp.groupby(class_temp['Date'].dt.to_period('d')).mean().reset_index()
    # add class temp to campus temp df to have it all in one df (without the Planta)
    temps = campus_temp.merge(class_temp[['Date', 'avg_temp']], on='Date')
    # From period type Date to datetime (period --> string --> datetime)
    temps['Date'] = temps['Date'].astype(str)
    temps['Date'] = pd.to_datetime(temps['Date'])
    energia = energia.groupby(energia['Date'].dt.to_period('d')).mean().reset_index()
    energia['Date'] = energia['Date'].astype(str)
    energia['Date'] = pd.to_datetime(energia['Date'])

    # Temperature chart with area and lines
    temperature_area = alt.Chart(temps).mark_area(opacity=0.5).encode(
        x='Date:T',
        y=alt.Y('avg_temp:Q', title='Temperature (℃)'),
        y2='Temperatura Campus Sud:Q',
        color=alt.value('lightblue'),
        tooltip=['Date:T', 'avg_temp:Q', 'Temperatura Campus Sud:Q']
    )

    line_indoor = alt.Chart(temps).mark_line(color='blue', opacity=0.5).encode(
        x='Date:T',
        y='avg_temp:Q',
        tooltip=['Date:T', 'avg_temp:Q']
    )

    line_outdoor = alt.Chart(temps).mark_line(color='green', opacity=0.5).encode(
        x='Date:T',
        y='Temperatura Campus Sud:Q',
        tooltip=['Date:T', 'Temperatura Campus Sud:Q']
    )

    # Combine the temperature charts
    temperature_chart = alt.layer(
        temperature_area,
        line_indoor,
        line_outdoor
    ).resolve_scale(
        y='shared'
    ).properties(
        width=900,  # Width adjusted for larger display
        height=400,
        title='Temperature and Energy Consumption'
    )

    # Energy consumption chart
    energy_chart = alt.Chart(energia).mark_line(color='red').encode(
        x='Date:T',
        y=alt.Y('Electricitat Total:Q', axis=alt.Axis(title='Energy Consumption (kWh)', titleColor='red', orient='right')),
        tooltip=['Date:T', 'Electricitat Total:Q']
    ).properties(
        width=900,  # Width adjusted for larger display
        height=400
    )

    # Combine the charts with independent y-axes
    combined_chart = alt.layer(
        temperature_chart,
        energy_chart
    ).resolve_scale(
        y='independent'
    ).properties(
        width=900,  # Width adjusted for larger display
        height=400,
        title='Temperature and Energy Consumption'
    )

    # Display the combined chart and explanation text
    st.altair_chart(combined_chart, use_container_width=True)

@st.experimental_fragment
def plot_week_seasonal_energy_trend():
    energia = pd.read_csv('/home/olga/Desktop/tfg/energia_seasonalETSAB2023_clean.csv')
    color_palette = alt.Scale(domain=['Autumn', 'Winter', 'Spring', 'Summer', 'Vacation'], range=['#996600', '#4997d0', '#3cd070', '#f5c71a', '#ff55a3'])

    building_options = ['A (Segarra)', 'B', 'C (Codach)', 'Total']
    select_building = st.radio("Choose building:", building_options, key = "filter_building_seasonal", horizontal = True)

    # Map building names to corresponding variables
    building_variable_mapping = {
        'A (Segarra)': 'CS A',
        'B': 'CS B',
        'C (Codach)': 'CS C',
        'Total': 'Electricitat Total'
    }

    building_variable = building_variable_mapping[select_building]

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    chart = alt.Chart(energia).mark_line().encode(
        x=alt.X('hour_of_day:O', title='hour of the day'),
        y=alt.Y(building_variable + ':Q'),  # Dynamically change the variable based on the selected building
        color=alt.Color('season:N', scale=color_palette)
    ).properties(
        width=150,
        height=200
    ).facet(
        column=alt.Column('day_of_week:N', sort=day_order, title='day of week'),  # Sort days of the week
        title=f'Energy Consumption of {select_building} by Season for Each Day of the Week',
        spacing=0
    )

    st.altair_chart(chart, use_container_width=True)



def main():
    # HTML for the header
    html_temp = """
    <div style="background-color:gray;padding:0px">
    <h4 style="color:white;text-align:center;">Energy Consumption</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    # Introduction
    st.markdown("<h2>Energy Consumption Analysis of ETSAB Buildings in 2023</h2>", unsafe_allow_html=True)
    st.write("""
    In this section, the energy consumption of the ETSAB buildings during 2023 will be analyzed using data from the energy meters. The ETSAB has three buildings: A (Segarra), B, and C (Codach). It is worth mentioning that the energy consumption of building A only refers to the lighting mechanism, as the heating works by gas, while the consumption in the other buildings includes heating.
    """)

    # Initial Analysis
    st.markdown("<h4 >Initial Analysis</h4>", unsafe_allow_html=True)
    st.write("""To start, we'll take a look at the evolution of energy consumption in 2023 comparing the three buildings. For better understanding, you can adjust the time aggregation to see more or less detailed data. Additionally, softening the vacation days ensures that they do not alter the global trend. So, the softening button removes the weekends and vacation days data, which are specified in the Additional Information section at the end of the page, so that the chart autocompletes them continuing the line of the labor days. Furthermore, you can filter the start and end dates of the period you want to examine in detail.
    """)
    plot_energia()
    # Map and Pie chart of Energy Consumption
    col1, col2 = st.columns(2)
    with col1:
        st.write('**Map of ETSAB Buildings**')
        st.image('/home/olga/Desktop/tfg/Situació campus sud-set 2017-Modelo_page-0001.jpg', width=400)
    with col2:
        plot_energia_total()

    st.write('**Total energy consumption in 2023**')
    col1, col2 = st.columns(2)
    #Some KPIS
    with col1:
        st.metric(label="Energy Consumption of Building A in 2023", value="486078.51 kWh")
        st.metric(label="Energy Consumption of Building C in 2023", value="225037.85 kWh")

    with col2:
        st.metric(label="Energy Consumption of Building B in 2023", value="143444.78 kWh")
        st.metric(label="Total ETSAB Energy Consumption in 2023", value="854543.41 kWh")

    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways:</h4>
        <ul>
            <li>Despite building A electricity is only consumed by lightening and not heating, it is the most consuming building among all.</li>
            <li>A clear decrease on weekends and vacation days can be observed, proportionally to the normal consumption of each building.</li>
            <li>Buildings A and C present a decrease of energy consumption in warm months, while B remains practically constant (with exception of August).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Consumption Patterns
    st.markdown("<h4 >Seasonal Consumption Patterns</h4>", unsafe_allow_html=True)
    st.write("""
    Now, we'll analyze the consumption pattern of each working day for every building, considering the different seasons of the year. In this chart, vacation days are separated from labor ones in order to see the patterns without distortion. These exceptional dates are specified in the Additional Information section.
    """)
    plot_week_seasonal_energy_trend()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways:</h4>
        <ul>
            <li>In vacation and Summer days, a huge decrease of consumption can be appreciated in all the buildings. </li>
            <li>...</li>
            <li>...</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Temperature and Energy Relationship
    st.markdown("<h4 >Temperature and Energy Relationship</h4>", unsafe_allow_html=True)
    st.write("""
    Let's explore the relationship between temperature and energy consumption and check whether they are correlated. In this plot, at the right axis there's the total energy consumption (all buildings included) while the left one represents indoor and outdoor temperatures. The green line is the outdoor temperature of the campus, the blue one is the mean temeprature of all classes of building A, and the shaded area represents the difference between indoor and outdoor temperatures.
    """)
    plot_temp_energy()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways:</h4>
        <ul>
            <li>It can clearly be seen that as more difference of indoor-outdoor temperature, more energy consumption. </li>
            <li>it is curious to see that the mean temperature indoors is always highest than the outdoors temperature.</li>
            <li>...</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Additional Information Section
    st.write("""
        <div style="padding: 15px; margin-top: 20px;">
            <h4 style="color: gray;">Additional Information:</h4>
            <p style="color: gray;">In the energy graphics, the vacation days are the ones where the campus is completely closed, as there's no consumption. So, the following dates are excluded from the energy consumption analysis:
                <br>
                2023-09-25, 2023-10-12, 2023-11-01, 2023-12-06, 2023-12-07, 2023-12-08, 2023-12-23, 2023-12-24, 2023-12-25, 2023-12-26, 2023-12-27, 2023-12-28, 2023-12-29, 2023-12-30, 2023-12-31, 2023-01-01, 2023-01-02, 2023-01-03, 2023-01-04, 2023-01-05, 2023-01-06, 2023-01-07, 2023-01-08, 2023-01-09, 2023-01-10, 2023-04-01, 2023-04-02, 2023-04-03, 2023-04-04, 2023-04-05, 2023-04-06, 2023-04-07, 2023-04-08, 2023-04-09, 2023-04-10, 2023-05-01, 2023-09-11.
                <br>
                All August days and weekends are also excluded.
            </p>
        </div>
    """, unsafe_allow_html=True)
