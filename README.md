
# Marcador de Pádel - Raspberry Pi

Este proyecto es una aplicación web para llevar el marcador de partidos de pádel, diseñada para ejecutarse en una Raspberry Pi. Utiliza Python, Flask y SQLite.

## Requisitos
- Raspberry Pi con Raspbian (o cualquier Linux)
- Python 3.8+
- pip

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/nailymm/padel-app.git
   cd padel-app
   ```

2. **(Opcional) Crea un entorno virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install Flask RPi.GPIO
   ```

4. **Inicializa la base de datos:**
   Esto se hace automáticamente al ejecutar la app por primera vez.

## Ejecución de la app principal

1. Inicia la aplicación Flask:
   ```bash
   python3 app.py
   ```
2. Abre tu navegador en la Raspberry Pi o desde otra máquina en la red:
   - [http://localhost:5000](http://localhost:5000)
   - O usa la IP de tu Raspberry Pi: [http://IP_RASPBERRY:5000](http://IP_RASPBERRY:5000)

## Uso del listener GPIO

1. Conecta los botones físicos a los pines GPIO indicados en `gpio_button_listener.py` (por defecto 17 y 27).
2. Ejecuta el listener en la Raspberry Pi:
   ```bash
   python3 gpio_button_listener.py
   ```
3. Los callbacks ya están integrados para enviar puntos a la app Flask mediante peticiones HTTP.

**Nota:** Si usas otro modelo de Raspberry Pi o pines diferentes, ajusta los valores de `PIN_EQUIPO1` y `PIN_EQUIPO2` en el script.

## Archivos principales
- `app.py`: Servidor Flask principal
- `padel_logic.py`: Lógica del partido
- `database_manager.py`: Gestión de la base de datos
- `gpio_button_listener.py`: Listener para botones físicos GPIO
- `templates/`: HTMLs de la app
- `static/`: Archivos estáticos (CSS, imágenes)

## Autor
- Naily Melendez

---
¡Disfruta tu marcador de pádel digital!
