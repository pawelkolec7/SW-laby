int value = 0;           // zmienna przechowująca wartość odczytaną z potencjometru
String buttonState = "off"; // zmienna przechowująca stan przycisku (on/off)

void setup() {
  pinMode(2, INPUT_PULLUP); // ustawienie pinu 2 z wbudowanym rezystorem (przycisk)
  pinMode(3, OUTPUT);    // ustawienie pinu 3 (dioda)
  pinMode(4, OUTPUT);    // ustawienie pinu 4 (dioda)
  pinMode(5, OUTPUT);    // ustawienie pinu 5 (dioda)
  pinMode(6, OUTPUT);    // ustawienie pinu 6 (dioda)
  attachInterrupt(digitalPinToInterrupt(2), toggleState, FALLING); // przerwanie na pinie 2
  Serial.begin(9600); }

// obsługa przycisku i odpowiadającej mu diody
void toggleState() {
  if (buttonState == "off") {
    digitalWrite(3, LOW);  
    buttonState = "on";    
  } else {
    digitalWrite(3, HIGH); 
    buttonState = "off";   
  }
  delay(500);             // delay 500 ms 
}
void loop() {
  value = analogRead(A5);  // odczytanie wartości z potencjometru
  if (value < 300) {       // jeśli wartość jest poniżej 300, wyłącz wszystkie diody
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
    digitalWrite(6, LOW);
  } else if (value >= 300 && value < 600) {  // jeśli wartość jest między 300 a 600, włącz zieloną diodę
    digitalWrite(4, HIGH);
    digitalWrite(5, LOW);
    digitalWrite(6, LOW);
  } else if (value >= 600 && value < 900) {  // jeśli wartość jest między 600 a 900, włącz zieloną i żółtą diodę
    digitalWrite(4, HIGH);
    digitalWrite(5, HIGH);
    digitalWrite(6, LOW);
  } else {                // jeśli wartość jest równa lub wyższa od 900, włącz wszystkie diody
    digitalWrite(4, HIGH);
    digitalWrite(5, HIGH);
    digitalWrite(6, HIGH);
  }
}
