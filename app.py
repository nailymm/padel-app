from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from padel_logic import PartidoPadel
from database_manager import get_matches_by_date, init_db
import datetime
import pickle
import os
import json
import time 
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_AQUI_MUY_LARGA_Y_COMPLICADA_Y_DIFICIL'

MATCH_STATE_FILE = 'current_match_state.pkl'

def load_match_state():
    if os.path.exists(MATCH_STATE_FILE):
        with open(MATCH_STATE_FILE, 'rb') as f:
            try:
                return pickle.load(f)
            except Exception as e:
                print(f"Error cargando estado del partido: {e}")
                return None
    return None

def save_match_state(match_obj):
    with open(MATCH_STATE_FILE, 'wb') as f:
        pickle.dump(match_obj, f)

def clear_match_state():
    if os.path.exists(MATCH_STATE_FILE):
        os.remove(MATCH_STATE_FILE)

init_db()
current_match = load_match_state()

@app.route('/')
def index():
    # Se pasa la información de la sesión a la plantilla
    reserva_activa = 'reserva_activa' in session and session['reserva_activa']
    tiempo_reserva = session.get('tiempo_reserva_minutos', 90)  # Valor por defecto
    return render_template('index.html', reserva_activa=reserva_activa, tiempo_reserva=tiempo_reserva)

@app.route('/iniciar_partido', methods=['POST'])
def iniciar_partido():
    """
    Inicia una nueva reserva (si no existe) y un nuevo partido.
    """
    global current_match

    # Lógica del cronómetro: Si no hay reserva activa, la iniciamos
    if 'reserva_activa' not in session or not session['reserva_activa']:
        try:
            tiempo_total_min = int(request.form.get('tiempo_reserva', 90)) # Se obtiene del formulario
        except (ValueError, TypeError):
            tiempo_total_min = 90 # Fallback por si hay un error en el valor
        
        session['tiempo_reserva_minutos'] = tiempo_total_min
        session['tiempo_reserva_segundos'] = tiempo_total_min * 60
        session['tiempo_inicio'] = time.time()
        session['reserva_activa'] = True

    # Lógica de los jugadores y el partido
    p1_eq1 = request.form['p1_eq1']
    p2_eq1 = request.form['p2_eq1']
    p1_eq2 = request.form['p1_eq2']
    p2_eq2 = request.form['p2_eq2']

    if not all([p1_eq1, p2_eq1, p1_eq2, p2_eq2]):
        return "Todos los nombres de jugadores son obligatorios", 400

    # Limpiar el estado del partido anterior antes de iniciar uno nuevo
    current_match = PartidoPadel(p1_eq1, p2_eq1, p1_eq2, p2_eq2)
    save_match_state(current_match)
    
    return redirect(url_for('score_board'))

@app.route('/marcador')
def score_board():
    global current_match

    if not current_match:
        return redirect(url_for('index'))

    return render_template('score_board.html', match=current_match.obtener_puntaje_display())

@app.route('/agregar_punto/<equipo>')
def agregar_punto(equipo):
    global current_match

    if not current_match:
        return jsonify({'error': 'No hay partido en curso'}), 400

    if current_match.estado_partido == "En Curso":
        updated_state = current_match.agregar_punto(equipo)
        save_match_state(current_match)
        return jsonify(updated_state)
    else:
        return jsonify(current_match.obtener_puntaje_display())

@app.route('/estado_partido')
def estado_partido():
    global current_match
    if not current_match:
        return jsonify({'error': 'No hay partido en curso'}), 400
    return jsonify(current_match.obtener_puntaje_display())

@app.route('/reiniciar_partido')
def reiniciar_partido():
    global current_match
    current_match = None
    clear_match_state()
    return redirect(url_for('index'))

@app.route('/tiempo_restante')
def tiempo_restante():
    """
    Devuelve el tiempo restante del cronómetro.
    """
    if 'reserva_activa' in session and session['reserva_activa']:
        tiempo_transcurrido = time.time() - session['tiempo_inicio']
        tiempo_restante_seg = session['tiempo_reserva_segundos'] - tiempo_transcurrido
        
        if tiempo_restante_seg <= 0:
            session['reserva_activa'] = False
            tiempo_restante_seg = 0

        minutos = int(tiempo_restante_seg // 60)
        segundos = int(tiempo_restante_seg % 60)
        
        return jsonify({'minutos': minutos, 'segundos': segundos, 'activo': session['reserva_activa']})
    else:
        return jsonify({'minutos': 0, 'segundos': 0, 'activo': False})

@app.route('/terminar_reserva')
def terminar_reserva():
    """
    Finaliza la reserva de la cancha manualmente y el partido actual.
    """
    session.pop('tiempo_reserva_minutos', None)
    session.pop('tiempo_reserva_segundos', None)
    session.pop('tiempo_inicio', None)
    session.pop('reserva_activa', None)
    global current_match
    current_match = None
    clear_match_state()
    return redirect(url_for('index'))

@app.route('/historial')
def historial():
    today = datetime.date.today().strftime('%Y-%m-%d')
    matches = get_matches_by_date(today)
    return render_template('historial.html', matches=matches, selected_date=today)

@app.route('/buscar_historial', methods=['POST'])
def buscar_historial():
    date = request.form['search_date']
    matches = get_matches_by_date(date)
    return render_template('historial.html', matches=matches, selected_date=date)

@app.route('/fin_partido')
def fin_partido():
    session['reserva_activa'] = False
    return render_template('end_game.html')

@app.route('/finalizar_partido')
def finalizar_partido():
    global current_match
    # Aquí puedes asegurarte de guardar el partido si no se ha guardado
    clear_match_state()
    current_match = None
    os.system("nohup /home/nezz/padel-app/cerrar_navegador.sh &")
    return "Navegador cerrando y partido finalizado."
    # return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)