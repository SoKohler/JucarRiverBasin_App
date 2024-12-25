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

import plotly.express as px
import dash_bootstrap_components as dbc
import time
import plotly.graph_objs as go

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


#Deficit and Output Alarcon
#DéfQecolAlar = variables_model["DéfQecolAlar"]


### 2.Test change QecolAlar (environmental flow downstream of Alarcon’s reservoir) = constant value
#QecolAlar = data_Demandas["QecolAlar"]

### 3. APP - DASH

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Júcar River Basin Management"

# Layout
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Menu", className="text-white bg-dark text-center py-3"),
            dbc.ListGroup([
                dbc.ListGroupItem("Home", href="/", active="exact", className="text-dark"),
                dbc.ListGroupItem("Alarcón’s Reservoir", href="/alarcon", active="exact", className="text-dark"),
            ], flush=True),
            html.Div([
                html.H4("Adjust QecolAlar", className="text-center mt-4"),
                dcc.Slider(id="qecolAlar-slider", min=0.0, max=10.0, step=0.01, value=5.184, marks={i: str(i) for i in range(11)}),
                dbc.Button("Run Simulation", id="run-simulation", color="primary", className="mt-3 w-100"),
            ], className="p-3"),
        ], className="shadow-sm", style={"height": "100vh", "background-color": "#f8f9fa"}), width=2),
        dbc.Col([dcc.Location(id="url"), dbc.Spinner(html.Div(id="page-content", style={"padding": "20px"}))], width=10),
    ], className="g-0"),
])

# Home Page
def home_page():
    return html.Div([
        html.H1("Júcar River Basin Management Tool", className="mb-4 text-center"),
        dbc.Tabs([
            dbc.Tab(html.Div([
                html.H3("Overview"),
                html.P("Simulate water flows, reservoir levels, and drought conditions to analyze management impacts."),
                html.H3("Key Features"),
                html.Ul([html.Li("Visualize Dynamics"), html.Li("Interactive Variables"), html.Li("Performance Indicators")]),
                html.Img(src="/assets/View_1.PNG", style={"width": "80%", "display": "block", "margin": "auto", "border-radius": "10px"}, alt="Júcar River Basin Visualization",),
            ]), label="Overview"),
            dbc.Tab(html.Div([
                html.H3("View 1"),
                html.P("Simulate water flows, reservoir levels, and drought conditions to analyze management impacts."),
                html.H3("Key Features"),
                html.Ul([html.Li("Visualize Dynamics"), html.Li("Interactive Variables"), html.Li("Performance Indicators")]),
                html.Img(src="/assets/View_2.PNG", style={"width": "80%", "display": "block", "margin": "auto", "border-radius": "10px"}, alt="Júcar River Basin Visualization",),
            ]), label="Overview"),
        ])
    ])

# Alarcón Page
def alarcon_page(qecolAlar_value=None):
    if qecolAlar_value is not None:
        time.sleep(2)     
        # Charger le fichier Excel
        workbook = openpyxl.load_workbook("data_initial.xlsx")
        # Sélectionner la feuille sur laquelle travailler
        sheet = workbook["Demandas"]
        # Spécifiez le nom de la colonne
        column_name = "QecolAlar"  # Remplacez par le nom de votre colonne
        # Rechercher la colonne correspondant au nom (ligne 2)
        column_letter = None
        for col in sheet.iter_cols(min_row=2, max_row=2):  # Itérer sur la ligne 2
            if col[0].value == column_name:  # Si la valeur correspond au nom de la colonne
                column_letter = col[0].column_letter  # Obtenir la lettre de la colonne
                break
        if column_letter is None:
            print(f"Colonne avec le nom '{column_name}' non trouvée.")
        else:
            # Modifier les valeurs en dessous de la ligne 2
            for row in range(3, sheet.max_row + 1):  # Commence à la ligne 3
                cell = sheet[f"{column_letter}{row}"]
                cell.value = qecolAlar_value  # Remplacez par la valeur souhaitée
        
            # Enregistrer les modifications dans un nouveau fichier
            workbook.save("data.xlsx")
            print("Les valeurs ont été mises à jour.")

        months = np.arange(1,121)
        variables_model = vensim_model.run(params={'INITIAL TIME': 1, 'FINAL TIME': 120, 'TIME STEP': 1})
        return html.Div([
            html.H1("Alarcón’s Reservoir Results", className="mb-4 text-center"),
            dcc.Graph(figure={"data": [go.Scatter(x=months, y=variables_model['Sal Jucar'], mode="lines", name="Outflow")],
                              "layout": go.Layout(title="Outflow", xaxis={"title": "Months"}, yaxis={"title": "hm³"})}),
            dcc.Graph(figure={"data": [go.Scatter(x=months, y=variables_model['DéfQecolAlar'], mode="lines", name="Deficit")],
                              "layout": go.Layout(title="Deficit", xaxis={"title": "Months"}, yaxis={"title": "hm³"})}),
        ])
    return html.Div([
        html.H1("Alarcón’s Reservoir Page", className="mb-4 text-center"),
        html.H3("Adjust the slider and run the simulation to see results."),
    ])

# Callback
@app.callback(Output("page-content", "children"), 
              [Input("url", "pathname"), Input("qecolAlar-slider", "value"), Input("run-simulation", "n_clicks")])
def display_page(pathname, qecolAlar_value, n_clicks):
    if pathname == "/": return home_page()
    if pathname == "/alarcon": return alarcon_page(qecolAlar_value) if n_clicks else alarcon_page()
    return html.Div("404: Page Not Found")

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
