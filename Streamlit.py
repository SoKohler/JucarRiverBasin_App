import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os


#cd myCloud\Sophia\Thesis\Model\Jucar_model\Adrià streamlit run Streamlit.py



st.title("Water Resource Management Dashboard")

# Define Tabs (Onglets)
tab1, tab2, tab3, tab4 = st.tabs(["Environmental Flows", "Agricultural Drought", "Urban Demand", "Crop Scenarios"])

# Tab 1: Environmental Flows
with tab1:
    st.header("Environmental Flows Management")
    qe_col_alar = st.slider("Environmental Flow at Alarcon (m³/s)", 10, 100, 50)
    sea_flow = st.slider("Environmental Flow to the Sea (m³/s)", 0, 50, 20)
    
    # Simulated Data and Visualization
    time = list(range(2020, 2031))
    flow = [qe_col_alar * 0.95**i for i in range(len(time))]
    sea = [sea_flow * 1.1**i for i in range(len(time))]
    
    fig, ax = plt.subplots()
    ax.plot(time, flow, label="Alarcon Flow")
    ax.plot(time, sea, label="Sea Flow")
    ax.set_title("Environmental Flows Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Flow (m³/s)")
    ax.legend()
    st.pyplot(fig)

# Tab 2: Agricultural Drought Management
with tab2:
    st.header("Agricultural Drought Management")
    drought_reduction = st.slider("Agricultural Demand Reduction (%)", -50, -20, -30)
    additional_pumping = st.slider("Additional Groundwater Pumping (hm³)", 0, 50, 25)
    
    st.write(f"### Agricultural Demand is Reduced by {drought_reduction}%")
    st.write(f"### Additional Pumping Allowed: {additional_pumping} hm³")

# Tab 3: Urban Demand Management
with tab3:
    st.header("Urban Demand Management")
    pop_growth_rate = st.number_input("Population Growth Rate (%/year)", -2.0, 5.0, 1.0)
    
    # Simulated Urban Demand
    demand = [100 + pop_growth_rate * i for i in range(len(time))]
    st.line_chart(pd.DataFrame({"Year": time, "Urban Demand": demand}).set_index("Year"))

# Tab 4: Crop Scenarios
with tab4:
    st.header("Crop Scenarios")
    citrus_area = st.slider("Citrus Crop Area (ha)", 10000, 50000, 30000)
    st.write(f"### Total Citrus Crop Area: {citrus_area} ha")
    
    abandonment = st.radio("Farmland Abandonment Scenario:", ["No Change", "10% Reduction", "20% Reduction"])
    st.write(f"Selected Scenario: {abandonment}")
