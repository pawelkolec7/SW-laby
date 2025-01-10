#include <OneWire.h>  
#include <DS18B20.h>  

#define ONEWIRE_PIN 19  // Pin do komunikacji 1-Wire

float mala[18] = {0.0};  // Tablica przechowująca ostatnie 18 odczytów temperatury
short int numer = 0;     // Indeks do zapisu kolejnych odczytów

// Adres czujnika 
byte address[8] = {0x28, 0x8, 0xC, 0x79, 0x97, 0x2, 0x3, 0x84};

OneWire onewire(ONEWIRE_PIN);  
DS18B20 sensors(&onewire);    

// Funkcja obliczająca najmniejszą wartość w tablicy
float mini(float mala[18]) {
    float a = 1000000.0; 
    for (int i = 0; i < 18; i++) {
        if (mala[i] < a) a = mala[i]; 
    }
    return a;
}

// Funkcja obliczająca największą wartość w tablicy
float maxi(float mala[18]) {
    float a = -273.15;  
    for (int i = 0; i < 18; i++) {
        if (mala[i] > a) a = mala[i];  
    }
    return a;
}

// Funkcja obliczająca średnią wartość bez minimum i maksimum
float srednia(float mala[18]) {
    float suma = 0;
    for (int i = 0; i < 18; i++) {
        suma += mala[i];  
    }
    suma = (suma - mini(mala) - maxi(mala)) / 16;  
    return suma;
}

void setup() {
    Serial.begin(9600);  
    sensors.begin();     
    sensors.request(address); 
}
void loop() {
    if (sensors.available()) {  
        float temperature = sensors.readTemperature(address);  // Odczyt temperatury
        mala[numer] = temperature;  // Zapis do tablicy

        numer++;  
        if (numer == 18) {  
            float avg_temperature = srednia(mala);  // Obliczenie średniej
            Serial.println(avg_temperature);  // Wyświetlenie wyniku
            numer = 0;  
        }
        sensors.request(address);  // Żądanie kolejnego pomiaru
        delay(1);  
    }
}
