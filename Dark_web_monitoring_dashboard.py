import os
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import io
import base64
import plotly.graph_objects as go
from datetime import datetime
import dash_daq as daq
import json

# Constants
REQUIRED_COLUMNS = ["Keyword", "URL", "Findings", "Link Response", "Time", "Date"]

# Initialize the Dash app with dark mode using the Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Dark Web Monitoring Dashboard"

# Function to clean and standardize column names
def clean_column_names(df):
    """Standardize column names to ensure they match the expected ones."""
    df.columns = [col.strip().lower() for col in df.columns]  # Remove extra spaces and lowercase all names
    column_mapping = {
        'keyword': 'Keyword',
        'link': 'URL',  # Map 'link' to 'URL'
        'findings': 'Findings',
        'link response': 'Link Response',
        'time': 'Time',
        'date': 'Date'
    }
    df = df.rename(columns=column_mapping)
    return df

# Function to process uploaded files
def process_uploaded_files(contents):
    """Process the uploaded Excel files and return a combined DataFrame."""
    data_frames = []
    for content in contents:
        # Decode the uploaded file
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_excel(io.BytesIO(decoded))
            print(f"File loaded successfully with {len(df)} rows. Columns: {df.columns.tolist()}")  # Debugging line
            # Clean and standardize column names
            df = clean_column_names(df)
            if all(col in df.columns for col in REQUIRED_COLUMNS):
                data_frames.append(df[REQUIRED_COLUMNS])
            else:
                print("Uploaded file does not contain required columns.")
        except Exception as e:
            print(f"Error processing the uploaded file: {e}")
    
    if data_frames:
        return pd.concat(data_frames, ignore_index=True)
    else:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

