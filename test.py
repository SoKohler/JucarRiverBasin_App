
### 0.Import functions and libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
#import Python System Dynamics library to run Vensim
import pysd
#app
import dash
from dash import Dash, dcc, html, Input, Output, callback,State
import dash_bootstrap_components as dbc # to make the app visually appealing 
import plotly.graph_objs as go # to create interactive graphs
import time
import pandas as pd
import openpyxl
vensim_model = pysd.read_vensim('WEFE Jucar (Simple).mdl')
qecolAlar_value = 10
# Example data as a pandas DataFrame
# Read the Excel sheet into a DataFrame
workbook = openpyxl.load_workbook("data.xlsx")
sheet = workbook["Demandas"]
column_name = "QecolAlar"
#change only until the max row of the column QecoAlar
# First, find the index of column "QecolAlar
column_index = None
for col in sheet[2]:  # Check header row 2
    if col.value == column_name:
        column_index = col.column  
        break
  #find max index
# Technic : find the last row not empty of the column
last_row = 2  
for row in range(3, sheet.max_row+1): 
    if sheet.cell(row=row, column=column_index).value is not None:
        last_row = row  
# change the values of column QecoAlar with the value wanted and save it into data.xlsx to keep data_initial intact
# Update values in the column
for row in range(3, last_row + 1):
    sheet.cell(row=row, column=column_index).value = qecolAlar_value
workbook.save("data.xlsx")

#rerun the model
variables_model_uptated = vensim_model.run(params={'INITIAL TIME': 1, 'FINAL TIME': 120, 'TIME STEP': 1})
outflow_up = variables_model_uptated['SueltasAlarcón']
updated_deficit_2 = variables_model_uptated['DéfQecolAlar']


N1 = variables_model_uptated['N1']
