# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash import dash_table 
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
spacex_df['Outcome Label'] = spacex_df['class'].map({1: 'Success', 0: 'No Success'})


# Get unique values from the 'Launch Site' column
# unique_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif'},
                    children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                            html.Img(src='https://live.staticflickr.com/65535/48380511427_eeafd03bd7_k.jpg', style={'height': '150px', 'marginTop': '10px'}),  # Image with 40px height
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),  # A line break
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL',
                                    placeholder='Select a Launch Site',
                                    searchable=True
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),

                                #Extra: Adding the CSV table:
                                dash_table.DataTable(
                                    id='launch-data-table',
                                    columns=[{"name": col, "id": col} for col in spacex_df.columns], 
                                    data=spacex_df.to_dict('records'), 
                                    page_size=10, 
                                    style_table={'overflowX': 'auto'}, 
                                    style_cell={'textAlign': 'left'},
                                )

                                ]
                                #style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}
                                )

                                

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # All sites selected: show total success counts
        pie_data = spacex_df.groupby('Outcome Label').size().reset_index(name='counts')
        fig = px.pie(
            pie_data,
            values='counts',
            names='Outcome Label',
            title='Success Launches Rate for All Sites'
        )
    else:
        # Filter for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        pie_data = filtered_df.groupby('Outcome Label').size().reset_index(name='counts')
        fig = px.pie(
            pie_data,
            values='counts',
            names='Outcome Label',
            title=f'Success vs Failure Launches Rate for Site {entered_site}'
        )

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            Input(component_id='payload-slider', component_property='value'),
            Input(component_id='site-dropdown', component_property='value'))

def get_scatter_plot(payload_range,entered_site):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Outcome for All Sites',
            labels={'class': 'Launch Outcome'}
        )
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Outcome for {entered_site}',
            labels={'class': 'Launch Outcome'}
        )
    return fig

@app.callback(
    Output(component_id='launch-data-table', component_property='data'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])
def update_table(entered_site, payload_range):
    # Filter data based on payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    if entered_site == 'ALL':
        # Return data for all sites within the payload range
        return filtered_df.to_dict('records')
    else:
        # Filter data for the selected site within the payload range
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        return filtered_df.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server()
