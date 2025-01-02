
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:49:58 2024

@author: sophi

source documentation : https://dash-bootstrap-components.opensource.faculty.ai/docs/components/accordion/
http://127.0.0.1:8050
"""
#cd C:\Users\sophi\myCloud\Sophia\Thesis\Model\Jucar_model\Adrià\App_Jucar
#streamlit run Jucar_river_basin.py
#git save

# Import libraries and modules
import pandas as pd
import numpy as np
import openpyxl
import pysd
import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

# Precompute initial graph data
workbook = openpyxl.load_workbook("data_initial.xlsx")
workbook.save("data.xlsx")
vensim_model = pysd.load('WEFE Jucar (Simple).py')
initial_qecolAlar_value = 5.18
qecolAlar_value = initial_qecolAlar_value
years_sim = 10
months = np.arange(1, (12*years_sim)+1)
variables_model_initial = vensim_model.run(params={'INITIAL TIME': 1, 'FINAL TIME': 12*years_sim, 'TIME STEP': 1})

initial_outflow = variables_model_initial['Sal Jucar']
initial_deficit = variables_model_initial['DéfQecolAlar']

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)
app.title = "Júcar River Basin Water Management"

# Define reusable page components
def create_home_page():
    return html.Div([
        html.H1("Júcar River Basin Management Tool", className="text-center mt-0"),
        html.P("Welcome to the Júcar River Basin System Dynamics Model. This tool provides an interactive platform "
               "to analyze and simulate the behavior of the Júcar River Basin under various scenarios."),
        html.H2("Content", className="mt-4"),
        html.Ul([
            html.Li("1. Model presentation - see how the model is formed"),
            html.Li("2. Explore environmental and reservoir management impacts"),
            html.Li("3. Drought management simulation"),
            html.Li("4. Monitor system performance through metrics"),
        ]),
        html.H2("User Guide", className="mt-4"),
        html.Ol([
            html.Li("Navigate using the menu on the left."),
            html.Li("Adjust variables using sliders or select different scenarios using dropdown menus."),
            html.Li("Run simulations to analyze results."),
        ])
    ])

def create_model_presentation():
    return html.Div([
        html.H1("Júcar River Basin Management Tool", className="text-center mt-0"),
        dbc.Tabs([
            dbc.Tab(label="View 1: SYSTEM NETWORK", children=[
                html.P("Overview of the model"),
                html.Img(src="/assets/View_1.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
            dbc.Tab(label="View 2", children=[
                html.P("MANCHA ORIENTAL AQUIFER"),
                html.Img(src="/assets/View_2.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
            dbc.Tab(label="View 3", children=[
                html.P("WATER DEMAND, SUPPLY AND DEFICIT"),
                html.Img(src="/assets/View_3.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
            dbc.Tab(label="View 4", children=[
                html.P("RESERVOIRS OPERATING RULES"),
                html.Img(src="/assets/View_4.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
            dbc.Tab(label="View 5", children=[
                html.P("STATE INDEX"),
                html.Img(src="/assets/View_5.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
            dbc.Tab(label="View Crops", children=[
                html.P("CROPS"),
                html.Img(src="/assets/Crops.PNG", style={"width": "80%", "margin": "auto", "display": "block"})
            ]),
        ])
    ])

def create_parameter_panel():
    return html.Div([
        html.H2("Parameter Settings", className="text-center mt-3"),
        html.P("QEcolAlar: This is the environmental flow downstream of Alarcon’s reservoir.", className="text-center ml-2"),
        
        # Radio Items for Selection
        html.Div([
            html.P("Select Input Type:", style={"text-align": "center"}),
            dbc.RadioItems(
                id="qecolAlar-selector",
                options=[
                    {"label": "Constant value", "value": "option1"},
                    {"label": "Monthly dynamic values", "value": "option2"},
                ],
                inline=True,
                value="option1",  # Default selection
                className="mb-3",
            ),
        ], className="p-4 bg-light shadow rounded", style={"text-align": "center"}),

        # Constant Input Box with Label
        html.Div([
            html.P("Set a constant Qeco", className="mb-1"),
            dbc.Input(
                type="number",
                min=0.0,
                max=10.0,
                step=0.1,
                value=initial_qecolAlar_value,
                style={"width": "100px", "text-align": "center"}
            )
        ], id="qecolAlar-constant", style={
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
            "margin-bottom": "20px",
        }),

        # Monthly Dynamic Input
        # Option 2 : Dynamic dropdown for 12 months for dynamic input
        html.Div([
            html.P("Set a Qeco for each month:", className="text-center mt-1"),
            html.Div([
                dbc.Row([
                    dbc.Col([html.Label("January"), dbc.Input(type="number", id="jan-value", value=5.0, step=0.1)], width=6),
                    dbc.Col([html.Label("February"), dbc.Input(type="number", id="feb-value", value=5.0, step=0.1)], width=6),
                ], className="mb-2"),
                dbc.Row([
                    dbc.Col([html.Label("March"), dbc.Input(type="number", id="mar-value", value=5.0, step=0.1)], width=6),
                    dbc.Col([html.Label("April"), dbc.Input(type="number", id="apr-value", value=5.0, step=0.1)], width=6),
                ], className="mb-2"),
                dbc.Row([
                    dbc.Col([html.Label("May"), dbc.Input(type="number", id="may-value", value=5.0, step=0.1)], width=6),
                    dbc.Col([html.Label("June"), dbc.Input(type="number", id="jun-value", value=5.0, step=0.1)], width=6),
                ], className="mb-2"),
                dbc.Row([
                    dbc.Col([html.Label("July"), dbc.Input(type="number", id="jul-value", value=5.0, step=0.1)], width=6),
                    dbc.Col([html.Label("August"), dbc.Input(type="number", id="aug-value", value=5.0, step=0.1)], width=6),
                ], className="mb-2"),
                dbc.Row([
                    dbc.Col([html.Label("September"), dbc.Input(type="number", id="sep-value", value=5.0, step=0.1)], width=6),
                    dbc.Col([html.Label("October"), dbc.Input(type="number", id="oct-value", value=5.0, step=0.1)], width=6),
                ], className="mb-2"),
                dbc.Row([
                    dbc.Col([html.Label("November"), dbc.Input(type="number", id="nov-value", value=5.0, step=0.1)], width=6),
                    dbc.Col([html.Label("December"), dbc.Input(type="number", id="dec-value", value=5.0, step=0.1)], width=6),
                ])
            ])
        ], id="qecolAlar-dynamic", 
            style={"display": "none", "margin-bottom": "20px","margin-top": "20px"},
            className="text-center mt-0"),

        # Run Simulation Button
        html.Div([
            dbc.Button("Run Simulation", id="run-simulation", color="primary")
        ], style={"display": "flex", "justify-content": "center", "margin-top": "20px"}),
    ], style={
        "maxWidth": "500px",
        "margin": "0 auto",
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
    }, className="p-4 bg-light shadow rounded")


        

def create_alarcon_page():
    return dbc.Container(fluid=True,children=[
        html.H1("Alarcón’s Reservoir", className="text-center mt-0"),
        dbc.Row([
            dbc.Col(create_parameter_panel(), width=3,className="bg-light border-right",),
            dbc.Col([
                dbc.Spinner(
                html.Div([
                    html.P("DéfQEcolAlar: Deficit regarding the environmental flow."),
                    dcc.Graph(
                        id="outflow-graph",
                        figure={
                            "data": [go.Scatter(x=months, y=initial_outflow, mode="lines", name="Outflow")],
                            "layout": go.Layout(title="Outflow Over Time", xaxis={"title": "Months"}, yaxis={"title": "hm³"})
                        }),
                    dcc.Graph(
                        id="deficit-graph",
                        figure={
                            "data": [go.Scatter(x=months, y=initial_deficit, mode="lines", name="Deficit")],
                            "layout": go.Layout(title="Deficit Over Time (DéfQEcolAlar)", xaxis={"title": "Months"}, yaxis={"title": "hm³"})
                        }),
                ]))
            ], width=9),
        ])
    ])

def create_population_growth_page():
    return dbc.Container(fluid=True, children=[
        html.H1("Population Growth Analysis", className="text-center mt-0"),
        dbc.Row([
            dbc.Col(create_parameter_panel(), width=3, className="bg-light border-right"),
            dbc.Col([
                dbc.Spinner(
                    html.Div([
                        html.P("Population Growth Dynamics: Analyze how population growth impacts resource demand."),
                        dcc.Graph(
                            id="population-growth-graph",
                            figure={
                                "data": [go.Scatter(x=months, y=np.random.rand(len(months)) * 1000, mode="lines", name="Population")],
                                "layout": go.Layout(title="Population Growth Over Time", xaxis={"title": "Months"}, yaxis={"title": "Population (Thousands)"})
                            }
                        ),
                        dcc.Graph(
                            id="resource-demand-graph",
                            figure={
                                "data": [go.Scatter(x=months, y=np.random.rand(len(months)) * 500, mode="lines", name="Resource Demand")],
                                "layout": go.Layout(title="Resource Demand Over Time", xaxis={"title": "Months"}, yaxis={"title": "Demand (Units)"})
                            }
                        ),
                    ])
                )
            ], width=9),
        ])
    ])


# Navigation menu
def create_menu():
    return html.Div(
        dbc.ListGroup(
            [
                dbc.ListGroupItem("Home", href="/", active="exact"),
                dbc.ListGroupItem("Model presentation", href="/model", active="exact"),
                dbc.ListGroupItem("Alarcón’s Reservoir", href="/alarcon", active="exact"),
                dbc.ListGroupItem("Population Growth", href="/population-growth", active="exact"),
            ],
        ),
        style={"width": "250px", "position": "fixed", "left": "0", "top": "0", "background-color": "#f8f9fa", "padding": "45px 10px", "box-shadow": "2px 0 5px rgba(0,0,0,0.1)"}
    )

# Update page routing
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def update_page(pathname):
    if pathname == "/":
        return create_home_page()
    elif pathname == "/model":
        return create_model_presentation()
    elif pathname == "/alarcon":
        return create_alarcon_page()
    elif pathname == "/population-growth":
        return create_population_growth_page()
    return html.Div("404: Page Not Found")
# Layout
# app.layout = html.Div([
#     dbc.Button("Menu", id="menu-toggle", color="primary", className="mb-2", style={"position": "fixed", "top": "10px", "left": "10px", "zIndex": 1000}),
#     dbc.Collapse(
#         create_menu(),
#         id="menu-collapse",
#         is_open=False,
#     ),
#     html.Div(
#         [dcc.Location(id="url"), html.Div(id="page-content", style={"padding": "20px"})],
#         id="main-content",
#         style={"margin-left": "0px", "transition": "margin-left 0.3s ease"}
#     )
# ])
app.layout = html.Div([
    dbc.Button("Menu", id="menu-toggle", color="primary", className="mb-2", style={"position": "fixed", "top": "10px", "left": "10px", "zIndex": 1000}),
    dbc.Collapse(create_menu(), id="menu-collapse", is_open=False),
    html.Div([
        dcc.Location(id="url"),
        html.Div(id="page-content", style={"padding": "20px"})
    ], id="main-content", style={"margin-left": "0px", "transition": "margin-left 0.3s ease"})
])


@app.callback(
    [Output("menu-collapse", "is_open"),# Control the is_open state of the Collapse
     Output("main-content", "style")],
    [Input("menu-toggle", "n_clicks")],# Triggered when the toggle button is clicked
    [State("menu-collapse", "is_open")], # Store the current state of the Collapse
)
def toggle_menu(n_clicks, is_open):
    if n_clicks:
        if not is_open:
            return True, {"margin-left": "250px", "transition": "margin-left 0.3s ease"}
        return False, {"margin-left": "0px", "transition": "margin-left 0.3s ease"}
    return is_open, {"margin-left": "0px", "transition": "margin-left 0.3s ease"}


#selection of slider_value
@app.callback(
    [Output("qecolAlar-constant", "style"),
     Output("qecolAlar-dynamic", "style"),
     Output("run-simulation", "style")],
    Input("qecolAlar-selector", "value")
)


def toggle_input(input_type):
    if input_type == "option1":
        # Show dropdown constant, hide dropdown monthly
        return {"display": "block"}, {"display": "none"}, {"display": "block", "margin-bottom": "20px"}
    elif input_type == "option2":
        # Show dropdown, hide slider
        return {"display": "none"}, {"display": "block", "margin-bottom": "20px","margin-top": "20px"} ,{"display": "block", "margin-bottom": "20px"}
    # If no option is selected, hide both
    return {"display": "none"}, {"display": "none"},{"display": "none"}

@app.callback(
    [Output("outflow-graph", "figure"),
      Output("deficit-graph", "figure")],
    [State("qecolAlar-selector", "value"),  # Determines input type
      State("qecolAlar-constant", "value"),   # Constant value
      State("qecolAlar-dynamic", "value")],  # Dynamic value
    [Input("run-simulation", "n_clicks")],  # Button click to trigger
    prevent_initial_call=True
)


def update_Alarcon_graphs(input_type, slider_value,dropdown_value, n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate  # Prevent callback if no clicks
    # Determine input value
    if input_type == "slider" :
        qecolAlar_value = slider_value 
    else :
        qecolAlar_value = dropdown_value
        
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
    for row in range(3, last_row + 1):
        sheet.cell(row=row, column=column_index).value = qecolAlar_value
    workbook.save("data.xlsx")

    #rerun the model
    vensim_model = pysd.load('WEFE Jucar (Simple).py')
    variables_model = vensim_model.run(params={'INITIAL TIME': 1, 'FINAL TIME': 12*years_sim, 'TIME STEP': 1})
    updated_outflow = variables_model['Sal Jucar']
    updated_deficit = variables_model['DéfQecolAlar']

    
    outflow_figure = {
        "data": [
            go.Scatter(x=months, y=initial_outflow, mode="lines", name=f"Initial Outflow (QecoAlar = {initial_qecolAlar_value})", line=dict(dash="dot")),
            go.Scatter(x=months, y=updated_outflow, mode="lines", name=f"Updated Outflow (QecoAlar = {qecolAlar_value})")
        ],
        "layout": go.Layout(title="Outflow Over Time", xaxis={"title": "Months"}, yaxis={"title": "hm³"})
    }
    deficit_figure = {
        "data": [go.Scatter(x=months, y=initial_deficit, mode="lines", name=f"initial Deficit (QecoAlar ={initial_qecolAlar_value})",line=dict(dash="dot")),
                go.Scatter(x=months, y=updated_deficit, mode="lines", name=f"Uptated Deficit(QecoAlar ={qecolAlar_value})")],

        "layout": go.Layout(title="Deficit Over Time", xaxis={"title": "Months"}, yaxis={"title": "hm³"})
    }

    return outflow_figure, deficit_figure

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
