python
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
data_path = 'Distribution of Pensioners 2022.xlsx'
data = pd.read_excel(data_path)

data['Quarter'] = 'Q' + data['Quarter'].astype(str)

dashboard = dash.Dash(__name__)
app_layout = html.Div([
    html.H1("Pensioners Distribution Dashboard for Abu Dhabi 2022"),
    html.Div([
        html.Label("Select Quarter:"),
        dcc.Dropdown(
            id='quarter-dropdown',
            options=[{'label': quarter, 'value': quarter} for quarter in data['Quarter'].unique()],
            value=data['Quarter'].unique()[0]
        )
    ]),
    dcc.Graph(id='pensioners-distribution-chart'),
    html.Label("Download Data: "),
    html.A("Download Excel File", href="/download_excel", download="Pensioners_Distribution_2022.xlsx")
])

dashboard.layout = app_layout

@dashboard.callback(
    Output('pensioners-distribution-chart', 'figure'),
    [Input('quarter-dropdown', 'value')]
)
def update_chart(selected_quarter):
    filtered_data = data[data['Quarter'] == selected_quarter]
    fig = px.bar(filtered_data, x='Gender', y='Count', title=f"Pensioners Distribution in {selected_quarter}")
    return fig

if __name__ == '__main__':
    dashboard.run_server(debug=True)
