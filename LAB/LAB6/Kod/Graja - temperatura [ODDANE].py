import Adafruit_DHT
import sqlite3
import time
from statistics import mean

# Konfiguracja czujnika
SENSOR = Adafruit_DHT.DHT11
PIN = 'P8_12'
MEASUREMENT_COUNT = 18  # Liczba pomiarów do zebrania

# Funkcja do normalizacji wyników
def normalize_results(results):
    if len(results) > 2:
        results.remove(max(results))
        results.remove(min(results))
    return results

# Funkcja do wykonania pomiarów temperatury
def perform_temperature_measurement():
    temperatures = []

    while len(temperatures) < MEASUREMENT_COUNT:
        _, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
        if temperature is not None:
            print(f"Temp={temperature:.1f}°C")
            temperatures.append(temperature)
        else:
            print("Błąd odczytu z czujnika. Próba ponowna...")

    # Normalizacja wyników
    temperatures = normalize_results(temperatures)

    # Wyliczanie średniej
    avg_temperature = mean(temperatures)
    print(f"Uśredniony wynik: Temp={avg_temperature:.1f}°C")

    return avg_temperature

# Funkcja inicjalizacji bazy danych
def initialize_database(db_name="temperature_measurements.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL NOT NULL
        )
    """)
    return conn, cursor

# Funkcja do zapisu wyników do bazy
def save_to_database(cursor, temperature):
    cursor.execute("INSERT INTO measurements (temperature) VALUES (?)", (temperature,))

# Funkcja do wyświetlania wyników z bazy
def display_results(cursor):
    cursor.execute("SELECT * FROM measurements")
    results = cursor.fetchall()
    print("\nWyniki pomiarów:")
    print(f"{'ID':>5} {'Temperatura':>12} {'Znacznik czasowy':>25}")
    print("=" * 50)
    for record in results:
        print(f"{record[0]:>5} {record[2]:>12.1f} {record[1]:>25}")

# Główna funkcja programu
def main():
    conn, cursor = initialize_database()

    # Wykonanie 5 pomiarów temperatury
    for i in range(5):
        print(f"\nPomiar {i + 1}:")
        avg_temperature = perform_temperature_measurement()
        save_to_database(cursor, avg_temperature)
        conn.commit()
        time.sleep(2)  # Odstęp między pomiarami

    # Wyświetlenie wyników z bazy danych
    display_results(cursor)

    # Zamknięcie połączenia z bazą
    conn.close()

if __name__ == "__main__":
    main()
