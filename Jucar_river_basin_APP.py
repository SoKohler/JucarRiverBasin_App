# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:49:58 2024

@author: sophi

source documentation : https://dash-bootstrap-components.opensource.faculty.ai/docs/components/accordion/
http://127.0.0.1:8050
"""
#cd C:\Users\sophi\myCloud\Sophia\Thesis\Model\Jucar_model\Adrià\App_Jucar
#streamlit run Jucar_river_basin.py
# -*- coding: utf-8 -*-
"""
Model to run Vensim 
"""
### 0.Import functions and libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
#import Python System Dynamics library to run Vensim
import pysd
#app
import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc # to make the app visually appealing 
import plotly.graph_objs as go # to create interactive graphs

### 1.Read data
# Import the data with all sheets (type = dictionary) (copy past data_initial)
workbook = openpyxl.load_workbook("data_initial.xlsx")
workbook.save("data.xlsx")
# # Import the data with all sheets (type = dictionary)
# # copy data_initial skipping the frist row
# data_all= pd.read_excel('data.xlsx', sheet_name=None)
# sheet_names = list(data_all.keys())
# # Create the variable for each of the sheets (globals() allows you to modify the global namespace))
# for sheet_name in sheet_names:
#     globals()[f"data_{sheet_name}"] = pd.read_excel('data.xlsx', sheet_name=sheet_name, engine="openpyxl")
#     print(f"data_{sheet_name}")
# ### 2. Read Vensim Model
vensim_model = pysd.read_vensim('WEFE Jucar (Simple).mdl')    
variables_model = vensim_model.run(params={'INITIAL TIME': 1,'FINAL TIME': 120,'TIME STEP': 1})


### 3. APP - DASH
# i. initialize the App
app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN]) # LUX = pre-built Bootstrap theme 
app.title = "Júcar River Basin Management"


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080) # port = 8080 to use is on any free port

