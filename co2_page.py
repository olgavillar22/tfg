import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

from common_functions import *


def plot_co2_aules():
    aules_co2 = pd.read_csv('co2subsampledETSAB2023_clean.csv')

    aules_co2['Date'] = pd.to_datetime(aules_co2['Date'], format='%Y-%m-%d %H:%M:%S')
    color_palette = alt.Scale(domain=['Comfort', 'Unhealthy', 'Outdoor air'], range=['blue', '#c3272b', '#3eb489'])

    chart = alt.Chart(aules_co2).mark_point(filled = True, size = 3).encode(
        x = 'Date:T',
        y = alt.Y('CO2:Q', title = 'CO₂ concentration (ppm)'),
        color = alt.Color('Color:N', scale = color_palette),
        tooltip= ['Date','CO2','Aula']
    ).properties(
        title = 'CO₂ concentration of classes of building A with the comfort zone'
    )

    comfort = alt.Chart(aules_co2).mark_area(opacity = 0.3).encode(
        alt.X('Date:T'),
        alt.Y('outdoors_co2'),
        alt.Y2('max_co2')
    )

    combined_chart = comfort + chart

    st.altair_chart(combined_chart, use_container_width=True)


def violinplot_floors():
    df = get_co2novacation_data()
    fig = px.violin(df, y="CO2", x="planta", color="planta", box=True, labels={'planta':'Floor', 'CO2':'CO₂'})
    fig.update_layout(title_text="Distribution of CO₂ concentration in floors of building A")
    # Remove the mode bar
    config = {
        'displayModeBar': False
    }
    st.plotly_chart(fig, config=config)


def co2_during_day():
    df = pd.read_csv('co2duringday.csv')

    chart = alt.Chart(df).mark_line().encode(
        x = alt.X('hour_of_day:O', title = 'hour of the day', axis=alt.Axis(labelAngle=0)),
        y = alt.Y('CO2:Q', scale=alt.Scale(domain=[425, 675]), title = 'CO₂ concentration (ppm)'),
        color = alt.Color('day_of_week:N', title = 'Day of the week')
    ).properties(title = 'Average CO₂ concentration evolution per each day of the week')

    st.altair_chart(chart, use_container_width=True)


def boxplot_finestres():
    co2_aulesA2 = get_co2novacation_data()

    finestres = pd.DataFrame(data={'Aula': ['A-11','A-12','A-13','A-14','A-21','A-22','A-23','A-24','A-31','A-32',
    'A-33','A-34','A-35','A-36','A-41','A-42','A-43','A-44','A-51','A-52','A-53','A-54','A-55','A-56','A-61','A-62'],
                                   'finestres': [6,6,6,6,6,6,6,6,4,4,4,4,4,4,4,7,6,6,4,4,4,4,4,4,5,6],
                                   'planta': [1,1,1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,5,5,5,5,5,5,6,6],
                                   'posicio': [1,2,3,4,1,2,3,4,1,2,3,4,5,6,1,2,3,4,1,2,3,4,5,6,1,2]
    })

    df = pd.merge(co2_aulesA2, finestres, on='Aula')


    fig = px.box(df, x='finestres', y='CO2', color = 'finestres',
                 title='Distribution of CO2 Concentration by Number of Windows',
                 labels={'finestres': 'Number of Windows', 'CO2': 'CO₂ Concentration (ppm)'})
    fig.update_layout(showlegend = False)
    # Remove the mode bar
    config = {
        'displayModeBar': False
    }
    st.plotly_chart(fig, config = config)


