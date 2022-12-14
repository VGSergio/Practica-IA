import copy
from queue import PriorityQueue

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Direccio, AccionsRana, ClauPercepcio
from practica1.agent import Estat


def minimax(turno_max: bool, profundidad: int, estat: Estat):
    if estat.es_meta() or profundidad == 0:
        return estat.evaluar(), estat

    if turno_max:
        hijos = estat.genera_fills(True)
        puntuacion_max = -2
        accion_max = AccionsRana.ESPERAR
        for hijo in hijos:
            puntuacion, accion = minimax(False, profundidad - 1, hijo)
            if puntuacion > puntuacion_max:
                puntuacion_max = puntuacion
                accion_max = accion
                if puntuacion_max > 0:
                    break
        return puntuacion_max, accion_max
    else:
        hijos = estat.genera_fills(False)
        puntuacion_min = 2
        accion_min = AccionsRana.ESPERAR
        for hijo in hijos:
            puntuacion, accion = minimax(True, profundidad - 1, hijo)
            if puntuacion < puntuacion_min:
                puntuacion_min = puntuacion
                accion_min = accion
                if puntuacion_min < 0:
                    break
        return puntuacion_min, accion_min


class RanaMiniMax(joc.Rana):

    def __init__(self, *args, **kwargs):
        super(RanaMiniMax, self).__init__(*args, **kwargs)

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        if self.esta_botant():
            return AccionsRana.ESPERAR

        estat = Estat(info=percep.to_dict(), turno=self.nom)
        if estat.es_meta():
            return AccionsRana.ESPERAR

        turno_max = False
        if estat.get_max() == self.nom:
            turno_max = True

        _, accion = minimax(turno_max=turno_max, profundidad=3, estat=estat)

        if accion and accion is not AccionsRana.ESPERAR:
            return accion[self.nom][AccionsRana], accion[self.nom][Direccio]
        else:
            return AccionsRana.ESPERAR


class Estat(Estat):

    def __init__(self, info: dict = None, pare=None, turno: str = ''):
        if info is None:
            info = {}

        self.__info = info
        self.__pare = pare

        players = self[ClauPercepcio.POSICIO].keys()
        for player in players:
            pos = self[ClauPercepcio.POSICIO][player]
            self[player] = {AccionsRana: AccionsRana.ESPERAR, Direccio: None, ClauPercepcio.POSICIO: pos}
        self["Turno"] = turno

    def genera_fills(self, turno_max) -> list:
        fills = []

        for accio in AccionsRana:
            if accio != AccionsRana.ESPERAR:
                for move in Direccio:
                    padre = copy.deepcopy(self)
                    nou_estat = Estat(info=padre.__info, pare=padre)
                    if turno_max:
                        player = nou_estat.get_max()
                    else:
                        player = nou_estat.get_min()
                    nou_estat[player][AccionsRana] = accio
                    nou_estat[player][Direccio] = move
                    pos = nou_estat[player][ClauPercepcio.POSICIO]
                    nou_estat[player][ClauPercepcio.POSICIO] = nou_estat.__sigiente_casilla(pos, accio, move)
                    nou_estat[ClauPercepcio.POSICIO][player] = nou_estat[player][ClauPercepcio.POSICIO]
                    nou_estat["Turno"] = player
                    if nou_estat.legal():
                        fills.append(nou_estat)

        return fills

    def get_max(self) -> str:
        players = self.__get_players()
        return players[0]

    def get_min(self) -> str:
        players = self.__get_players()
        return players[1]

    def __get_players(self):
        ranas = self[ClauPercepcio.POSICIO]
        noms = []
        for rana in ranas:
            noms.append(rana)

        return noms

    def __sigiente_casilla(self, actual, accio: AccionsRana, direccio: Direccio) -> tuple:
        if accio is AccionsRana.ESPERAR:
            return actual

        step = 1
        if accio is AccionsRana.BOTAR:
            step = 2

        pos = list(actual)

        match direccio:
            case Direccio.ESQUERRE:
                pos[0] -= step
            case Direccio.DRETA:
                pos[0] += step
            case Direccio.DALT:
                pos[1] -= step
            case Direccio.BAIX:
                pos[1] += step

        return tuple(pos)

    def es_meta(self) -> bool:
        posiciones = self[ClauPercepcio.POSICIO].values()
        return posiciones in self[ClauPercepcio.OLOR]

    def evaluar(self) -> int:
        if self.es_meta():
            player_max = self.get_max()
            if self[player_max][ClauPercepcio.POSICIO] == self[ClauPercepcio.OLOR]:
                return 1
            else:
                return -1
        return 0

    def legal(self) -> bool:
        player = self["Turno"]
        parets = self[ClauPercepcio.PARETS]
        tam = self[ClauPercepcio.MIDA_TAULELL]
        new_pos = self[player][ClauPercepcio.POSICIO]

        new_pos = list(new_pos)

        if (tam[0] > new_pos[0] >= 0) and (tam[1] > new_pos[1] >= 0):
            if new_pos not in parets:
                return True

        return False

    def __eq__(self, other):
        return self.__info == other.__info

    def __hash__(self):
        return hash(tuple(self.__info))
