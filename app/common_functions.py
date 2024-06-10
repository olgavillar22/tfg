import pandas as pd
import streamlit as st


def groupby_time(df, time_agg):
    if time_agg == 'Month':
        return df.groupby(df['Date'].dt.to_period('M')).mean().reset_index()
    elif time_agg == 'Day':
        return df.groupby(df['Date'].dt.to_period('d')).mean().reset_index()
    elif time_agg == 'Hour':
        return df.groupby(df['Date'].dt.to_period('h')).mean().reset_index()


def groupby_time_planta(df, time_agg):
    if time_agg == 'Month':
        return df.groupby([df['Date'].dt.to_period('M'), 'Planta']).mean().reset_index()
    elif time_agg == 'Day':
        return df.groupby([df['Date'].dt.to_period('d'), 'Planta']).mean().reset_index()
    elif time_agg == 'Hour':
        return df.groupby([df['Date'].dt.to_period('h'), 'Planta']).mean().reset_index()


def get_time_groupby_selection(kind):
    # Add groupby button custom
    groupby_options = ['Month', 'Day', 'Hour']
    select_groupby_var= st.radio("Choose the time aggregation:", groupby_options, key = f"""groupby_key_{kind}""", horizontal = True)

    return select_groupby_var

def get_festius_energy_selection(kind):
    groupby_options = ['Show vacation days', 'Soften vacation days']
    select_vacation = st.radio("Choose vacation filter:", groupby_options, key = f"""filter_vacation_days_{kind}""", horizontal = True)
    return select_vacation


def get_time_filter(kind):
    # Sidebar widgets for selecting time interval
    start_date_default = pd.Timestamp('2023-01-01 00:00:00')
    end_date_default = pd.Timestamp('2023-12-31 23:59:59')

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Determine the Start Date:", value=start_date_default, min_value=start_date_default.date(), max_value=end_date_default.date(), key = f"""filter_start_key_{kind}""")
    with col2:
        end_date = st.date_input("Determine the End Date:", value=end_date_default, min_value=start_date_default.date(), max_value=end_date_default.date(), key = f"""filter_end_key_{kind}""")

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if start_date > end_date:
        st.error("Error: Start date must not be after end date")

    return start_date, end_date


def get_temperatureA_data():
    # Dades de temperatura de l'edifici A per plantes
    temp = pd.read_csv('/home/olga/Desktop/tfg/temperatureETSAB2023_clean.csv')
    temp['Date'] = pd.to_datetime(temp['Date'], format='%Y-%m-%d %H:%M:%S')

    return temp
