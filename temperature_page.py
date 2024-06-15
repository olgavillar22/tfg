import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

from common_functions import *


@st.experimental_fragment
def plot_diff_floors_temperatura():
    diff_temp = pd.read_csv('temperaturefloordiff.csv')
    mean_monthly_temp = pd.read_csv('temperaturefloormean.csv')
    palette_plantes = alt.Scale(domain=[1, 2, 3, 4, 5, 6], range=['#2496cd', '#e52b50', '#3b7a57', '#ff8b00', '#804040', '#9932cc'])

    # Slider for the month
    slider_month = alt.binding_range(name='Month', min=1, max=12, step=1)
    selector_month = alt.selection_single(name="Select a month", fields=['Date'], bind=slider_month, init={'Date': 1})

    # Bar chart for temperature differences
    bar_chart = alt.Chart(diff_temp).mark_bar().encode(
        y=alt.Y('Planta:N', title='Floor', scale=alt.Scale(reverse=True)),
        x=alt.X('diff:Q', title='Temperature Difference (℃)', scale = alt.Scale(domain=[-1.1, 0.7])),
        color=alt.Color('Planta:N', scale=palette_plantes, title='Floors', legend = None),
    ).add_selection(selector_month).transform_filter(selector_month).properties(height = 200, title = 'Average difference between each floor temperature and the mean')

    bar_chart_means = alt.Chart(mean_monthly_temp).mark_bar(color = '#4a646c').encode(
        x=alt.X('Date:O', title = 'Month', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('mean_monthly_temp:Q', title ='Avg temperature (℃)'),
        opacity = alt.condition(selector_month, alt.value(1), alt.value(0.5))
    ).add_selection(selector_month).properties(height = 100, title = 'Average monthly temperature of all classrooms of building A')

    chart = bar_chart & bar_chart_means
    st.altair_chart(chart, use_container_width=True)


@st.experimental_fragment
def plot_floors_temp():
    temp = get_temperatureA_data()

    col1, col2 = st.columns(2)
    with col1:
        # Add groupby button custom
        select_groupby_var = get_time_groupby_selection('planta_temp')
        temp = groupby_time_planta(temp, select_groupby_var)
        temp['Date'] = temp['Date'].dt.to_timestamp()
    with col2:
        # Function to convert floor numbers to ordinal strings
        def ordinal(n):
            return "%d%s" % (n, "tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

        # Create a mapping for floor numbers to ordinal strings
        floor_mapping = {floor: ordinal(floor) for floor in temp['Planta'].unique()}

        # Map the floor numbers to ordinal strings
        temp['Planta_str'] = temp['Planta'].map(floor_mapping)

        # Multi-select for floor selection with ordinal labels
        selected_floors = st.multiselect(
            "Select Floors to Highlight",
            options=temp['Planta_str'].unique(),
            default=temp['Planta_str'].unique()
        )

    # Filter data based on selected time interval
    start_date, end_date = get_time_filter('planta_temp')
    filtered_data = temp[(temp['Date'] >= start_date) & (temp['Date'] <= end_date)]

    palette_plantes = alt.Scale(domain=[1, 2, 3, 4, 5, 6], range=['#2496cd', '#e52b50', '#3b7a57', '#ff8b00', '#804040', '#9932cc'])

    chart = alt.Chart(filtered_data).mark_line().encode(
        x = 'Date:T',
        y = alt.Y('avg_temp:Q', scale = alt.Scale(domain=[16, 32]), title = 'Temperature (℃)'),
        color=alt.Color('Planta:N', scale=palette_plantes, title='Plantes'),
        opacity=alt.condition(alt.FieldOneOfPredicate(field='Planta_str', oneOf=selected_floors), alt.value(1), alt.value(0.2))
    ).properties(title = 'Average temperature of the classes of different floors of building A')

    st.altair_chart(chart, use_container_width=True)


@st.cache_data
def plot_temperatura_aules():
    df = pd.read_csv('temperaturesubsampledETSAB2023_clean.csv')

    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
    color_palette = alt.Scale(domain=['Comfort', 'Too cold', 'Too warm'], range=['blue', '#77b5fe', '#c3272b'])

    chart = alt.Chart(df).mark_point(filled = True, size = 3).encode(
        x = 'Date:T',
        y = alt.Y('Temperatura:Q', title = 'Temperature (℃)'),
        color = alt.Color('Color:N', scale = color_palette),
        tooltip= ['Date','Temperatura','Aula']
    ).properties(
        title = 'Temperature of classes of building A with the comfort zone'
    )

    comfort = alt.Chart(df).mark_area(opacity = 0.3).encode(
        alt.X('Date:T'),
        alt.Y('min_comfort'),
        alt.Y2('max_comfort')
    )

    combined_chart = comfort + chart

    st.altair_chart(combined_chart, use_container_width=True)


@st.experimental_fragment
def heatmap_temperatures():
    sourcemonth = get_qualitataules_data()
    sourceyear = get_qualitataulesnovacation_data()

    groupby_options = ['Whole year', 'Group by month']
    select_radio = st.radio("Choose time aggregation:", groupby_options, key = "time_agg", horizontal = True)
    if select_radio == 'Whole year':
        source = sourceyear
    else:
        source = sourcemonth
        slider_month = alt.binding_range(name='Month', min=1, max=12, step=1)
        selector_month = alt.selection_single(name="Select a month", fields=['Month'], bind=slider_month, init={'Month': 1})
    col1, col2 = st.columns(2)

    with col1:
        # TEMPERATURA ALTA
        # Configure heatmap
        if select_radio == 'Whole year': #set a different domain
            heatmap = alt.Chart(source).mark_rect(color = 'red').encode(
                x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title = 'Floor'),
                color = alt.Color('temp_excessiva_alta:Q', scale=alt.Scale(scheme='reds'), title = '% Hours temperature higher than comfort')
            )
        else:
            heatmap = alt.Chart(source).mark_rect(color = 'red').encode(
                x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title = 'Floor'),
                color = alt.Color('temp_excessiva_alta:Q', scale=alt.Scale(scheme='reds', domain=[0,100]), title = '% Hours temperature higher than comfort')
            )

        # Configure text
        text = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title = 'Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        if select_radio == 'Whole year':
            chart1 = (heatmap + text)
        else:
            chart1 = (heatmap+text).add_selection(selector_month).transform_filter(selector_month)
        chart1 = chart1.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=11).properties(width = 250, height = 500, title = 'Percentage of times each class exceeded comfort temperature').configure_title(fontSize=14).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart1, use_container_width=True, theme='streamlit')

    with col2:
        # TEMPERATURA BAIXA
        # Configure heatmap
        if select_radio == 'Whole year': #set a different domain
            heatmap2 = alt.Chart(source).mark_rect(color = 'red').encode(
                x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title = 'Floor'),
                color = alt.Color('temp_excessiva_baixa:Q', title = '% Hours temperature lower than comfort')
            )
        else:
            heatmap2 = alt.Chart(source).mark_rect(color = 'red').encode(
                x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title = 'Floor'),
                color = alt.Color('temp_excessiva_baixa:Q', scale=alt.Scale(domain=[0,100]), title = '% Hours temperature lower than comfort')
            )

        # Configure text
        text2 = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title = 'Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        if select_radio == 'Whole year':
            chart2 = (heatmap2+text2)
        else:
            chart2 = (heatmap2 + text2).add_selection(selector_month).transform_filter(selector_month)
        chart2 = chart2.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=11).properties(width = 250, height = 500, title = 'Percentage of times each class fell down comfort temperature').configure_title(fontSize=14).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart2, use_container_width=True, theme='streamlit')



