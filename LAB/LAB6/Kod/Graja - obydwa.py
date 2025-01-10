#!/usr/bin/python

import Adafruit_DHT
import sqlite3
import time
from statistics import mean

sensor = Adafruit_DHT.DHT11
pin = 'P8_12'
count = 18


def normalize_results(results):
    if len(results) > 2:
        results.remove(max(results))
        results.remove(min(results))
    return results


def measure():
    result_temperatures = []
    result_humidities = []

    while len(result_temperatures) < count:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is None or temperature is None:
            print('Nie udało się uzyskać odczytu. Spróbuj ponownie!')
            continue

        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

        result_temperatures.append(temperature)
        result_humidities.append(humidity)

    result_temperatures = normalize_results(result_temperatures)
    result_humidities = normalize_results(result_humidities)

    avg_temperature = mean(result_temperatures)
    avg_humidity = mean(result_humidities)

    print("Usredniony wynik Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(avg_temperature, avg_humidity))

    return avg_temperature, avg_humidity


def initialize_database(db_name="measurements.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements 
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL
        )""")
    return conn, cursor


def save(cursor, temperature: float, humidity: float):
    cursor.execute("INSERT INTO measurements (temperature, humidity) VALUES (?, ?)", (temperature, humidity))


def print_results(cursor):
    print("Wczytuje dotychczasowe wyniki...")

    cursor.execute("SELECT * from measurements")
    for (id, timestamp, temperature, humidity) in cursor.fetchall():
        print("{:>5} {:>5} {:>5} {:>20}".format(id, temperature, humidity, timestamp))


def main():
    conn, cursor = initialize_database()

    print_results(cursor)
    time.sleep(2)

    for i in range(5):
        print("Robię pomiar {}...".format(i + 1))
        temperature, humidity = measure()

        print("Zapisuje...")
        save(cursor, temperature, humidity)

        conn.commit()

    conn.close()


if __name__ == "__main__":
    main()