#!/usr/bin/python
import Adafruit_DHT
import sqlite3
from datetime import datetime

sensor = Adafruit_DHT.DHT11

conn = sqlite3.connect("pomiary.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS pomiary
    (id INTEGER PRIMARY KEY,
    data_godzina TEXT,
    sredni_pomiar NUMBER(7,2));''')

pin = 'P8_12'


pomiary = list()
for i in range(18):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        pomiary.append(humidity)
        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')

pomiary.remove(max(pomiary))
pomiary.remove(min(pomiary))
suma = sum(pomiary)
srednia = suma / len(pomiary)

print(*pomiary)
print(srednia)

data_godzina = datetime.now()
cursor.execute("INSERT INTO pomiary (data_godzina, sredni_pomiar) VALUES (?,?)",
               (data_godzina, srednia))

cursor.execute("SELECT * FROM pomiary;")
records = cursor.fetchall()
for row in records:
    print("Id: ", row[0])
    print("Data i godzina: ", row[1])
    print("Średni pomiar: ", row[2])
    print("\n")

conn.commit()
conn.close()