# database_manager.py

import sqlite3

DATABASE_NAME = 'padel_app.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            equipo1_jugador1_id INTEGER,
            equipo1_jugador2_id INTEGER,
            equipo2_jugador1_id INTEGER,
            equipo2_jugador2_id INTEGER,
            sets_equipo1 INTEGER,
            sets_equipo2 INTEGER,
            historial_juegos_json TEXT,
            ganador_equipo TEXT,
            FOREIGN KEY (equipo1_jugador1_id) REFERENCES jugadores(id),
            FOREIGN KEY (equipo1_jugador2_id) REFERENCES jugadores(id),
            FOREIGN KEY (equipo2_jugador1_id) REFERENCES jugadores(id),
            FOREIGN KEY (equipo2_jugador2_id) REFERENCES jugadores(id)
        )
    """)
    conn.commit()
    conn.close()

def get_or_create_player(player_name):
    """
    Obtiene el ID de un jugador por su nombre. Si no existe, lo crea.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    player_id = None # Inicializa player_id a None

    # Usa un bloque try-finally para asegurar que la conexión se cierra
    try:
        cursor.execute("SELECT id FROM jugadores WHERE nombre = ?", (player_name,))
        result = cursor.fetchone()

        if result:
            player_id = result['id'] # Si el jugador existe, devuelve su ID
        else:
            cursor.execute("INSERT INTO jugadores (nombre) VALUES (?)", (player_name,))
            conn.commit()
            player_id = cursor.lastrowid # Devuelve el ID del jugador recién creado
    finally: # Este finally cierra la conexión independientemente de si hubo un error o no
        conn.close()
    
    return player_id


def save_match(match_data):
    """
    Guarda los datos de un partido finalizado en la base de datos.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try: # Agregamos un try-finally aquí también para asegurar el cierre
        cursor.execute("""
            INSERT INTO partidos (
                fecha, hora, equipo1_jugador1_id, equipo1_jugador2_id,
                equipo2_jugador1_id, equipo2_jugador2_id, sets_equipo1,
                sets_equipo2, historial_juegos_json, ganador_equipo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            match_data['fecha'],
            match_data['hora'],
            match_data['equipo1_jugador1_id'],
            match_data['equipo1_jugador2_id'],
            match_data['equipo2_jugador1_id'],
            match_data['equipo2_jugador2_id'],
            match_data['sets_equipo1'],
            match_data['sets_equipo2'],
            match_data['historial_juegos_json'],
            match_data['ganador_equipo']
        ))
        conn.commit()
    finally:
        conn.close()

def get_matches_by_date(date):
    """
    Obtiene todos los partidos jugados en una fecha específica,
    incluyendo los nombres de los jugadores.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    matches = [] # Inicializa matches como una lista vacía
    try: # Agregamos un try-finally aquí también
        cursor.execute("""
            SELECT
                p.fecha, p.hora,
                j1.nombre AS equipo1_jugador1, j2.nombre AS equipo1_jugador2,
                j3.nombre AS equipo2_jugador1, j4.nombre AS equipo2_jugador2,
                p.sets_equipo1, p.sets_equipo2, p.ganador_equipo
            FROM partidos p
            JOIN jugadores j1 ON p.equipo1_jugador1_id = j1.id
            JOIN jugadores j2 ON p.equipo1_jugador2_id = j2.id
            JOIN jugadores j3 ON p.equipo2_jugador1_id = j3.id
            JOIN jugadores j4 ON p.equipo2_jugador2_id = j4.id
            WHERE p.fecha = ?
            ORDER BY p.hora DESC
        """, (date,))
        
        matches = cursor.fetchall()
    finally:
        conn.close()
    return matches

# Inicializa la base de datos cuando este módulo es importado o ejecutado
init_db()