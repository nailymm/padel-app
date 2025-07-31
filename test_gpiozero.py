from gpiozero import Button
from signal import pause

# Reemplaza 17 con el número BCM de tu pin GPIO
button = Button(17, pull_up=True) 

print("Esperando presiones de botón en GPIO 17...")

button.when_pressed = lambda: print("¡Botón presionado!")
button.when_released = lambda: print("¡Botón liberado!")

pause() # Mantiene el script en ejecución hasta que se detenga manualmente