@st.experimental_fragment
def metrics_aules_temp():
    st.write('**Ranking: Temperature Statistics for Each Class**')

    # Load and preprocess the data
    aules_temp = get_tempaules_data()
    grouped_temp = aules_temp.groupby('Aula')['Temperatura'].agg(['mean', 'min', 'max']).round(2).reset_index()

    # Sorting options
    sort_order = st.selectbox("Sort order", ["Class position", "Colder to Warmer", "Warmer to Colder"])

    # Sort the DataFrame based on the user's selection
    if sort_order == "Colder to Warmer":
        grouped_temp = grouped_temp.sort_values(by='mean', ascending=True)
    elif sort_order == "Warmer to Colder":
        grouped_temp = grouped_temp.sort_values(by='mean', ascending=False)
    else:
        grouped_temp = grouped_temp.sort_values(by='Aula', ascending=True)


    # Display the metrics using st.expander to save space
    for _, row in grouped_temp.iterrows():
        aula = row['Aula']
        mean_temp = row['mean']
        min_temp = row['min']
        max_temp = row['max']

        with st.expander(f"Class: {aula}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Mean Temperature", value=f"{mean_temp}°C")
            with col2:
                st.metric(label="Min Temperature", value=f"{min_temp}°C")
            with col3:
                st.metric(label="Max Temperature", value=f"{max_temp}°C")


def violinplot_floors():
    df = pd.read_csv('temperatureETSAB2023_clean.csv')
    fig = px.violin(df, y="avg_temp", x="Planta", color="Planta", box=True, labels={'Planta':'Floor', 'avg_temp':'Temperature (℃)'})
    fig.update_layout(title_text="Distribution of temperature in the different floors of building A")
    # Remove the mode bar
    config = {
        'displayModeBar': False
    }

    st.plotly_chart(fig, config=config)


