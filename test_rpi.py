import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # Usar numeración BCM
GPIO.setwarnings(False) # Desactivar advertencias sobre canales en uso

INPUT_PIN = 17 # Reemplaza con el número BCM de tu pin GPIO

# Configurar el pin como entrada con resistencia pull-up
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print(f"Probando lectura del GPIO {INPUT_PIN}. Presiona Ctrl+C para salir.")

try:
    while True:
        # GPIO.LOW indica que el botón fue presionado (porque está conectado a GND)
        if GPIO.input(INPUT_PIN) == GPIO.LOW:
            print("¡Botón presionado!")
        else:
            print("Botón no presionado.")
        time.sleep(0.1) # Pequeña pausa para evitar lecturas inestables
except KeyboardInterrupt:
    print("\nSaliendo del programa.")
finally:
    GPIO.cleanup() # Limpiar los GPIOs