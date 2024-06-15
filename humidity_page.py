import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

from common_functions import *


def plot_humidity_aules():
    aules_hum = pd.read_csv('humiditysubsampledETSAB2023_clean.csv')

    aules_hum['Date'] = pd.to_datetime(aules_hum['Date'], format='%Y-%m-%d %H:%M:%S')
    color_palette = alt.Scale(domain=['Comfort', 'Too humid', 'Too dry'], range=['blue', '#c3272b', '#77b5fe'])

    chart = alt.Chart(aules_hum).mark_point(filled = True, size = 3).encode(
        x = 'Date:T',
        y = alt.Y('Humidity:Q', title = 'Humidity (%)'),
        color = alt.Color('Color:N', scale = color_palette),
        tooltip= ['Date','Humidity','Aula']
    ).properties(
        title = 'Humidity of classes of building A with the comfort zone'
    )

    comfort = alt.Chart(aules_hum).mark_area(opacity = 0.3).encode(
        alt.X('Date:T'),
        alt.Y('min_humidity'),
        alt.Y2('max_humidity')
    )

    combined_chart = comfort + chart

    st.altair_chart(combined_chart, use_container_width=True)


def violinplot_floors():
    df = pd.read_csv('humiditynovacation.csv')
    fig = px.violin(df, y="Humidity", x="planta", color="planta", box=True, labels={'planta':'Floor', 'Humidity':'Humidity (%)'})
    fig.update_layout(title_text="Distribution of humidity in the floors of building A")
    # Remove the mode bar
    config = {
        'displayModeBar': False
    }
    st.plotly_chart(fig,config=config)


@st.experimental_fragment
def heatmap_hum():
    sourcemonth = get_qualitataules_data()
    sourceyear = get_qualitataulesnovacation_data()

    groupby_options = ['Whole year', 'Group by month']
    select_radio = st.radio("Choose time aggregation:", groupby_options, key = "time_agg_hum", horizontal = True)
    if select_radio == 'Whole year':
        source = sourceyear
    else:
        source = sourcemonth
        slider_month = alt.binding_range(name='Month', min=1, max=12, step=1)
        selector_month = alt.selection_single(name="Select a month", fields=['Month'], bind=slider_month, init={'Month': 1})

    col1, col2 = st.columns(2)

    with col1:
        if select_radio == 'Whole year': #change scale
            heatmap = alt.Chart(source).mark_rect(color = 'red').encode(
                x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
                color = alt.Color('humitat_alta:Q', scale=alt.Scale(scheme='reds'), title = '% Hours humidity higher than comfort')
            )
        else:
            # Configure heatmap
            heatmap = alt.Chart(source).mark_rect(color = 'red').encode(
                x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
                color = alt.Color('humitat_alta:Q', scale=alt.Scale(scheme='reds', domain=[0,34]), title = '% Hours humidity higher than comfort')
            )

        # Configure text
        text = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        if select_radio == 'Whole year':
            chart1 = (heatmap + text)
        else:
            chart1 = (heatmap+text).add_selection(selector_month).transform_filter(selector_month)
        chart1 = chart1.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=11).properties(width = 250, height = 500, title = 'Percentage of times each class exceeded comfort humidity').configure_title(fontSize=14).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart1, use_container_width=True, theme='streamlit')

    with col2:
        # Configure heatmap
        if select_radio == 'Whole year':
            heatmap2 = alt.Chart(source).mark_rect(color = 'red').encode(
                x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
                color = alt.Color('humitat_baixa:Q', title = '% Hours humidity lower than comfort')
            )
        else:
            heatmap2 = alt.Chart(source).mark_rect(color = 'red').encode(
                x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
                color = alt.Color('humitat_baixa:Q', scale=alt.Scale(domain=[0,39]), title = '% Hours humidity lower than comfort')
            )

        # Configure text
        text2 = alt.Chart(source).mark_text(baseline='middle').encode(
            x=alt.X('posicio:O', title='Class position', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
            text = alt.Text('Aula:N'),
        )

        # Draw the chart
        if select_radio == 'Whole year':
            chart2 = (heatmap2 + text2)
        else:
            chart2 = (heatmap2+text2).add_selection(selector_month).transform_filter(selector_month)
        chart2 = chart2.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=11).properties(width = 250, height = 500, title = 'Percentage of times each class fell down comfort humidity').configure_title(fontSize=14).configure_axis(labelFontSize=10,titleFontSize=10)
        st.altair_chart(chart2, use_container_width=True, theme='streamlit')



