import Adafruit_DHT
import sqlite3
import time
from statistics import mean

CZUJNIK = Adafruit_DHT.DHT11  # Typ czujnika DHT
PIN = 'P8_11'  # Pin GPIO, do którego podłączony jest czujnik
LICZBA_POMIAROW = 18  # Liczba pomiarów do wykonania

# Normalizuje listę przez usunięcie wartości maksymalnej i minimalnej.
def normalizuj_wyniki(wyniki):
    if len(wyniki) > 2:
        wyniki.remove(max(wyniki))
        wyniki.remove(min(wyniki))
    return wyniki

# Wykonuje pomiar wilgotności i oblicza średnią z kilku odczytów.
def wykonaj_pomiar_wilgotnosci():
    wilgotnosci = []
    while len(wilgotnosci) < LICZBA_POMIAROW:
        wilgotnosc, _ = Adafruit_DHT.read_retry(CZUJNIK, PIN)
        if wilgotnosc is not None:
            print(f"Wilgotnosc={wilgotnosc:.1f}%")
            wilgotnosci.append(wilgotnosc)
        else:
            print("Blad odczytu z czujnika.")
    wilgotnosci = normalizuj_wyniki(wilgotnosci)

    srednia_wilgotnosc = mean(wilgotnosci)
    print(f"Usredniony wynik: {srednia_wilgotnosc:.1f}%")

    return srednia_wilgotnosc

# Inicjalizuje bazę danych SQLite do zapisu wyników pomiarów wilgotności.
def inicjalizuj_baze_danych(nazwa_bazy="pomiary_wilgotnosci.db"):
    polaczenie = sqlite3.connect(nazwa_bazy)
    kursor = polaczenie.cursor()
    kursor.execute(""" 
        CREATE TABLE IF NOT EXISTS pomiary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            znacznik_czasu DATETIME DEFAULT CURRENT_TIMESTAMP,
            wilgotnosc REAL NOT NULL
        )
    """)
    return polaczenie, kursor
# Zapisuje wynik pomiaru wilgotności do bazy danych.
def zapisz_do_bazy(kursor, wilgotnosc):
    kursor.execute("INSERT INTO pomiary (wilgotnosc) VALUES (?)", (wilgotnosc,))

# Wyświetla zapisane wyniki pomiarów z bazy danych.
def wyswietl_wyniki(kursor):
    kursor.execute("SELECT * FROM pomiary")
    wyniki = kursor.fetchall()
    print("\nWyniki pomiarow:")
    print(f"{'ID':>5} {'Wilgotnosc':>12} {'Znacznik czasu':>25}")
    print("-" * 50)
    for rekord in wyniki:
        print(f"{rekord[0]:>5} {rekord[2]:>12.1f} {rekord[1]:>25}")

# Główna funkcja programu - wykonuje pomiary wilgotności i zapisuje je do bazy danych.
def main():
    polaczenie, kursor = inicjalizuj_baze_danych()

    for i in range(5):
        print(f"\nPomiar {i + 1}:")
        srednia_wilgotnosc = wykonaj_pomiar_wilgotnosci()
        zapisz_do_bazy(kursor, srednia_wilgotnosc)
        polaczenie.commit()
        time.sleep(1)

    wyswietl_wyniki(kursor)

    polaczenie.close()

if __name__ == "__main__":
    main()

