import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px


def normalize_percentages(df, groupby_cols):
    df['Total'] = df.groupby(groupby_cols)['Percentage'].transform('sum')
    df['Percentage'] = (df['Percentage'] / df['Total']) * 100
    df.drop(columns=['Total'], inplace=True)
    return df


@st.experimental_fragment
def dataclass_building_selection():
    finestres = pd.read_csv('finestresaulesETSAB2023_clean.csv')
    aules_data = {
            'Temperature': pd.read_csv('temperatureaulesETSAB2023_clean.csv'),
            'CO2': pd.read_csv('co2aulesETSAB2023_clean.csv'),
            'Humidity': pd.read_csv('humidityaulesETSAB2023_clean.csv')
        }
    aules_data['Temperature'] = aules_data['Temperature'].rename(columns={'Temperatura':'Temperature'})
    quality_data = {
            'Temperature': pd.read_csv('piequalitytemp.csv'),
            'CO2': pd.read_csv('piequalityco2.csv'),
            'Humidity': pd.read_csv('piequalityhum.csv')
        }
    for var in aules_data:
        aules_data[var]['Date'] = pd.to_datetime(aules_data[var]['Date'], format='%Y-%m-%d %H:%M:%S')
        aules_data[var]['Month'] = aules_data[var]['Date'].dt.month

    # Define the color mapping
    color_mapping = {
        'A-11': '#318ce7', 'A-12': '#e74c3c', 'A-13': '#2ecc71', 'A-14': '#f1c40f',
        'A-21': '#3498db', 'A-22': '#9b59b6', 'A-23': '#e67e22', 'A-24': '#1abc9c',
        'A-31': '#d35400', 'A-32': '#34495e', 'A-33': '#16a085', 'A-34': '#2980b9',
        'A-35': '#8e44ad', 'A-36': '#f39c12', 'A-41': '#c0392b', 'A-42': '#27ae60',
        'A-43': '#d35400', 'A-44': '#8e44ad', 'A-51': '#2ecc71', 'A-52': '#3498db',
        'A-53': '#f1c40f', 'A-54': '#1abc9c', 'A-55': '#e74c3c', 'A-56': '#34495e',
        'A-61': '#9b59b6', 'A-62': '#16a085'
    }

    # Initialize session state for selected classes
    if 'selected_classes' not in st.session_state:
        st.session_state.selected_classes = ['A-11']

    # Get unique floors and positions
    floors = sorted(finestres['planta'].unique(), reverse=True)
    positions = sorted(finestres['posicio'].unique())

    # Create a dictionary to store the state of each checkbox
    checkbox_states = {}
    st.write("RECOMMENDATION: Do not select more than 5 classes. The performance and understandability will decrease. The plot is thought to compare a few classes in more detail.")
    st.write("**Select Classes from the Building Layout**")
    col1, col2 = st.columns([2,1])
    with col1:
        # Create a layout of checkboxes
        for floor in floors:
            cols = st.columns(len(positions))
            for pos_idx, pos in enumerate(positions):
                aula = finestres[(finestres['planta'] == floor) & (finestres['posicio'] == pos)]
                if not aula.empty:
                    aula_name = aula['Aula'].values[0]
                    checkbox_states[aula_name] = cols[pos_idx].checkbox(
                        aula_name,
                        value=aula_name in st.session_state.selected_classes,
                        key=f'class{aula_name}'  # Unique key for temperature checkboxes
                    )

        # Update session state with selected classes
        st.session_state.selected_classes = [aula for aula, selected in checkbox_states.items() if selected]

    with col2:
        # Variable selection
        variable = st.selectbox("Select variable to display:", ['Temperature', 'CO2', 'Humidity'], key='variable_selection')

        # Filter the dataset based on the selected classes
        filtered_aules_data = aules_data[variable][aules_data[variable]['Aula'].isin(st.session_state.selected_classes)]
        filtered_data_quality = quality_data[variable][quality_data[variable]['Aula'].isin(st.session_state.selected_classes)]

        groupby_options = ['Whole year', 'Show a month']
        select_radio = st.radio("Choose time aggregation:", groupby_options, key="time_agg_temp", horizontal=True)

        if select_radio == 'Show a month':
            slider_month = st.slider("Select a month", 1, 12)
            filtered_aules_data = filtered_aules_data[filtered_aules_data['Month']==slider_month]
            filtered_data_quality = filtered_data_quality[filtered_data_quality['Month']==slider_month]


    # Plot the temperature data
    if not filtered_aules_data.empty:
        # Create a new DataFrame for the color legend to map classes to their colors
        color_df = pd.DataFrame({
            'Aula': list(color_mapping.keys()),
            'Color': list(color_mapping.values())
        })

        # Merge the filtered data with the color DataFrame to maintain color consistency
        merged_data = pd.merge(filtered_aules_data, color_df, on='Aula', how='left')

        # Get the selected class colors
        selected_colors = {aula: color_mapping[aula] for aula in st.session_state.selected_classes}

        # Define y-axis title based on the variable
        y_axis_title = {
            'Temperature': 'Temperature (°C)',
            'CO2': 'CO2 Concentrations (ppm)',
            'Humidity': 'Percentage of humidity'
        }

        chart = alt.Chart(merged_data).mark_point(filled=True, size=3).encode(
            x='Date:T',
            y=alt.Y(f'{variable}:Q', title=y_axis_title[variable]),
            color=alt.Color('Aula:N', scale=alt.Scale(domain=list(selected_colors.keys()), range=list(selected_colors.values())))
        ).properties(
            title=f'{variable} of the classes of building A with the comfort'
        )

        # Define comfort ranges for each variable
        comfort_ranges = {
            'Temperature': {'min': 'min_comfort', 'max': 'max_comfort'},
            'CO2': {'min': 'outdoors_co2', 'max': 'max_co2'},
            'Humidity': {'min': 'min_humidity', 'max': 'max_humidity'}
        }

        comfort = alt.Chart(merged_data).mark_area(opacity=0.3).encode(
            alt.X('Date:T'),
            alt.Y(comfort_ranges[variable]['min']),
            alt.Y2(comfort_ranges[variable]['max'])
        )

        combined_chart = comfort + chart
        #combined_chart = (comfort + chart).add_selection(selector_month).transform_filter(selector_month)

        st.altair_chart(combined_chart, use_container_width=True)

        # Function to normalize percentages
        def normalize_percentages(df):
            df['Total'] = df[['Lower', 'Upper', 'Comfort']].sum(axis=1)
            df['Lower'] = (df['Lower'] / df['Total']) * 100
            df['Upper'] = (df['Upper'] / df['Total']) * 100
            df['Comfort'] = (df['Comfort'] / df['Total']) * 100
            df.drop(columns=['Total'], inplace=True)
            return df

        # Drop any unnamed columns that may have been read in
        filtered_data_quality = filtered_data_quality.loc[:, ~filtered_data_quality.columns.str.contains('^Unnamed')]

        # PIE CHARTS
        if select_radio == 'Whole year':
            filtered_data_quality = filtered_data_quality.drop(columns=['Month'])
            filtered_data_quality = filtered_data_quality.groupby('Aula').mean().reset_index()
            filtered_data_quality = normalize_percentages(filtered_data_quality)
            melted_df = filtered_data_quality.melt(id_vars=['Aula'], var_name='Zone', value_name='Percentage')
        else:
            filtered_data_quality = normalize_percentages(filtered_data_quality)
            melted_df = filtered_data_quality.melt(id_vars=['Aula', 'Month'], var_name='Zone', value_name='Percentage')

        # Function to create pie chart for a given Aula
        def create_pie_chart(df, aula):
            fig = px.pie(
                df[df['Aula'] == aula],
                values='Percentage',
                names='Zone',
                title=f'Class: {aula}',
                color='Zone',
                color_discrete_map={'Lower': '#3CB371', 'Upper': '#FF6347', 'Comfort': '#1E90FF'},
                hole=0.3  # Make the pie chart smaller with a donut chart style
            )
            fig.update_layout(
                margin=dict(t=20, b=20, l=0, r=0),
                height=300,  # Smaller height
                width=200   # Smaller width
            )
            return fig

        # Display pie charts in a grid layout in Streamlit
        aulas = melted_df['Aula'].unique()
        num_cols = 3  # Number of columns in the grid
        num_rows = (len(aulas) + num_cols - 1) // num_cols
        # Remove the mode bar
        config = {
            'displayModeBar': False
        }
        for row in range(num_rows):
            cols = st.columns(num_cols)
            for col in range(num_cols):
                index = row * num_cols + col
                if index < len(aulas):
                    aula = aulas[index]
                    pie_chart = create_pie_chart(melted_df, aula)
                    cols[col].plotly_chart(pie_chart, use_container_width=True, config=config)



def main():
    st.markdown("<h2>Detailed Classroom Comparison</h2>", unsafe_allow_html=True)
    st.write("""
    In this section, you can compare detailed air quality metrics for different classrooms. Select the variable you want to analyze, the time period, and the aggregation level (whole year or per month).
    """)
    st.write("""
    The scatter plot below shows the selected variable over time for the selected classrooms. This allows for a detailed comparison of air quality metrics between different classrooms.
    """)

    st.write("""
    The pie chart provides a breakdown of the percentage of time each classroom spends in comfort, high, or low values for the selected variable. This gives an overview of the overall air quality performance for each classroom.
    """)
    dataclass_building_selection()