def main():
    # Title and Introduction
    st.markdown("<h2>Analysis of Classroom Temperatures</h2>", unsafe_allow_html=True)
    st.write("""
    In this section, we will analyze the temperature of classrooms in Building A at ETSAB. First, we'll examine the overall trends and then focus on differences between floors.
    """)

    # Global Temperature Analysis
    st.markdown("<h4 >Global Temperature Analysis</h4>", unsafe_allow_html=True)
    st.write('This chart shows the temperatures per hour of each class of Building A during 2023. The main objective is to know whether the classrooms have an optimal temperature for a work environment, that\'s why the blue zone (comfort) is highlighted, and points are classified into warm, comfort or cold temperatures.')
    st.write("""It's important to note that the temperature data in this plot has been subsampled to enhance performance. However, the subsampling has been done in a way to preserve the outliers and remove some of the central values for each time instant, in order to ensure that the data remains informative and interesting.""")
    plot_temperatura_aules()

    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>Classroom temperatures mostly fall outside the comfort zone.</li>
            <li>The temperature data shows clear seasonal variations, with temperatures rising above the comfort zone from June to October, indicating a warm problem in the periods where classes are being used.</li>
            <li>Colder months present more temperatures inside the comfort zone, despite some values are extremely far (like December 4 reaching 31.6℃ and March 5 lowering to 9.45℃).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Floor-wise Temperature Analysis
    st.markdown("<h4 >Floor-wise Temperature Analysis</h4>", unsafe_allow_html=True)
    st.write('In the following graphics, temperatures of the different floors will be compared to find differences and patterns.')
    st.write('This first chart shows the average temperature for each floor during the year. A specific time period and time aggregation can be selected in order to see different details in the data. Furthermore, a subset of floors to highlight can be selected to avoid the overlap.')
    plot_floors_temp()
     # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>The temperature trends across all floors are remarkably consistent, with similar peaks and troughs.</li>
            <li>In spite of all floors having similar average temperature, floor 1 is always colder than the others.</li>
    </div>
    """, unsafe_allow_html=True)
    st.write('Now, instead of only focusing on the average, we will compare the distribution of temperatures of each floor.')
    st.write('This violin plot shows the distribution of the data for each floor. Wider sections indicate a higher density of data points, while narrower sections indicate a lower density. The box inside shows the interquartile range and the line in the middle is the median temperature of each floor.')
    violinplot_floors()
     # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>All floors present similar temperature distributions, with peaks of density near 27℃ and 21℃.</li>
            <li>Floor 1 is slightly lower than the others, and floors 2 and 3 reach the highest maximum temperature.</li>
    </div>
    """, unsafe_allow_html=True)
    st.write('Instead of focusing on all year, let\'s analyse the difference of temperatures between floors for each month.')
    st.write('The following bar plot shows the average difference between the mean temperature per month of the building and of each floor. Each color bar is a different floor ordered like the building, and the second bar plot shows the montly average temperature value. There is a slider to select a month that filters the plots.')
    plot_diff_floors_temperatura()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>Floor 1 consistently has temperatures below the building's average across all months, while Floor 4 has always higher temperatures.</li>
            <li>The differences approximately range from 1 degree colder to 0.6 degrees warmer, with floors 1 and 6 showing the most oscillation.</li>
    </div>
    """, unsafe_allow_html=True)

    # Detailed Temperature Analysis
    st.markdown("<h4 >Temperature Quality Metric per Class</h4>", unsafe_allow_html=True)
    st.write('The heatmaps below show the percentage of hours in 2023 that each class\' temperature was higher or lower than the comfort zone. It allows you to see the whole year data, removing the vacation days and weekends, or see the montly data with a slider to select the month. Be careful with the color scale, as it changes when seeing the global year or monthly data, in order to be able to appreciate the variations between classes in the global data.')
    heatmap_temperatures()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>The lower floors in the building experience more cold, while the upper floors are warmer.</li>
            <li>Separating data per month changes a lot the localization of the most problematic classes. Meaning that a class being out of the comfort temperature does not remain constant during the whole year.</li>
    </div>
    """, unsafe_allow_html=True)
    metrics_aules_temp()

    # Additional Information Section
    st.write("""
        <div style="padding: 15px; margin-top: 20px;">
            <h4 style="color: gray;">Additional Information:</h4>
            <p style="color: gray;">In the temperature graphics, the vacation days are the ones where there's no class or activity for the students, as there's no usage of the classrooms. So, the following dates are excluded from the air quality analysis:
                <br>
                2023-09-25, 2023-10-12, 2023-11-01, 2023-12-06, 2023-12-07, 2023-12-08, 2023-12-23, 2023-12-24, 2023-12-25, 2023-12-26, 2023-12-27, 2023-12-28, 2023-12-29, 2023-12-30, 2023-12-31, 2023-01-01, 2023-01-02, 2023-01-03, 2023-01-04, 2023-01-05, 2023-01-06, 2023-01-07, 2023-01-08, 2023-01-09, 2023-01-10, 2023-04-01, 2023-04-02, 2023-04-03, 2023-04-04, 2023-04-05, 2023-04-06, 2023-04-07, 2023-04-08, 2023-04-09, 2023-04-10, 2023-05-01, 2023-09-11.
                <br>
                All August and July days and weekends are also excluded.
            </p>
        </div>
    """, unsafe_allow_html=True)