# Dashboard layout with enhanced styles
app.layout = html.Div([
    # Header section with title centered
    html.Div([
        html.H2("Dark Web Monitoring Dashboard", style={'color': '#F8F9FA', 'textAlign': 'center', 'padding': '20px', 'fontWeight': 'bold'})
    ], style={'backgroundColor': '#343A40', 'marginBottom': '30px'}),  # Header styling with center alignment

    # Statistics section with Bootstrap cards
    html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H3("Total Findings: ", id="total-findings", className="card-text", style={'color': 'white', 'textAlign': 'center'}),
                    ]), color="primary", inverse=True, style={'borderRadius': '10px', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)'}
                ),
                width=3
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H3("Unique Keywords: ", id="unique-keywords", className="card-text", style={'color': 'white', 'textAlign': 'center'}),
                    ]), color="success", inverse=True, style={'borderRadius': '10px', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)'}
                ),
                width=3
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H3("Monitored URLs: ", id="monitored-urls", className="card-text", style={'color': 'white', 'textAlign': 'center'}),
                    ]), color="warning", inverse=True, style={'borderRadius': '10px', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)'}
                ),
                width=3
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H3("Found Keywords: ", id="found-keyword-count", className="card-text", style={'color': 'white', 'textAlign': 'center'}),
                    ]), color="danger", inverse=True, style={'borderRadius': '10px', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)'}
                ),
                width=3
            ),
        ], style={"marginBottom": "20px"}),

        # Date Picker for selecting the date range
        dbc.Row([
            dbc.Col(dcc.DatePickerRange(
                id="date-picker-range",
                start_date=datetime(2020, 1, 1).date(),
                end_date=datetime.today().date(),
                display_format='YYYY-MM-DD',
                style={'width': '100%'}
            ), width=6),
        ], style={"marginBottom": "20px"}),
    ]),

    # File upload component - Button styled to be clickable (not a whole bar)
    html.Div([
        dcc.Upload(
            id="upload-data",
            children=html.Button("Upload Excel Files", style={
                'backgroundColor': '#007bff', 
                'color': 'white', 
                'border': 'none', 
                'padding': '10px 20px', 
                'borderRadius': '5px', 
                'cursor': 'pointer',
                'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',  # Adding shadow for 3D effect
                'transition': 'all 0.3s ease-in-out'  # Smooth transition effect
            }),
            multiple=True
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        
    # Loading Spinner and content display
    dcc.Loading(
        id="loading",
        type="circle",
        children=[
            # Findings Over Time Chart
            dcc.Graph(id="findings-over-time", style={"height": "400px", "backgroundColor": "#343A40", 'borderRadius': '15px'}),

            # Frequency of All Keywords (Bar chart with color gradient)
            dcc.Graph(id="keyword-frequency", style={"height": "400px", "backgroundColor": "#343A40", 'borderRadius': '15px'}),

            # Keyword Success Rate (Pie chart)
            dcc.Graph(id="success-frequency", style={"height": "400px", "backgroundColor": "#343A40", 'borderRadius': '15px'}),

            # Data Table displaying the raw data
            dash_table.DataTable(
                id="data-table",
                style_table={'height': '500px', 'overflowY': 'auto', 'borderRadius': '15px'},
                style_cell={'color': 'white', 'backgroundColor': '#343A40', 'textAlign': 'center'},
                style_header={'backgroundColor': '#495057', 'color': 'white', 'fontWeight': 'bold'},
                style_data_conditional=[
                    {
                        'if': {'state': 'active'},
                        'backgroundColor': '#007bff',
                        'color': 'white',
                    }
                ],
            ),
        ]
    )
])

# Callback for updating the dashboard based on uploaded files
@app.callback(
    [
        Output("total-findings", "children"),
        Output("unique-keywords", "children"),
        Output("monitored-urls", "children"),
        Output("found-keyword-count", "children"),
        Output("findings-over-time", "figure"),
        Output("keyword-frequency", "figure"),
        Output("success-frequency", "figure"),
        Output("data-table", "data"),
    ],
    [
        Input("upload-data", "contents"),
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
    ]
)
def update_dashboard(contents, start_date, end_date):
    # Check if the files are uploaded
    if contents is None:
        raise PreventUpdate

    # Process the uploaded files and load them into a dataframe
    data = process_uploaded_files(contents)

    # Convert 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Filter data based on date range
    filtered_data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]

    # Total Findings
    total_findings = len(filtered_data)

    # Unique Keywords
    unique_keywords = len(filtered_data['Keyword'].unique())

    # Monitored URLs
    monitored_urls = len(filtered_data['URL'].unique())

    # Correctly calculate Found Keywords based on presence of 'Keyword found' in the Findings column
    found_keywords = filtered_data[filtered_data['Findings'].str.contains("Keyword found", case=False, na=False)]
    found_keyword_count = len(found_keywords)

    # Findings Over Time (Bar chart)
    findings_over_time = filtered_data.groupby(['Date']).size().reset_index(name='Findings Count')
    findings_fig = px.bar(
        findings_over_time, 
        x='Date', 
        y='Findings Count', 
        title="Findings Over Time", 
        template="plotly_dark", 
        color='Findings Count', 
        color_continuous_scale="Viridis"
    )

    # Keyword Frequency (Bar chart for all keywords, regardless of findings)
    keyword_data = filtered_data['Keyword'].value_counts().reset_index()
    keyword_data.columns = ['Keyword', 'Frequency']
    keyword_frequency_fig = px.bar(
        keyword_data, 
        x='Keyword', 
        y='Frequency', 
        title="Keyword Frequency (All)", 
        template="plotly_dark", 
        color='Frequency',
        color_continuous_scale="Viridis"
    )

    # Keyword Success Rate (Pie chart showing only found keywords)
    success_counts = found_keywords.groupby('Keyword').size().reset_index(name='Count')
    success_fig = px.pie(
        success_counts, 
        names='Keyword', 
        values='Count', 
        title="Keyword Success Rate", 
        template="plotly_dark"
    )

    # Convert DataFrame to dictionary for DataTable
    table_data = filtered_data.to_dict('records')

    return (
        f"Total Findings: {total_findings}", 
        f"Unique Keywords: {unique_keywords}", 
        f"Monitored URLs: {monitored_urls}", 
        f"Found Keywords: {found_keyword_count}",
        findings_fig, 
        keyword_frequency_fig, 
        success_fig, 
        table_data
    )

if __name__ == "__main__":
    app.run_server(debug=True)