def humidity_temp_high():
    # Load the data
    df = pd.read_csv('highhumtempcount.csv')

    # Scatter Plot with adjusted spacing
    scatter_chart = alt.Chart(df).mark_point(filled=True).encode(
        y=alt.Y('Month:O', scale=alt.Scale(padding=10)),  # Adjust padding as needed
        x=alt.X('Aula:N', title='Classroom', axis=alt.Axis(labelAngle=0)),
        size=alt.Size('count:Q', title = 'Count'),
        tooltip=['Aula', 'Month', 'count']
    ).properties(
        title='Total High Humidity and Temperature Occurrences by Class',
        width=800,
        height=300
    )

    st.altair_chart(scatter_chart, use_container_width=True)


def scatter_sensation():
    df = pd.read_csv('highhumtempsensation.csv')
    color_palette = alt.Scale(domain=['High', 'Caution', 'Extreme caution'], range=['#ffce44', '#ff8243', 'red'])
    # Scatter plot
    scatter_chart = alt.Chart(df).mark_point(filled=True).encode(
        x='Date:T',  # Assuming 'Date' is the column name for dates
        y=alt.Y('Heat index:Q', scale=alt.Scale(domain=[25,36])),
        color=alt.Color('Sensation:N', scale = color_palette),
        #size='Humidity:Q',
        tooltip=['Aula', 'Date:T', 'Temperatura', 'Heat index', 'Humidity']
    ).properties(
        title='Scatter Plot of heat index (temperature affected by humidity)',
        width=800,
        height=400
    )

    st.altair_chart(scatter_chart, use_container_width=True)


@st.experimental_fragment
def metrics_aules_hum():
    st.write('**Ranking: Humidity Statistics for Each Class**')

    # Load and preprocess the data
    aules_temp = get_humidityaules_data()
    grouped_temp = aules_temp.groupby('Aula')['Humidity'].agg(['mean', 'min', 'max']).reset_index().round(2).reset_index()

    # Sorting options
    sort_order = st.selectbox("Sort order", ["Class position", "More to Less Humid", "Less to More Humid"], key = '222')

    # Sort the DataFrame based on the user's selection
    if sort_order == "More to Less Humid":
     grouped_temp = grouped_temp.sort_values(by='mean', ascending=True)
    elif sort_order == "Less to More Humid":
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
                st.metric(label="Mean percentage of humidity", value=f"{mean_temp}%")
            with col2:
                st.metric(label="Min percentage of humidity", value=f"{min_temp}%")
            with col3:
                st.metric(label="Max percentage of humidity", value=f"{max_temp}%")


