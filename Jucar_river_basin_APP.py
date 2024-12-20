# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 18:06:32 2024

@author: sophi
"""
#cd myCloud\Sophia\Thesis\Model\Jucar_model\Adrià\
#streamlit run Jucar_river_basin_APP.py
#git save


#import Python System Dynamics library to run Vensim
import pysd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_echarts import st_echarts
import openpyxl
from openpyxl import load_workbook

### 1.Read data
#transform all the formulas into static number 
workbook = load_workbook('data_formulas.xlsx', data_only=True) 
sheet = workbook.active #it will read all the sheets 
#overwrite formulas with values
for row in sheet.iter_rows():
    for cell in row:
        if cell.data_type == 'f':  # if the cell contains a formula
            cell.value = cell.value  #replace the formula by the static value
workbook.save('data.xlsx')


# Import the data with all sheets (type = dictionary)
data_all = pd.read_excel("data.xlsx", sheet_name=None, engine="openpyxl")# List of sheet names
sheet_names = list(data_all.keys())
# Create the variable for each of the sheets (globals() allows you to modify the global namespace))
for sheet_name in sheet_names:
    globals()[f"data_{sheet_name}"] = pd.read_excel("data.xlsx", sheet_name=sheet_name,skiprows=1, engine="openpyxl")
    print(f"data_{sheet_name}")

### 2. Read Vensim Model
vensim_model = pysd.read_vensim('WEFE Jucar (Simple).mdl')    
variables_model = vensim_model.run(params={'INITIAL TIME': 1,'FINAL TIME': 120,'TIME STEP': 1})


# Page configuration
st.set_page_config(page_title="Júcar River Basin Water management visualization tool", layout="centered",initial_sidebar_state="expanded")

### Dynamic navigation menu 
menu = st.sidebar.radio( "Menu",
    ["Home", "Alarcon’s reservoir","vary"])
# App title
st.title("Júcar River Basin - Water management visualization tool")
### 0. Home page (explain the content of the app and the model)
if menu == "Home":
    st.header("0. Home page")
    # Tabs in Home Section
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Vensim model - View 1", "Vensim model - View 2", "Vensim model - View 3","Vensim model - View 4","Vensim model - View 3","Vensim model - View 5","Vensim model - View 6"])
    
    with tab1:
        st.header("Overview")
        st.write("""
        The Júcar River Basin System Dynamics Model is designed to simulate water flows, reservoir levels, and drought conditions. 
        It helps analyze the effects of water management policies on the environment and economy.
        """)
        st.header("Key Features")
        st.write("""
        - **Visualize Water Resource Dynamics**: Explore flows between reservoirs, aquifers, and demands.
        - **Interactive Variables**: Adjust reservoir operating rules and test drought measures.
        - **Performance Indicators**: Monitor compliance with ecological flows and economic impacts.
        """)
        st.header("Instructions")
        st.write("""
        1. **Navigate** through the app using the menu on the left.
        2. **Explore Key Variables**: Use sliders and inputs to adjust flows, demands, and policies.
        3. **Simulate Scenarios**: Observe results in charts and tables.
        """)
    with tab2:
        st.header("Vensim model - View 1  - SYSTEM NETWORK " )
        st.image("View_1.PNG", caption="General view of the system the Júcar River Model", use_column_width=True)
    with tab3:
        st.header("Vensim model - View 2 - MANCHA ORIENTAL AQUIFER " )
        st.image("View_2.PNG", caption="Subsystem for the stream aquifer interaction between the Jucar River and the Mancha Oriental aquifer", use_column_width=True)
    with tab4:
        st.header("Vensim model - View 3 - WATER DEMAND, SUPPLY AND DEFICIT " )
        st.image("View_3.PNG", caption="The Júcar River, Spain", use_column_width=True)
    with tab5:
        st.header("Vensim model - View 4 - RESERVOIRS OPERATING RULES " )
        st.image("View_4.PNG", caption="The Júcar River, Spain", use_column_width=True)        
    with tab6:
        st.header("Vensim model - View 5 - STATE INDEX" )
        st.image("View_5.PNG", caption="The Júcar River, Spain", use_column_width=True)      
    with tab7:
        st.header("Vensim model - View 6 - CROPS" )
        st.image("Crops.PNG", caption="The Júcar River, Spain", use_column_width=True)    

### 1. Alarcon’s reservoir
elif menu == "Alarcon’s reservoir":
    st.header("1. Alarcon’s reservoir")
    st.write("xjgojdsg")

    # Input Controls
    initial_env_flow = 5.8
    x_data = st.slider("Select Environmental Flow (m³/s)", 0.0, 10.0, initial_env_flow, 0.1) # min, max, default, step
    y_data = [(x_data / 100)]

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


