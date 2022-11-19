import abc
import copy
from queue import PriorityQueue

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Direccio, AccionsRana, ClauPercepcio
from practica1.agent import Estat


def _get_players(estat: Estat):
    ranas = estat[ClauPercepcio.POSICIO]
    noms = []
    for rana in ranas:
        noms.append(rana)

    return noms


def is_end(estat: Estat):
    posiciones = estat[ClauPercepcio.POSICIO].values()
    return posiciones in estat[ClauPercepcio.OLOR]


class RanaMiniMax(joc.Rana):

    def __init__(self, *args, **kwargs):
        super(RanaMiniMax, self).__init__(*args, **kwargs)
        self.__accions = None

    def minimax(self, estat: Estat, turno_max: bool):

        fills = estat.genera_fills(turno_max)

        for fill in fills:
            print(fill)

    # Player 0 is max
    def max(self, estat: Estat):
        # -1 - loss
        # 1  - win
        maxv = -2

        end = is_end(estat)

    def min(self):
        pass

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        if self.esta_botant():
            return AccionsRana.ESPERAR

        estat = Estat(info=percep.to_dict())

        if self.__accions is None:
            self.minimax(estat=estat, turno_max=True)

        if len(self.__accions) > 0:
            aux = self.__accions.pop()
            return aux[AccionsRana], aux[Direccio]
        else:
            return AccionsRana.ESPERAR


class Estat(Estat):

    def __init__(self, info: dict = None, pare=None):
        if info is None:
            info = {}

        self.__info = info | {AccionsRana: [], Direccio: []}
        self.__pare = pare

        players = self[ClauPercepcio.POSICIO].keys()
        for player in players:
            self[AccionsRana].append({player: AccionsRana.ESPERAR})
            self[Direccio].append({player: None})

    def genera_fills(self, turno_max) -> list:
        indice = 0 if turno_max else 1
        fills = []

        for accio in AccionsRana:
            if accio != AccionsRana.ESPERAR:
                for move in Direccio:
                    padre = copy.deepcopy(self)
                    nou_estat = Estat(info=padre.__info, pare=padre)
                    player = _get_players(padre)[indice]
                    nou_estat[AccionsRana][indice][player] = accio
                    nou_estat[Direccio][indice][player] = move
                    pos = nou_estat[ClauPercepcio.POSICIO][player]
                    nou_estat[ClauPercepcio.POSICIO][player] = self.__sigiente_casilla(pos, accio, move)
                    if nou_estat.legal():
                        fills.append(nou_estat)

        return fills

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
