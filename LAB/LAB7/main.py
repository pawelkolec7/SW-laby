import Adafruit_BBIO.UART as UART
import serial
import sqlite3
import time

# Inicjalizacja UART
def setup_uart():
    UART.setup("UART1")  # Ustawienie portu UART1
    ser = serial.Serial(port="/dev/ttyS1", baudrate=9600, timeout=1)  # Konfiguracja połączenia UART
    return ser  # Zwraca obiekt serial do dalszego użytku

# Tworzenie bazy danych (jeśli nie istnieje)
def create_db():
    conn = sqlite3.connect('temperatura.db')  # Połączenie z bazą SQLite
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS temperatura
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  MEASURED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                  temperatura REAL)''')  # Tworzenie tabeli do przechowywania temperatur
    conn.commit()
    conn.close()

# Wstawianie średniej temperatury do bazy danych
def insert_db(avg_temp):
    conn = sqlite3.connect('temperatura.db')  # Połączenie z bazą
    c = conn.cursor()
    c.execute("INSERT INTO temperatura (temperatura) VALUES (?)", (avg_temp,))  # Wstawienie wartości
    conn.commit()
    conn.close()

# Wyświetlanie danych z bazy
def show_db():
    conn = sqlite3.connect('temperatura.db')  # Połączenie z bazą
    c = conn.cursor()
    c.execute("SELECT * FROM temperatura")  # Pobranie wszystkich rekordów
    measurements = c.fetchall()
    for measurement in measurements:
        print(f"ID: {measurement[0]} Znacznik czasowy: {measurement[1]} Temperatura: {measurement[2]} C")  # Wyświetlenie rekordów
    conn.close()

# Funkcja do odczytu danych z UART i przetwarzania
def read_uart_data(ser):
    if ser.isOpen():  # Sprawdzenie, czy port UART jest otwarty
        message = ser.readline().decode("utf-8").strip()  # Odczyt i oczyszczenie danych
        return message
    return None  # Zwraca None, jeśli port nie jest otwarty

# Główna funkcja programu
def main():
    ser = setup_uart()  # Inicjalizacja UART
    create_db()  # Tworzenie bazy danych
    while True:
        message = read_uart_data(ser)  # Odczyt danych z UART
        if message:
            try:
                avg_temp = float(message)  
                print(f"Odczytana temperatura: {avg_temp} C")

                insert_db(avg_temp)  # Zapis temperatury do bazy danych
                show_db()  # Wyświetlenie zawartości bazy
            except ValueError:
                print("Nieprawidłowy format danych temperatury")  
        time.sleep(1)  # Przerwa między odczytami
if __name__ == "__main__":
    main()    
