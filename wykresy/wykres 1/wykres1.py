import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Load data
dane_jakosc_powietrza = pd.read_csv('E:/wizualizacja/wykres 1/average_monthly_historical_measurements.csv')
dane_demograficzne = pd.read_csv('E:/wizualizacja/wykres 1/cities_residents_density.csv')

# Process data
dane_zaludnienie_najnowsze = dane_demograficzne[dane_demograficzne['date'] == dane_demograficzne['date'].max()]

# List of available air quality indicators
indikatory = ['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']

# Create Dash application
app = Dash(__name__)

app.layout = html.Div([
    dcc.Slider(
        id='year-slider',
        min=dane_jakosc_powietrza['year'].min(),
        max=dane_jakosc_powietrza['year'].max(),
        value=2024,
        marks={str(year): str(year) for year in range(dane_jakosc_powietrza['year'].min(), dane_jakosc_powietrza['year'].max() + 1)},
        step=None
    ),
    dcc.Slider(
        id='month-slider',
        min=1,
        max=12,
        value=5,
        marks={str(month): str(month) for month in range(1, 13)},
        step=None
    ),
    dcc.Dropdown(
        id='indicator-dropdown',
        options=[{'label': ind, 'value': ind} for ind in indikatory],
        value='pm25'
    ),
    dcc.Graph(id='scatter-plot')
])

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('year-slider', 'value'),
    Input('month-slider', 'value'),
    Input('indicator-dropdown', 'value')
)
def update_graph(selected_year, selected_month, selected_indicator):
    # Filter air quality data based on selected year and month
    dane_filtrowane = dane_jakosc_powietrza[(dane_jakosc_powietrza['year'] == selected_year) & (dane_jakosc_powietrza['month'] == selected_month)]
    
    # Select relevant columns
    dane_filtrowane = dane_filtrowane[['city', selected_indicator]]
    
    # Merge air quality data with demographic data
    dane_polaczone = pd.merge(dane_filtrowane, dane_zaludnienie_najnowsze, on='city')
    
    # Add population density category
    def nowa_kategoria_zaludnienia(row):
        if row['residents_per_1km2'] < 1000:
            return '<1000'
        elif 1000 <= row['residents_per_1km2'] <= 2000:
            return '1000-2000'
        else:
            return '>2000'

    dane_polaczone['Kategoria'] = dane_polaczone.apply(nowa_kategoria_zaludnienia, axis=1)
    
    # Create plot
    fig = px.scatter(dane_polaczone, x='residents_per_1km2', y=selected_indicator, color='Kategoria',
                     title=f'Jakość powietrza ({selected_indicator.upper()}) a zaludnienie w miastach Polski w {selected_month}/{selected_year}',
                     labels={'residents_per_1km2': 'Liczba mieszkańców na 1 km²', selected_indicator: selected_indicator.upper()},
                     hover_data={'city': True})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
