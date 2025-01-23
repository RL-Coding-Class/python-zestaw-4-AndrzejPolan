import sqlite3
import pandas as pd

def create_table(max_repeats, databasefile="flights.db"):
    """
    Tworzy (lub odtwarza) w bazie danych tabelę airport_atl.
    Jeśli max_repeats == 0, to nie robi nic.
    Jeśli max_repeats > 0, to usuwa tabelę (jeśli istnieje) i tworzy nową.
    """
    if max_repeats > 0:
        # Połącz z bazą danych (lub utwórz ją, jeśli nie istnieje).
        connection = sqlite3.connect(databasefile)
        cursor = connection.cursor()

        # Usuń tabelę, jeśli istnieje
        cursor.execute("DROP TABLE IF EXISTS airport_atl")

        # Utwórz tabelę
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS airport_atl (
                icao24 TEXT,
                callsign TEXT,
                origin_country TEXT,
                time_position TEXT,
                last_contact TEXT,
                long REAL,
                lat REAL,
                baro_altitude REAL,
                on_ground TEXT,
                velocity REAL,
                true_track REAL,
                vertical_rate REAL,
                sensors TEXT,
                geo_altitude REAL,
                squawk TEXT,
                spi TEXT,
                position_source INTEGER
            )
        ''')
        connection.commit()
        connection.close()


def save_to_db(flight_df, databasefile="flights.db"):
    """
    Zapisuje zawartość DataFrame flight_df do tabeli airport_atl w bazie danych.
    Jeśli tabela nie istnieje, tworzy ją – ale zakładamy, że jest już utworzona w create_table.
    """
    connection = sqlite3.connect(databasefile)
    # Dopisujemy rekordy do istniejącej tabeli (if_exists="append").
    flight_df.to_sql("airport_atl", connection, if_exists="append", index=False)
    connection.close()


def load_flight_data(databasefile="flights.db"):
    """
    Odczytuje wszystkie dane z tabeli airport_atl w bazie danych i zwraca je jako obiekt DataFrame.
    """
    connection = sqlite3.connect(databasefile)
    flight_df = pd.read_sql_query("SELECT * FROM airport_atl", connection)
    connection.close()
    return flight_df
