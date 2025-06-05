import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import argparse
import threading
import time
import os

app = dash.Dash(__name__)

DATA_FILE = "results/simulation_log.csv"

def serve_layout():
    df = pd.read_csv(DATA_FILE, parse_dates=['timestamp'])
    return html.Div([
        html.H1("📈 QuantRush Real-Time Dashboard"),
        dcc.Graph(id='pnl-graph'),
        dcc.Graph(id='inventory-graph'),
        dcc.Interval(id='interval-component', interval=5000, n_intervals=0)
    ])

@app.callback(
    Output('pnl-graph', 'figure'),
    Output('inventory-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graphs(n):
    df = pd.read_csv(DATA_FILE, parse_dates=['timestamp'])

    pnl_fig = px.line(df, x='timestamp', y='pnl', title='PnL Over Time')
    inv_fig = px.line(df, x='timestamp', y='inventory', title='Inventory Over Time')

    return pnl_fig, inv_fig

app.layout = serve_layout

def run_dashboard(port):
    app.run_server(debug=False, port=port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    run_dashboard(args.port)
