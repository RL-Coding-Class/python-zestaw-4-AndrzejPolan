import schedule
import time
from zadanie_1.database import create_table
from zadanie_1.flight_data import fetch_flight_data, plot_flight_data

def main(interval, max_repeats):
    """
    Uruchamia harmonogram: fetch_flight_data() co 'interval' sekund,
    łącznie 'max_repeats' razy. Jeśli max_repeats == 0, to nie pobiera
    nowych danych, tylko odczytuje istniejącą bazę.
    """
    # Jeśli max_repeats == 0, tworzenie nowej tabeli jest zbędne
    create_table(max_repeats)

    # Licznik iteracji
    counter = 0

    # Funkcja 'opakowująca' wywołanie fetch_flight_data
    def job_wrapper():
        nonlocal counter
        if counter < max_repeats:
            fetch_flight_data()
            counter += 1
        else:
            print("All tasks completed. Stopping scheduler...")
            return schedule.CancelJob

    # Jeśli jednak chcemy ściągnąć dane:
    if max_repeats > 0:
        schedule.every(interval).seconds.do(job_wrapper)

        # Pętla główna scheduler-a
        while counter < max_repeats:
            schedule.run_pending()
            time.sleep(1)  # Krótkie opóźnienie

    # Po zakończeniu (lub gdy max_repeats=0) generuj wykres
    plot_flight_data()

if __name__ == '__main__':
    FETCH_INTERVAL = 60  # liczba sekund między kolejnymi odczytami
    MAX_REPEATS = 10     # ile razy pobrać dane (10 razy co 60 s)
    # jeśli MAX_REPEATS = 0 -> nie pobieramy nowych danych, tylko generujemy wykres z poprzednich
    main(FETCH_INTERVAL, MAX_REPEATS)
