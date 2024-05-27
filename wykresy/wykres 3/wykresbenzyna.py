import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Załaduj dane
dane_jakosc_powietrza = pd.read_csv('E:/wizualizacja/wykres 1/average_monthly_historical_measurements.csv')
dane_samochody = pd.read_csv(r'E:/wizualizacja/wykres 3/cars_number_benzyna.csv')

# Przetwarzanie danych
dane_zaludnienie_najnowsze = dane_samochody[dane_samochody['date'] == dane_samochody['date'].max()]

# Sprawdzenie struktury danych
print(dane_jakosc_powietrza.head())
print(dane_samochody.head())

# Lista dostępnych wskaźników jakości powietrza
indikatory = ['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']

# Tworzenie aplikacji Dash
app = Dash(__name__)

app.layout = html.Div([
    dcc.Slider(
        id='year-slider',
        min=2015,
        max=2022,
        value=2022,
        marks={str(year): str(year) for year in range(2015, 2023)},
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
    Input('indicator-dropdown', 'value')
)
def update_graph(selected_year, selected_indicator):
    # Filtrowanie danych jakości powietrza na podstawie wybranego roku i 1. miesiąca
    dane_filtrowane = dane_jakosc_powietrza[(dane_jakosc_powietrza['year'] == selected_year) & (dane_jakosc_powietrza['month'] == 1)]
    
    # Wybranie interesujących kolumn
    dane_filtrowane = dane_filtrowane[['city', selected_indicator]]
    
    # Połączenie danych jakości powietrza z danymi o samochodach
    dane_polaczone = pd.merge(dane_filtrowane, dane_zaludnienie_najnowsze, on='city')
    
    # Dodanie kategorii liczby samochodów
    def nowa_kategoria_zaludnienia(row):
        if row['no_of_cars'] < 30000:
            return '<30000'
        elif 30000 <= row['no_of_cars'] <= 50000:
            return '30000-50000'
        else:
            return '>50000'

    dane_polaczone['Kategoria'] = dane_polaczone.apply(nowa_kategoria_zaludnienia, axis=1)
    
    # Tworzenie wykresu z jawnym przypisaniem kolorów do kategorii
    fig = px.scatter(
        dane_polaczone, 
        x='no_of_cars', 
        y=selected_indicator, 
        color='Kategoria',
        color_discrete_map={
            '<30000': 'blue', 
            '30000-50000': 'green', 
            '>50000': 'red'
        },
        title=f'Jakość powietrza ({selected_indicator.upper()}) a liczba samochodów w miastach Polski w 01/{selected_year}',
        labels={'no_of_cars': 'Liczba samochodów benzyna', selected_indicator: selected_indicator.upper()}
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
