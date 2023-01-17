import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
spacex_df = pd.read_csv('spacex_launch_dash.csv')
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
    style={'textAlign': 'center', 'color': '#363650', 'font-size': 50}),
    dcc.Dropdown(id='site-dropdown',
    options=[{'label': 'All Sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}], 
    value='ALL', placeholder="Select a Launch Site here",
    searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
    min=0, max=10000, step=1000, value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]),
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'), 
Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    clean_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Success for all launch sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        clean_df=spacex_df[spacex_df['Launch Site']==entered_site]
        clean_df=clean_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(clean_df,values='class count',names='class',title=f"Total Success Launches for site {entered_site}")
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
[Input(component_id='site-dropdown',component_property='value'),
Input(component_id='payload-slider',component_property='value')])

def scatter(entered_site,payload):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
    # thought reusing filtered_df may cause issues, but tried it out of curiosity and it seems to be working fine
    if entered_site=='ALL':
        fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Success count on Payload mass for all sites')
        return fig
    else:
        fig=px.scatter(filtered_df[filtered_df['Launch Site']==entered_site],
        x='Payload Mass (kg)',y='class',color='Booster Version Category',
        title=f"Success count on Payload mass for site {entered_site}")
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
