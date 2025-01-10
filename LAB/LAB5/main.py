import Adafruit_BBIO.GPIO as GPIO
import time

LED_PIN = "P8_10"
GPIO.setup(LED_PIN, GPIO.OUT)

def short_blink():
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.25)

def long_blink():
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.75)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.25)

try:
    while True:
        # Trzy krótkie mignięcia
        for _ in range(3):
            short_blink()
        
        # Przerwa
        time.sleep(0.5)
        
        # Trzy długie mignięcia
        for _ in range(3):
            long_blink()
        
        # Przerwa
        time.sleep(0.5)
        
        # Trzy krótkie mignięcia
        for _ in range(3):
            short_blink()
        
        # Dłuższa przerwa po zakończeniu sygnału SOS 
        time.sleep(3)

except KeyboardInterrupt:
    # Czyszczenie ustawień GPIO po zakończeniu programu
    GPIO.cleanup()
