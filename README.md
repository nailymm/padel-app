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
   cd REPO
   ```

2. **(Opcional) Crea un entorno virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install Flask
   ```

4. **Inicializa la base de datos:**
   Esto se hace automáticamente al ejecutar la app por primera vez.

## Ejecución

1. **Inicia la aplicación:**
   ```bash
   python3 app.py
   ```

2. **Abre tu navegador en la Raspberry Pi o desde otra máquina en la red:**
   - [http://localhost:5000](http://localhost:5000)
   - O usa la IP de tu Raspberry Pi: [http://IP_RASPBERRY:5000](http://IP_RASPBERRY:5000)

## Archivos principales
- `app.py`: Servidor Flask principal
- `padel_logic.py`: Lógica del partido
- `database_manager.py`: Gestión de la base de datos
- `templates/`: HTMLs de la app
- `static/`: Archivos estáticos (CSS, imágenes)

## Notas
- Puedes conectar botones físicos a la Raspberry Pi y adaptar la lógica en `usb_button_listener.py`.
- El marcador es responsivo y puede verse en tablets o pantallas grandes.

## Autor
- Naily Melendez

---
¡Disfruta tu marcador de pádel digital!
