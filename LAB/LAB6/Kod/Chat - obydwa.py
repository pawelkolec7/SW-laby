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
        sredni_pomiar_temperature REAL,
        sredni_pomiar_humidity REAL
    );
    ''')
    conn.commit()
    return conn, cursor


def read_sensor_data(sensor, pin, num_readings):
    """Odczytuje dane z czujnika."""
    temperature_readings = []
    humidity_readings = []
    for _ in range(num_readings):
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            humidity_readings.append(humidity)
            temperature_readings.append(temperature)
            print(f"Odczyt wilgotności: {humidity:.1f}%, Odczyt temperatury: {temperature:.1f}°C")
        else:
            print("Nie udało się pobrać danych z czujnika.")
        time.sleep(1)  # Krótka przerwa między odczytami
    return temperature_readings, humidity_readings


def calculate_average(readings):
    """Oblicza średnią z pomiarów po odrzuceniu wartości skrajnych."""
    if len(readings) < 3:
        print("Za mało odczytów do obliczenia średniej.")
        return None
    readings.remove(max(readings))
    readings.remove(min(readings))
    return sum(readings) / len(readings)


def store_to_database(cursor, timestamp, avg_temperature, avg_humidity):
    """Zapisuje pomiar do bazy danych."""
    cursor.execute(
        f"INSERT INTO {TABLE_NAME} (data_godzina, sredni_pomiar_temperature, sredni_pomiar_humidity) VALUES (?, ?, ?)",
        (timestamp, avg_temperature, avg_humidity))


def display_database_contents(cursor):
    """Wyświetla zawartość bazy danych."""
    cursor.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY id DESC LIMIT 5;")
    rows = cursor.fetchall()
    print("\nOstatnie 5 pomiarów:")
    for row in rows:
        print(
            f"Id: {row[0]}, Data i godzina: {row[1]}, Średnia temperatura: {row[2]:.2f}°C, Średnia wilgotność: {row[3]:.2f}%")


def main():
    conn, cursor = initialize_database()

    for _ in range(MEASUREMENTS_COUNT):
        print("\nRozpoczynam nowy cykl pomiarowy...")
        temperature_readings, humidity_readings = read_sensor_data(SENSOR, PIN, NUM_READINGS)

        average_temperature = calculate_average(temperature_readings)
        average_humidity = calculate_average(humidity_readings)

        if average_temperature is not None and average_humidity is not None:
            timestamp = datetime.now().isoformat()
            store_to_database(cursor, timestamp, average_temperature, average_humidity)
            conn.commit()
            print(
                f"Średnia temperatura: {average_temperature:.2f}°C, Średnia wilgotność: {average_humidity:.2f}% zapisana do bazy.")
        else:
            print("Pomiary nie zostały zapisane (błąd odczytu).")

    display_database_contents(cursor)
    conn.close()


if __name__ == "__main__":
    main()