from evdev import InputDevice, categorize, ecodes
import requests
import time

# --- CONFIGURACIÓN ---
FLASK_APP_URL = "http://127.0.0.1:5000"  # URL de la aplicación Flask

# Identifica el dispositivo de tus botones USB.
DEVICE_PATH = "/dev/input/event0"  # Cambia esto a la ruta correcta de tu dispositivo USB

# Códigos de los botones que esperas recibir
BUTTON_CODE_EQUIPO1 = ecodes.KEY_A  # Cambia esto al código real de tu botón
BUTTON_CODE_EQUIPO2 = ecodes.KEY_B  # Cambia esto al código real de tu botón

# --- Lógica del Listener ---
def listen_for_buttons():
    print(f"Buscando dispositivo en {DEVICE_PATH}...")
    try:
        dev = InputDevice(DEVICE_PATH)
        print(f"Dispositivo encontrado: {dev.name} ({dev.path})")
    except FileNotFoundError:
        print(f"Error: Dispositivo {DEVICE_PATH} no encontrado.")
        print("Asegúrate de que los botones USB estén conectados y que la ruta sea correcta.")
        return

    print("Escuchando eventos de botones...")
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:  # Si es un evento de tecla
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:  # Solo cuando la tecla es presionada
                print(f"Botón presionado: {key_event.keycode} ({key_event.event.code})")

                if key_event.event.code == BUTTON_CODE_EQUIPO1:
                    print("Punto para Equipo 1!")
                    try:
                        response = requests.get(f"{FLASK_APP_URL}/agregar_punto/equipo1")
                        print(f"Respuesta de Flask: {response.json()}")
                    except requests.exceptions.ConnectionError as e:
                        print(f"Error de conexión a Flask: {e}")
                elif key_event.event.code == BUTTON_CODE_EQUIPO2:
                    print("Punto para Equipo 2!")
                    try:
                        response = requests.get(f"{FLASK_APP_URL}/agregar_punto/equipo2")
                        print(f"Respuesta de Flask: {response.json()}")
                    except requests.exceptions.ConnectionError as e:
                        print(f"Error de conexión a Flask: {e}")

if __name__ == '__main__':
    listen_for_buttons()