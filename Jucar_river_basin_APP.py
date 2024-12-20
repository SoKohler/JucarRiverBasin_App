# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 18:06:32 2024

@author: sophi
"""
#cd myCloud\Sophia\Thesis\Model\Jucar_model\Adrià\
#streamlit run Jucar_river_basin_APP.py
#git save

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_echarts import st_echarts

# Page configuration
st.set_page_config(page_title="Júcar River Basin Water management visualization tool", layout="wide")


### Dynamic navigation menu 
menu = st.sidebar.radio( "Menu",
    ["Home", "Alarcon’s reservoir", "Scenario Analysis", "Comparisons", "Data Upload"])


# App title
st.title("Júcar River Basin - Water management visualization tool")
### 0. Home page (explain the content of the app and the model)
if menu == "Home":
    st.header("0. Home page")
    st.write(""" Welcome to the **Júcar River Basin System Dynamics Model**.  
    This tool provides an interactive platform to analyze and simulate the behavior of the Júcar River system under various conditions, including drought scenarios and reservoir operation strategies.""")
    st.header("Key features of the tool")
    st.write("""
    - **Visualize Water Resource Dynamics**: Explore flows between reservoirs, aquifers, and demands.
    - **Interactive Variables**: Adjust reservoir operating rules, environmental flows, and agricultural water reductions.
    - **Drought Management Simulation**: Test drought-triggered measures and evaluate their impacts on storage, supply, and economic outcomes.
    - **Performance Indicators**: Monitor system performance with metrics like deficits, ecological flow compliance, and reservoir states.
    """)
    # Instructions
    st.header("How to use this tool")
    st.write("""
    1. **Navigate** through the app using the menu on the left.
    2. **Explore Key Variables**: Use sliders and inputs to adjust flows, demands, and policies.
    3. **Simulate Scenarios**: Run simulations and observe results in dynamic charts and tables.
    4. **Compare Impacts**: Analyze the effects of management decisions on water availability and system resilience.
    """)





### 1. Alarcon’s reservoir
elif menu == "Alarcon’s reservoir":
    st.header("1. Alarcon’s reservoir")
    st.write("This is the dashboard displaying key visualizations and metrics.")

    # Sample Data for Visualization
    x_data = list(range(1, 11))
    y_data = [i**2 for i in x_data]

    # Line Chart
    st.subheader("Line Chart Example")
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data, label="y = x²", color="blue")
    ax.set_title("Line Chart Example")
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.legend()
    st.pyplot(fig)

    # Display Metrics
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Flow", "350 m³/s", "+10%")
    col2.metric("Deficit Reduction", "12%", "-5%")
    col3.metric("Population Growth", "2.5%", "Stable")

# --- Scenario Analysis Page ---
elif menu == "Scenario Analysis":
    st.header("📈 Scenario Analysis")
    st.write("Adjust the parameters below to analyze different scenarios.")

    # Input Controls
    scenario_value = st.slider("Select Environmental Flow (m³/s)", 50, 200, 100)
    demand_reduction = st.slider("Agricultural Demand Reduction (%)", 10, 50, 30)

    # Visualization
    x_scenario = list(range(2020, 2031))
    y_scenario = [scenario_value - (demand_reduction / 100) * x for x in range(0, 11)]

    options = {
        "title": {"text": "Scenario Analysis Results"},
        "xAxis": {"type": "category", "data": x_scenario},
        "yAxis": {"type": "value"},
        "series": [{"data": y_scenario, "type": "line", "name": "Flow"}],
    }
    st_echarts(options=options, height="400px")

# --- Comparisons Page ---
elif menu == "Comparisons":
    st.header("📊 Chart Comparisons")
    st.write("Compare multiple charts and datasets side by side.")

    col1, col2 = st.columns(2)

    # Bar Chart
    with col1:
        st.subheader("Bar Chart Example")
        data = {"Category": ["A", "B", "C"], "Values": [10, 20, 30]}
        df = pd.DataFrame(data)
        st.bar_chart(df.set_index("Category"))

    # Pie Chart
    with col2:
        st.subheader("Pie Chart Example")
        pie_options = {
            "title": {"text": "Pie Chart Example"},
            "series": [
                {"type": "pie", "radius": "50%", "data": [
                    {"value": 10, "name": "A"},
                    {"value": 20, "name": "B"},
                    {"value": 30, "name": "C"},
                ]}
            ],
        }
        st_echarts(options=pie_options, height="400px")

# --- Data Upload Page ---
elif menu == "Data Upload":
    st.header("📋 Data Upload")
    st.write("Upload a dataset for analysis.")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        user_df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:")
        st.dataframe(user_df)

        # Basic Summary
        st.subheader("Data Summary")
        st.write(user_df.describe())


#treitoiejtjeotektoet