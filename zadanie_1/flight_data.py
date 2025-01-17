import pandas as pd
import matplotlib.pyplot as plt
import requests

# Zaimportuj funkcje z pliku database.py
from zadanie_1.database import save_to_db, load_flight_data

def fetch_flight_data(databasefile="flights.db"):
    """
    Pobiera dane z OpenSky Network API dla obszaru ATL ± 100 km,
    przekształca je do obiektu DataFrame i zapisuje w bazie danych.
    """
    # Współrzędne ATL (Atlanta) w stopniach: ±100 km
    lon_min, lat_min = -85.4277, 32.6407
    lon_max, lat_max = -83.4277, 34.6407

    # Dane do autentykacji w OpenSky Network
    user_name = 'dwfdfWEFDWFF'   # login
    password = 'SFDFDSSDFadfga'   #  hasło

    # Budujemy URL do zapytania REST API
    url_data = (
        'https://' + user_name + ':' + password +
        '@opensky-network.org/api/states/all?' +
        'lamin=' + str(lat_min) + '&lomin=' + str(lon_min) +
        '&lamax=' + str(lat_max) + '&lomax=' + str(lon_max)
    )

    # Wysłanie zapytania do serwera
    response = requests.get(url_data).json()
    print(response)


    # Jeśli klucza 'states' nie ma lub jest pusty, to kończymy
    if 'states' not in response or response['states'] is None:
        print("No data received from the OpenSky API.")
        return

    # Kolumny zgodnie z dokumentacją
    col_name = [
        'icao24', 'callsign', 'origin_country', 'time_position', 'last_contact',
        'long', 'lat', 'baro_altitude', 'on_ground', 'velocity',
        'true_track', 'vertical_rate', 'sensors', 'geo_altitude',
        'squawk', 'spi', 'position_source'
    ]

    # Tworzymy DataFrame (często bywa mniej kolumn w odpowiedzi – trzeba się zabezpieczyć)
    flight_df = pd.DataFrame(response['states'], columns=col_name)

    # (Opcjonalnie) uzupełniamy brakujące wartości
    # flight_df = flight_df.fillna('No Data')

    # Zapisujemy do bazy danych
    save_to_db(flight_df, databasefile=databasefile)
    print("Data saved to database successfully!")


def plot_flight_data(databasefile="flights.db", show_plot=True):
    """
    Wczytuje dane z bazy, filtruje i rysuje wykres zależności wysokości geograficznej od prędkości.
    """
    # Wczytanie danych z bazy do obiektu DataFrame
    flight_df = load_flight_data(databasefile=databasefile)

    if flight_df.empty:
        print("Brak danych w bazie. Najpierw pobierz dane.")
        return

    # Usuwamy wiersze z brakami w kolumnach 'velocity' oraz 'geo_altitude'
    flight_df = flight_df.dropna(subset=['velocity', 'geo_altitude'])

    # Konwersja na typ liczbowy (jeśli z jakichś powodów są typu string)
    flight_df['velocity'] = pd.to_numeric(flight_df['velocity'], errors='coerce')
    flight_df['geo_altitude'] = pd.to_numeric(flight_df['geo_altitude'], errors='coerce')

    # Po powtórnym dropna, bo np. konwersja mogła wstawić NaN
    flight_df = flight_df.dropna(subset=['velocity', 'geo_altitude'])

    # Zamiana m/s -> km/h oraz metrów -> km
    flight_df['velocity_kmh'] = flight_df['velocity'] * 3.6
    flight_df['geo_altitude_km'] = flight_df['geo_altitude'] / 1000.0

    # Wybranie jednego rekordu na samolot:
    # np. tego, gdzie velocity_kmh jest największe (sortowanie malejące)
    flight_df = flight_df.sort_values(by='velocity_kmh', ascending=False)
    flight_df = flight_df.drop_duplicates(subset='icao24', keep='first')

    # Rysowanie wykresu prędkość (x) vs. wysokość (y)
    plt.figure(figsize=(8, 6))
    plt.scatter(flight_df['velocity_kmh'], flight_df['geo_altitude_km'],
                alpha=0.6, color='blue', marker='o')

    plt.xlabel('Velocity [km/h]')
    plt.ylabel('Geo altitude [km]')
    plt.title('ATL area flights – velocity vs. geo altitude')
    plt.xlim([0, 1200])
    plt.ylim([0, 14])
    plt.grid(True)
    plt.tight_layout()

    # Wyświetlenie wykresu tylko, jeśli show_plot=True
    if show_plot:
        plt.show()