def main():
    # Title and Introduction
    st.markdown("<h2>Analysis of Humidity Percentage in Classrooms</h2>", unsafe_allow_html=True)
    st.write("""
    In this section, we will analyze the humidity percentages in classrooms at ETSAB to evaluate indoor air quality. The analysis includes visualizations of humidity percentages across different floors and times of the day.
    """)

    # Humidity Analysis
    st.markdown("<h4>Humidity Analysis</h4>", unsafe_allow_html=True)
    st.write("""
    This chart displays the humidity percentages in various classrooms. Proper humidity percentages are crucial for comfort and health, affecting both physical well-being and cognitive performance. High or low humidity can lead to discomfort and various health issues.
    """)
    plot_humidity_aules()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>Percentage of humidity is mostly inside the comfort zone during the year.</li>
            <li>There are some humidity exceedances from July to October, while cold months present lower humidity percentage than recommended.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Floor-wise Humidity Analysis
    st.markdown("<h4>Floor-wise Humidity Analysis</h4>", unsafe_allow_html=True)
    st.write("""
    This analysis compares humidity percentages across different floors of the building. Identifying floors with significant humidity issues can help in taking targeted actions to improve air quality. Vacation days and weekends, specified in the Additional Information section, have been excluded from this analysis. The data is only for hours when classes are in session, from 8 AM to 9 PM.
    """)
    violinplot_floors()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>Floors 1 and 2 present higher range of humidity percentage than the others.</li>
            <li>The median and interquantile range of all the floors is quite similar, with exception of floor 1, which present higher himidity values.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # High Humidity and Temperature Correlation
    st.markdown("<h4>High Humidity related to High Temperature: Thermal Sensation</h4>", unsafe_allow_html=True)
    st.write("""
    This chart explores the correlation between high humidity percentages and temperature by counting the number of times that both variables are higher than a certain threshold (40% of humidity and 25℃ of temperature). Understanding this relationship can help in better managing classroom environments, as humidity related to temperature is an important factor for comfort. Vacation days and weekends have been excluded, and the data is only for hours when classes are in session, from 8 AM to 9 PM.
    """)
    humidity_temp_high()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>Only September, October and June present high temperature and humidity values at the same time, being October the most problematic month.</li>
            <li>Classes of the first floors are the ones that present the highest occurence of both extreme temperature and humidity.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.write("""
    This scatter plot shows the relationship between humidity and heat index in classrooms, which can only be computed for temperatures higher than 26℃ and humidity percentage higher than 40%. So, the data for this subsection has been filtered according to these values. Also, vacation days and weekends have been excluded, and the data is only for hours when classes are in session, from 8 AM to 9 PM.
    """)
    st.write("""
    Heat index, also known as the apparent temperature, is what the temperature feels like to the human body when relative humidity is combined with the air temperature. The reason why it's so important is because it is what students and teachers are really feeling when they are in the classrooms. When heat index reach caution (from 27℃ to 32℃), the human being can feel possible fatigue due to prolonged exposure or physical activity. Furthermore, when heat index reaches from 33℃ to 40℃, the sensation is classified as extreme caution, as people can have sunstroke, heatstroke and cramps when prolonged exposure or physical activity.
    """)
    scatter_sensation()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
       <ul>
           <li>Dangerous heat index is reached a significantly high number of times during class hours.</li>
           <li>This problem only takes place on warm months, being June the most problematic.</li>
       </ul>
    </div>
    """, unsafe_allow_html=True)

    # Metrics Summary
    st.markdown("<h4>Humidity Quality Metric per Class</h4>", unsafe_allow_html=True)
    st.write("""
    This heatmap provides a visual representation of humidity percentages across different classrooms and times. It helps in quickly identifying areas with significant humidity variations that may need attention. When the whole year option is selected, the data is automatically filtered by no-vacation and no-weekends. Be careful with the color scale, as it changes when seeing the global year or monthly data, in order to be able to appreciate the variations between classes in the global data.
    """)
    heatmap_hum()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>Humidity percentages higher than comfort are always much more present in floor 1, and some months also floors 2 and 3.</li>
            <li>Lower humidity percentages are more frequent than higher humidity percentages.</li>
            <li>These low percentages are a problem in higher floors (mostly floors 5 and 6) and, on December, in classrooms placed in position 1 (near the bathrooms).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.write("""
    This section summarizes the humidity metrics across all classrooms. It provides an overview of how often and by how much classrooms deviate from optimal humidity percentages.
    """)
    metrics_aules_hum()

    # Additional Information Section
    st.write("""
        <div style="padding: 15px; margin-top: 20px;">
            <h4 style="color: gray;">Additional Information:</h4>
            <p style="color: gray;">In the humidity graphics, the vacation days are the ones where there's no class or activity for the students, as there's no usage of the classrooms. So, the following dates are excluded from the air quality analysis:
                <br>
                2023-09-25, 2023-10-12, 2023-11-01, 2023-12-06, 2023-12-07, 2023-12-08, 2023-12-23, 2023-12-24, 2023-12-25, 2023-12-26, 2023-12-27, 2023-12-28, 2023-12-29, 2023-12-30, 2023-12-31, 2023-01-01, 2023-01-02, 2023-01-03, 2023-01-04, 2023-01-05, 2023-01-06, 2023-01-07, 2023-01-08, 2023-01-09, 2023-01-10, 2023-04-01, 2023-04-02, 2023-04-03, 2023-04-04, 2023-04-05, 2023-04-06, 2023-04-07, 2023-04-08, 2023-04-09, 2023-04-10, 2023-05-01, 2023-09-11.
                <br>
                All August and July days and weekends are also excluded.
            </p>
        </div>
    """, unsafe_allow_html=True)
