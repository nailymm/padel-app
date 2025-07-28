from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from padel_logic import PartidoPadel
from database_manager import get_matches_by_date, init_db
import datetime
import pickle
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
    if current_match and current_match.estado_partido == "En Curso":
        return redirect(url_for('score_board'))
    return render_template('index.html')

@app.route('/iniciar_partido', methods=['POST'])
def iniciar_partido():
    global current_match
    p1_eq1 = request.form['p1_eq1']
    p2_eq1 = request.form['p2_eq1']
    p1_eq2 = request.form['p1_eq2']
    p2_eq2 = request.form['p2_eq2']

    if not all([p1_eq1, p2_eq1, p1_eq2, p2_eq2]):
        return "Todos los nombres de jugadores son obligatorios", 400

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

@app.route('/reiniciar_partido')
def reiniciar_partido():
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)