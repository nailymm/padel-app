import json
from datetime import datetime

# Importamos las funciones de nuestro manejador de base de datos
from database_manager import get_or_create_player, save_match

class PartidoPadel:
    def __init__(self, equipo1_jugador1_nombre, equipo1_jugador2_nombre,
                 equipo2_jugador1_nombre, equipo2_jugador2_nombre):
        self.puntuacion_display = {0: '0', 1: '15', 2: '30', 3: '40', 4: 'ADV'}

        self.jugadores_nombres = {
            'equipo1': [equipo1_jugador1_nombre, equipo1_jugador2_nombre],
            'equipo2': [equipo2_jugador1_nombre, equipo2_jugador2_nombre]
        }
        self.jugadores_ids = {
            'equipo1': [get_or_create_player(equipo1_jugador1_nombre), get_or_create_player(equipo1_jugador2_nombre)],
            'equipo2': [get_or_create_player(equipo2_jugador1_nombre), get_or_create_player(equipo2_jugador2_nombre)]
        }

        self.puntuacion_juego = {'equipo1': 0, 'equipo2': 0}
        # Cambiamos a listas para sets
        self.sets_equipo1 = [0, 0, 0]
        self.sets_equipo2 = [0, 0, 0]
        self.set_actual = 0  # 0: primer set, 1: segundo, 2: tercero

        self.puntuacion_partido = {'equipo1': 0, 'equipo2': 0}
        self.juego_en_tiebreak = False
        self.historial_juegos = []
        self.estado_partido = "En Curso"

        from datetime import datetime
        self.hora_inicio = datetime.now().strftime('%H:%M:%S')

    def agregar_punto(self, equipo):
        if self.estado_partido == "Finalizado":
            return self.obtener_puntaje_display()

        otro_equipo = 'equipo2' if equipo == 'equipo1' else 'equipo1'

        if self.juego_en_tiebreak:
            self.puntuacion_juego[equipo] += 1
            if self.puntuacion_juego[equipo] >= 7 and \
               (self.puntuacion_juego[equipo] - self.puntuacion_juego[otro_equipo] >= 2):
                self._ganar_juego(equipo)
                self.juego_en_tiebreak = False
        else:
            if self.puntuacion_juego[equipo] == 3 and self.puntuacion_juego[otro_equipo] == 3:
                self.puntuacion_juego[equipo] = 4
            elif self.puntuacion_juego[equipo] == 4:
                self._ganar_juego(equipo)
            elif self.puntuacion_juego[otro_equipo] == 4:
                self.puntuacion_juego[otro_equipo] = 3
            else:
                self.puntuacion_juego[equipo] += 1

                if self.puntuacion_juego[equipo] >= 4 and \
                   (self.puntuacion_juego[equipo] - self.puntuacion_juego[otro_equipo] >= 2):
                    self._ganar_juego(equipo)

        self._verificar_partido_finalizado()
        return self.obtener_puntaje_display()

    def _ganar_juego(self, equipo_ganador):
        # Sumar juego al set actual
        if equipo_ganador == 'equipo1':
            self.sets_equipo1[self.set_actual] += 1
        else:
            self.sets_equipo2[self.set_actual] += 1

        puntos_eq1_str = self.puntuacion_display.get(self.puntuacion_juego['equipo1'], str(self.puntuacion_juego['equipo1']))
        puntos_eq2_str = self.puntuacion_display.get(self.puntuacion_juego['equipo2'], str(self.puntuacion_juego['equipo2']))
        self.historial_juegos.append(f"{puntos_eq1_str}-{puntos_eq2_str}")

        self._reiniciar_puntuacion_juego()
        self._verificar_ganador_set(equipo_ganador)

    def _reiniciar_puntuacion_juego(self):
        self.puntuacion_juego = {'equipo1': 0, 'equipo2': 0}

    def _verificar_ganador_set(self, equipo_que_gano_juego_recientemente):
        juegos_eq1 = self.sets_equipo1[self.set_actual]
        juegos_eq2 = self.sets_equipo2[self.set_actual]

        if self.juego_en_tiebreak:
            self._ganar_set(equipo_que_gano_juego_recientemente)
            return

        if (juegos_eq1 >= 6 or juegos_eq2 >= 6) and abs(juegos_eq1 - juegos_eq2) >= 2:
            ganador_set = 'equipo1' if juegos_eq1 > juegos_eq2 else 'equipo2'
            self._ganar_set(ganador_set)
        elif juegos_eq1 == 6 and juegos_eq2 == 6:
            self.juego_en_tiebreak = True
            print("¡Inicia Tie-break!")

    def _ganar_set(self, equipo_ganador):
        self.puntuacion_partido[equipo_ganador] += 1
        self.set_actual += 1
        # Solo reiniciar juegos del nuevo set si quedan sets
        if self.set_actual < 3:
            self.puntuacion_juego = {'equipo1': 0, 'equipo2': 0}
        self.juego_en_tiebreak = False

    def _verificar_partido_finalizado(self):
        if self.puntuacion_partido['equipo1'] == 2 or self.puntuacion_partido['equipo2'] == 2 or self.set_actual >= 3:
            self.estado_partido = "Finalizado"
            self.ganador = 'equipo1' if self.puntuacion_partido['equipo1'] == 2 else 'equipo2'
            print(f"¡Partido Finalizado! Ganador: {self.ganador}")
            
            match_data = {
                'fecha': datetime.now().strftime('%Y-%m-%d'),
                'hora': datetime.now().strftime('%H:%M:%S'),
                'equipo1_jugador1_id': self.jugadores_ids['equipo1'][0],
                'equipo1_jugador2_id': self.jugadores_ids['equipo1'][1],
                'equipo2_jugador1_id': self.jugadores_ids['equipo2'][0],
                'equipo2_jugador2_id': self.jugadores_ids['equipo2'][1],
                'sets_equipo1': self.puntuacion_partido['equipo1'],
                'sets_equipo2': self.puntuacion_partido['equipo2'],
                'historial_juegos_json': json.dumps(self.historial_juegos),
                'ganador_equipo': self.ganador
            }
            save_match(match_data)
            return True
        return False

    def obtener_puntaje_display(self):
        from datetime import datetime
        puntos_eq1_display = self.puntuacion_display.get(self.puntuacion_juego['equipo1'], str(self.puntuacion_juego['equipo1']))
        puntos_eq2_display = self.puntuacion_display.get(self.puntuacion_juego['equipo2'], str(self.puntuacion_juego['equipo2']))
        hora_actual = datetime.now().strftime('%H:%M:%S')
        return {
            'jugadores': self.jugadores_nombres,
            'sets_equipo1': self.sets_equipo1,
            'sets_equipo2': self.sets_equipo2,
            'puntos_equipo1': puntos_eq1_display,
            'puntos_equipo2': puntos_eq2_display,
            'estado_partido': self.estado_partido,
            'juego_en_tiebreak': self.juego_en_tiebreak,
            'hora_actual': hora_actual,
            'hora_inicio': self.hora_inicio,
            "ganador": self.ganador if hasattr(self, 'ganador') else None,
        }