@st.experimental_fragment
def heatmap_co2():
    sourcemonth = get_qualitataules_data()
    sourceyear = get_qualitataulesnovacation_data()

    groupby_options = ['Whole year', 'Group by month']
    select_radio = st.radio("Choose time aggregation:", groupby_options, key = "time_agg_co2", horizontal = True)
    if select_radio == 'Whole year':
        source = sourceyear
    else:
        source = sourcemonth
        slider_month = alt.binding_range(name='Month', min=1, max=12, step=1)
        selector_month = alt.selection_single(name="Select a month", fields=['Month'], bind=slider_month, init={'Month': 1})
    col1, col2 = st.columns(2)

    # Configure heatmap
    heatmap = alt.Chart(source).mark_rect(color = 'red').encode(
        x=alt.X('posicio:O', title = 'Class position', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
        color = alt.Color('co2_excessiu:Q', scale=alt.Scale(scheme='reds', domain=[0,8.1]), title='% Hours CO₂ out Comfort')
    )

    # Configure text
    text = alt.Chart(source).mark_text(baseline='middle').encode(
        x=alt.X('posicio:O', title ='Class position', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('planta:O', scale=alt.Scale(reverse=True), title='Floor'),
        text = alt.Text('Aula:N'),
    )

    # Draw the chart
    if select_radio == 'Whole year':
        chart1 = (heatmap + text)
    else:
        chart1 = (heatmap+text).add_selection(selector_month).transform_filter(selector_month)
    chart1 = chart1.configure_legend(orient='bottom',labelFontSize=10,titleFontSize=11).properties(width = 500, height = 500, title = 'Percentage of times each class exceeded comfort CO₂ concentration').configure_title(fontSize=15).configure_axis(labelFontSize=10,titleFontSize=10)
    st.altair_chart(chart1, theme='streamlit')


@st.experimental_fragment
def metrics_aules_co2():
    st.write('**Ranking: CO₂ Statistics for Each Class**')

    # Load and preprocess the data
    aules_temp = get_co2aules_data()
    grouped_temp = aules_temp.groupby('Aula')['CO2'].agg(['mean', 'min', 'max']).round(2).reset_index()

    # Sorting options
    sort_order = st.selectbox("Sort order", ["Class position", "Healthier to Unhealthier", "Unhealtier to Healthier"], key = '111')

    # Sort the DataFrame based on the user's selection
    if sort_order == "Healthier to Unhealthier":
     grouped_temp = grouped_temp.sort_values(by='mean', ascending=True)
    elif sort_order == "Unhealtier to Healthier":
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
                st.metric(label="Mean CO₂ concentration", value=f"{mean_temp}ppm")
            with col2:
                st.metric(label="Min CO₂ concentration", value=f"{min_temp}ppm")
            with col3:
                st.metric(label="Max CO₂ concentration", value=f"{max_temp}ppm")


def main():
    # Title and Introduction
    st.markdown("<h2>Analysis of CO₂ Concentration in Classrooms</h2>", unsafe_allow_html=True)
    st.write("""
    In this section, we will analyze the CO₂ concentration in classrooms at ETSAB to assess air quality. The analysis includes visualizations of CO₂ concentrations across different floors and times of the day.
    """)

    # CO₂ Concentration Analysis
    st.markdown("<h4 >CO₂ Concentration Analysis</h4>", unsafe_allow_html=True)
    st.write("""
    This chart shows the CO₂ concentration concentrations in various classrooms. Monitoring CO₂ concentration is crucial for understanding ventilation effectiveness and ensuring a healthy learning environment. Elevated CO₂ concentrations can indicate inadequate ventilation, which can affect cognitive function and overall well-being.
    """)
    plot_co2_aules()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>During the week, CO₂ concentration gets clearly high with respect to the comfort zone, reaching possible unhealty values.</li>
            <li>There are frequent exceedances of the CO₂ comfort zone, especially from October to December, suggesting periods of poor ventilation.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Floor-wise CO₂ Concentration Analysis
    st.markdown("<h4 >Floor-wise CO₂ Concentration Analysis</h4>", unsafe_allow_html=True)
    st.write("""
    This analysis compares CO₂ concentration levels across different floors of the building. It helps to identify if certain floors have poorer air quality and may need better ventilation. Vacation days and weekends, specified in the Additional Information section, have been excluded from this analysis. The data is only for hours when classes are in session, from 8 AM to 9 PM.
    """)
    violinplot_floors()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>In floor 3, classrooms clearly reach higher CO₂ concentration levels than in other floors, while floors 5 and 6 are the ones with lower maximum CO₂ concentration.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Boxplot of CO₂ Levels by Windows
    st.markdown("<h4 >CO₂ Concentration by Number of Windows</h4>", unsafe_allow_html=True)
    st.write("""
    This boxplot shows the distribution of CO₂ concentrations based on the number of windows in each classroom. More windows usually imply better natural ventilation, which should result in lower CO₂ concentrations. Vacation days and weekends have been excluded, and the data is only for hours when classes are in session, from 8 AM to 9 PM.
    """)
    st.write("""It is worth mentioning that all the windows of building A have the same dimensions (a surface of 3.6m²) and they are equally separated. This means that the number of windows is directly proportional to the size of the classroom, which is important to interpretate this graphic.
    """)
    boxplot_finestres()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>Classrooms with four windows (also indicating smaller room size) tend to have higher CO₂ concentrations, indicating poorer air quality.</li>
            <li>Surprisingly, classrooms with six windows present higher CO₂ concentration levels than the ones with five windows, which should be related to class attendance.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # CO₂ Variation during the Day
    st.markdown("<h4 >CO₂ Variation during the Day</h4>", unsafe_allow_html=True)
    st.write("""
    This chart displays the variation in CO₂ concentration throughout the day for each day of the week. Understanding daily patterns can help identify times when air quality might be at its worst and require intervention. Vacation days have been excluded from this analysis.
    """)
    co2_during_day()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>In labor days, class hours can clearly be appreciated through CO₂ concentration.</li>
            <li>On Mondays and Tuesdays, there's higher CO₂ concentration during class hours, which might be related to class attendance.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Heatmap of CO₂ Levels
    st.markdown("<h4 >CO₂ Concentration Quality Metric per Class</h4>", unsafe_allow_html=True)
    st.write("""
    This heatmap provides a visual representation of CO₂ concentrations across different classrooms and times. It helps in quickly identifying hotspots with high CO₂ concentrations that may need improved ventilation measures. When the whole year option is selected, the data is automatically filtered by no-vacation and no-weekends.
    """)
    heatmap_co2()
    # Insights & Takeaways
    st.markdown("""
    <div style="border-radius: 10px; background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
        <h4 style="font-size: 14px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 2px;">Insights & Takeaways</h4>
        <ul>
            <li>The three first floors of the building have much higher CO₂ concentrations than the others, probably being related to the fact that they are more used for teaching sessions.</li>
            <li>The percentage of times each class is outside the CO₂ concentration comfort changes significantly across different months.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    metrics_aules_co2()

    # Additional Information Section
    st.write("""
    <div style="padding: 15px; margin-top: 20px;">
        <h4 style="color: gray;">Additional Information:</h4>
        <p style="color: gray;">In the the CO₂ graphics, vacation days are the ones where there's no class or activity for the students, as there's no usage of the classrooms. So, the following dates are excluded from the air quality analysis:
            <br>
            2023-09-25, 2023-10-12, 2023-11-01, 2023-12-06, 2023-12-07, 2023-12-08, 2023-12-23, 2023-12-24, 2023-12-25, 2023-12-26, 2023-12-27, 2023-12-28, 2023-12-29, 2023-12-30, 2023-12-31, 2023-01-01, 2023-01-02, 2023-01-03, 2023-01-04, 2023-01-05, 2023-01-06, 2023-01-07, 2023-01-08, 2023-01-09, 2023-01-10, 2023-04-01, 2023-04-02, 2023-04-03, 2023-04-04, 2023-04-05, 2023-04-06, 2023-04-07, 2023-04-08, 2023-04-09, 2023-04-10, 2023-05-01, 2023-09-11.
            <br>
            All August and July days and weekends are also excluded.
        </p>
    </div>
    """, unsafe_allow_html=True)
