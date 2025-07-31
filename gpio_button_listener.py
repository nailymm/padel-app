# gpio_button_listener.py
# Listener para botones físicos conectados a GPIO en Raspberry Pi

import RPi.GPIO as GPIO
import time
import requests

# Configuración de pines GPIO
PIN_EQUIPO1 = 17  # Cambia según tu conexión
PIN_EQUIPO2 = 27  # Cambia según tu conexión

FLASK_URL = 'http://localhost:5000/agregar_punto/'

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_EQUIPO1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIN_EQUIPO2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Callback para sumar punto a cada equipo
def punto_equipo1(channel):
    print("Punto para equipo 1")
    try:
        requests.get(FLASK_URL + 'equipo1')
    except Exception as e:
        print(f"Error al enviar punto equipo 1: {e}")

def punto_equipo2(channel):
    print("Punto para equipo 2")
    try:
        requests.get(FLASK_URL + 'equipo2')
    except Exception as e:
        print(f"Error al enviar punto equipo 2: {e}")

# Configura la detección de eventos
GPIO.add_event_detect(PIN_EQUIPO1, GPIO.FALLING, callback=punto_equipo1, bouncetime=300)
GPIO.add_event_detect(PIN_EQUIPO2, GPIO.FALLING, callback=punto_equipo2, bouncetime=300)

try:
    print("Escuchando botones GPIO. Presiona Ctrl+C para salir.")
    while True:
        print(GPIO.input(PIN_EQUIPO1), GPIO.input(PIN_EQUIPO2))
        time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO limpio y programa terminado.")
