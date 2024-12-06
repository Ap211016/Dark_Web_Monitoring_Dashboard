# Dark Web Monitoring Dashboard

The Dark Web Monitoring Dashboard is a Python-based application built using Dash. It provides an interactive platform to visualize and analyze keyword monitoring data from Excel files. After monitoring results are generated and saved as Excel files, users can upload them to the dashboard, which will display key statistics and visualizations like pie charts, bar charts, and a detailed data table for findings.

## Features

- **Upload Multiple Excel Files**: Upload multiple Excel files containing keyword monitoring data.
- **Visualizations**:
  - **Pie Chart**: Displays the success rate of keywords based on findings.
  - **Bar Charts**: Visualizes the number of findings over time and the frequency of all keywords.
  - **Data Table**: Displays raw data in an interactive table format.
- **Date Range Filter**: Filter findings based on a specified date range to analyze trends over time.
- **Statistics**: Displays the total number of findings, unique keywords, monitored URLs, and found keywords.

## Prerequisites

Ensure you have the following installed:
- **Python 3.x**: Make sure Python is installed on your machine.
- **Libraries**: You can install the necessary libraries by running:

```bash
pip install dash pandas plotly dash-bootstrap-components dash-daq
```

## Running the Application

- Clone the Repository:
```bash
git clone https://github.com/Ap211016/Dark_Web_Monitoring_Dashboard
cd Dark_Web_Monitoring_Dashboard
```
## Run the App: Run the following command to start the Dash app:
```bash
python app.py
```
- Access the Dashboard: Open a web browser and go to http://127.0.0.1:8050/ to access the Dark Web Monitoring Dashboard.
