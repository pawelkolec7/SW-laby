#!/usr/bin/python

import Adafruit_DHT
import sqlite3
from datetime import datetime
import time

# Ustawienia
SENSOR = Adafruit_DHT.DHT11
PIN = 'P8_12'  # Pin dla BeagleBone Black (zmień na GPIO23 dla Raspberry Pi)
NUM_READINGS = 18
MEASUREMENTS_COUNT = 5  # Liczba cykli pomiarowych

DB_NAME = "pomiary.db"
TABLE_NAME = "pomiary"


def initialize_database():
    """Inicjalizuje bazę danych."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_godzina TEXT,
        sredni_pomiar REAL
    );
    ''')
    conn.commit()
    return conn, cursor


def read_sensor_data(sensor, pin, num_readings):
    """Odczytuje dane z czujnika."""
    readings = []
    for _ in range(num_readings):
        humidity, _ = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None:
            readings.append(humidity)
            print(f"Odczyt wilgotności: {humidity:.1f}%")
        else:
            print("Nie udało się pobrać danych z czujnika.")
        time.sleep(1)  # Krótka przerwa między odczytami
    return readings


def calculate_average(readings):
    """Oblicza średnią z pomiarów po odrzuceniu wartości skrajnych."""
    if len(readings) < 3:
        print("Za mało odczytów do obliczenia średniej.")
        return None
    readings.remove(max(readings))
    readings.remove(min(readings))
    return sum(readings) / len(readings)


def store_to_database(cursor, timestamp, average):
    """Zapisuje pomiar do bazy danych."""
    cursor.execute(f"INSERT INTO {TABLE_NAME} (data_godzina, sredni_pomiar) VALUES (?, ?)",
                   (timestamp, average))


def display_database_contents(cursor):
    """Wyświetla zawartość bazy danych."""
    cursor.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY id DESC LIMIT 5;")
    rows = cursor.fetchall()
    print("\nOstatnie 5 pomiarów:")
    for row in rows:
        print(f"Id: {row[0]}, Data i godzina: {row[1]}, Średni pomiar: {row[2]:.2f}%")


def main():
    conn, cursor = initialize_database()

    for _ in range(MEASUREMENTS_COUNT):
        print("\nRozpoczynam nowy cykl pomiarowy...")
        readings = read_sensor_data(SENSOR, PIN, NUM_READINGS)
        average = calculate_average(readings)
        if average is not None:
            timestamp = datetime.now().isoformat()
            store_to_database(cursor, timestamp, average)
            conn.commit()
            print(f"Średnia wilgotność: {average:.2f}% zapisana do bazy.")
        else:
            print("Pomiary nie zostały zapisane (błąd odczytu).")

    display_database_contents(cursor)
    conn.close()


if __name__ == "__main__":
    main()
