# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:49:58 2024

@author: sophi

source documentation : https://dash-bootstrap-components.opensource.faculty.ai/docs/components/accordion/
http://127.0.0.1:8050
git add .
git commit -m "Updated app functionality"
git pushinst

"""
#cd C:\Users\sophi\myCloud\Sophia\Thesis\Model\Jucar_model\Adrià\App_Jucar
#run Jucar_river_basin_APP.py
#git save

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
from dash import Dash, dcc, html, Input, Output, callback,State
import dash_bootstrap_components as dbc # to make the app visually appealing 
import plotly.graph_objs as go # to create interactive graphs
import time

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
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True) # pre-built Bootstrap theme (YETI OR FLATY)  https://bootswatch.com/yeti/
app.title = "Júcar River Basin Water Management"

### 3. Define Reusable Functions
# Function to create the Home page
def create_home_page():
    """Generate the content for the home page."""
    return html.Div([
        html.H1("Júcar River Basin Management Tool", className="text-center my-4"),
        html.P(
            "Welcome to the Júcar River Basin System Dynamics Model. "
            "This tool provides an interactive platform to analyze and simulate "
            "the behavior of the Júcar River Basin system under various scenarios."
        ),
        html.H2("Content", className="mt-4"),
        html.Ul([
            html.Li("1. Model presentation - see how the model is formed"),
            html.Li("2. "),
            html.Li("3. Drought management simulation."),
            html.Li("4. Monitor system performance through metrics."),
        ]),
        html.H2("User guide", className="mt-4"),
        html.Ol([
            html.Li("Navigate using the menu on the left. There are multiple scenarios and possible analysis to play with."),
            html.Li("In each page, you can adjust variables using sliders or select different scenario using the dropdown menus."),
            html.Li("Run simulations to analyze results."),
        ])
    ])


def create_model_presentation():
    return html.Div([
        html.H1("Júcar River Basin Management Tool", className="text-center my-4"),
        #TABS
        dbc.Tabs([
            dbc.Tab(label="View 1 : SYSTEM NETWORK", children=[
                html.P("Overview of the model"),
                html.Img(src="/assets/View_1.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
            dbc.Tab(label="View 2 : MANCHA ORIENTAL AQUIFER", children=[
                html.P("Explore reservoir and environmental management impacts."),
                html.Img(src="/assets/View_2.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
            dbc.Tab(label="View 3 : WATER DEMAND, SUPPLY AND DEFICIT", children=[
                html.P("Explore reservoir and environmental management impacts."),
                html.Img(src="/assets/View_3.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
            dbc.Tab(label="View 4 : RESERVOIRS OPERATING RULES", children=[
                html.P("Explore reservoir and environmental management impacts."),
                html.Img(src="/assets/View_4.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
            dbc.Tab(label="View 5 : STATE INDEX", children=[
                html.P("Explore reservoir and environmental management impacts."),
                html.Img(src="/assets/View_5.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
            dbc.Tab(label="CROPS", children=[
                html.P("Explore reservoir and environmental management impacts."),
                html.Img(src="/assets/Crops.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
        ])
    ])
# Function to create the Alarcón Reservoir page
def create_alarcon_page(qecolAlar_value=5.18):
    """Generate the Alarcón Reservoir page with simulation logic."""
    # Default value handling
    if qecolAlar_value is None:
        qecolAlar_value = 5.18  # Default value
    # Simulate Vensim model run with updated slider value
    workbook = openpyxl.load_workbook("data_initial.xlsx")
    sheet = workbook["Demandas"]
    column_name = "QecolAlar"
    for col in sheet.iter_cols(min_row=2, max_row=2):
        if col[0].value == column_name:
            for row in range(3, sheet.max_row + 1):
                sheet[f"{col[0].column_letter}{row}"].value = qecolAlar_value
            break
    workbook.save("data.xlsx")
    # Run the Vensim model with the updated value
    variables_model = vensim_model.run(params={'INITIAL TIME': 1, 'FINAL TIME': 120, 'TIME STEP': 1})
    months = np.arange(1, 121)
    # Page layout with slider and results
    control_section = html.Div([
        html.H5("Adjust QecolAlar", className="text-center mt-4"),
             dcc.Slider(id="qecolAlar-slider",min=0.0,max=10.0,step=0.01,value=qecolAlar_value,marks={i: str(i) for i in range(11)}),
             dbc.Button("Run Simulation", id="run-simulation", color="primary", className="mt-3 w-100")
        ], className="p-3")
    result_section = html.Div([
        html.H1("Simulation Results", className="text-center my-4"),
        dcc.Graph(figure={
            "data": [go.Scatter(x=months, y=variables_model['Sal Jucar'], mode="lines", name="Outflow")],
            "layout": go.Layout(title="Outflow Over Time", xaxis={"title": "Months"}, yaxis={"title": "hm³"})
        }),
        dcc.Graph(figure={
            "data": [go.Scatter(x=months, y=variables_model['DéfQecolAlar'], mode="lines", name="Deficit")],
            "layout": go.Layout(title="Deficit Over Time", xaxis={"title": "Months"}, yaxis={"title": "hm³"})
        })
    ])
    collapse = html.Div([
        dbc.Button("Open collapse", id="collapse-button", className="mb-3", color="primary", n_clicks=0,),
        dbc.Collapse(dbc.Card(dbc.CardBody("This content is hidden in the collapse")), id="collapse", is_open=False,),
    ])
    return html.Div([
        html.H1("Alarcón’s Reservoir", className="text-center my-4"),
        collapse,
        html.Img(src="/assets/Qeco.JPG", style={"width": "80%", "margin": "auto", "display": "block"}),
        html.Img(src="/assets/Output.JPG", style={"width": "80%", "margin": "auto", "display": "block"}),
        html.Img(src="/assets/QecoAlar_tree.jpg", style={"width": "80%", "margin": "auto", "display": "block"}),
        html.P("Use the slider and run the simulation."),
        control_section,
        result_section
    ])


### 4. App Layout
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Menu", className="bg-dark text-white text-center py-3"),
                dbc.ListGroup([
                    dbc.ListGroupItem("Home", href="/", active="exact", className="text-dark"),
                    dbc.ListGroupItem("Model presentation", href="/model", active="exact", className="text-dark"),
                    dbc.ListGroupItem("Alarcón’s Reservoir", href="/alarcon", active="exact", className="text-dark"),
                ]),
            ], className="shadow-sm", style={"height": "100vh"}), width=2
        ),
        dbc.Col(
            [dcc.Location(id="url"), html.Div(id="page-content", style={"padding": "20px"})],
            width=10
        )
    ])
])

### 5. Callbacks
#for page content
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
    prevent_initial_call=True , # Prevent callback from triggering prematurely
)
def update_page(pathname, qecolAlar_value=None, n_clicks=None):    
    if pathname == "/": 
        return create_home_page()
    if pathname == "/model": 
        return create_model_presentation()
    if pathname == "/alarcon":
        return create_alarcon_page()
    return html.Div("404: Page Not Found")
#for collapse
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")]
)
def collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open  #change to collapse state
    return is_open  #nothing change the current state unchanged

#6.running the APP
if __name__ == "__main__":
    app.run_server(debug=True) # add port to use is on any free port

