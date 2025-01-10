#include <OneWire.h>
#include <DS18B20.h> 

// Numer pinu, do którego podłączyliśmy czujnik
#define ONEWIRE_PIN 7

// Funkcja wyciągająca wartość maksymalną z tablicy ostatnich pomiarów
float maxi(float mala[18]) {
    float a = -273.15;
    for (int i = 0; i < 18; i++) {
        if (mala[i] > a) a = mala[i];
    }
    return a;
}

// Funkcja wyciągająca wartość minimalną z tablicy ostatnich pomiarów
float mini(float mala[18]) {
    float a = 1000000.0;
    for (int i = 0; i < 18; i++) {
        if (mala[i] < a) a = mala[i];
    }
    return a;
}

// Funkcja wyliczająca średnią po odjęciu wartości maksymalnej i minimalnej
float srednia(float mala[18]) {
    float suma = 0; 
    for (int i = 0; i < 18; i++) {
        suma += mala[i]; 
    }
    suma = (suma - mini(mala) - maxi(mala)) / 16; 
    return suma; 
}

// Funkcja do obliczenia sumy wartości po usunięciu min i max
int suma_bitowa(float mala[18]) {
    float suma = 0;
    for (int i = 0; i < 18; i++) {
        suma += mala[i]; 
    }
    suma = (suma - mini(mala) - maxi(mala));
    return suma; 
}

// Adres czujnika
byte address[8] = {0x28, 0x8, 0xC, 0x79, 0x97, 0x2, 0x3, 0x84};

// Inicjalizacja obiektów do komunikacji z czujnikiem
OneWire onewire(ONEWIRE_PIN);
DS18B20 sensors(&onewire); 

float mala[18] = {0.0}; // Tablica do przechowywania 18 pomiarów temperatury
short int numer = 0; // Indeks dla tablicy pomiarów
int p1 = 0; // Pierwszy przycisk
int p2 = 0; // Drugi przycisk
int p3 = 0; // Trzeci przycisk

void setup() {
    pinMode(2, OUTPUT); 
    pinMode(4, INPUT_PULLUP); 
    pinMode(5, INPUT_PULLUP); 
    pinMode(6, INPUT_PULLUP); 
    digitalWrite(2, LOW); 

    while (!Serial);
    Serial.begin(9600); 
    sensors.begin(); 
    sensors.request(address); 
}

void loop() {
    // Sprawdzenie, czy przycisk podłączony do pinu 4 jest wciśnięty
    if (digitalRead(4) == 0 && p2 != 1 && p3 != 1) {
        p1 = 1; 
    }
    // Sprawdzenie, czy przycisk podłączony do pinu 5 jest wciśnięty
    if (digitalRead(5) == 0 && p2 != 1 && p3 != 1) {
        p2 = 1; 
    }
    // Sprawdzenie, czy przycisk podłączony do pinu 6 jest wciśnięty
    if (digitalRead(6) == 0 && p2 != 1 && p3 != 1) {
        p3 = 1; 
    }

    // Sprawdzenie, czy czujnik jest gotowy do odczytu
    if (sensors.available()) {
        // Jeśli przycisk 1 został wciśnięty
        if (p1 == 1) {
            float temperature = sensors.readTemperature(address); // Odczytanie temperatury
            Serial.println("Jeden pomiar:");
            Serial.print(temperature); 
            Serial.println(" 'C"); 
            sensors.request(address); // Wysłanie żądania do czujnika
            delay(20); 
            p1 = 0; 
        }

        // Jeśli przycisk 2 został wciśnięty
        else if (p2 == 1) {
            float temperature = sensors.readTemperature(address); // Odczytanie temperatury
            mala[numer] = temperature; // Zapisanie temperatury do tablicy
            //Miganie diody
            digitalWrite(2, HIGH); 
            delay(200); 
            digitalWrite(2, LOW); 
            if (numer == 17) {
                Serial.println("Srednia temperatura:"); 
                Serial.print(srednia(mala));
                Serial.println(F(" 'C"));
                numer = 0;
                p2 = 0;
            } else {
                numer++; 
            }
            sensors.request(address); // Wysłanie żądania do czujnika
            delay(20); 
        }
        // Jeśli przycisk 3 został wciśnięty
        else if (p3 == 1) {
            float temperature = sensors.readTemperature(address); // Odczytanie temperatury
            mala[numer] = temperature; // Zapisanie temperatury do tablicy
            digitalWrite(2, HIGH); 
            delay(200); 
            digitalWrite(2, LOW); 
            if (numer == 17) {
                int bitowe = suma_bitowa(mala) >> 4; // Obliczenie średniej za pomocą przesunięcia bitowego
                Serial.println("Srednia temperatura - bitowo:"); 
                Serial.print(bitowe);
                Serial.println(F(" 'C")); 
                numer = 0; 
                p3 = 0; 
            } else {
                numer++; 
            }
            sensors.request(address); // Wysłanie żądania do czujnika
            delay(20); 
        }
    }
}


