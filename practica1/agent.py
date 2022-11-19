"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
import abc

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Direccio, AccionsRana, ClauPercepcio


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

    def pinta(self, display):
        pass

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass


class Estat:

    def __init__(self, info: dict = None, pare=None):
        if info is None:
            info = {}

        self.__info = info
        self.__pare = pare

        pos = self[ClauPercepcio.POSICIO]
        aux = list(pos.keys())[0]
        self[ClauPercepcio.POSICIO][aux] = self.__sigiente_casilla()

    def __hash__(self):
        return hash(tuple(self.__info))

    def __getitem__(self, key):
        return self.__info[key]

    def __setitem__(self, key, value):
        self.__info[key] = value

    def __eq__(self, other):
        return (
                self[ClauPercepcio.POSICIO] == other[ClauPercepcio.POSICIO]
                and self[AccionsRana] == other[AccionsRana]
                and self[Direccio] == other[Direccio]
        )

    def legal(self) -> bool:
        parets = self[ClauPercepcio.PARETS]
        tam = self[ClauPercepcio.MIDA_TAULELL]
        new_pos = self[ClauPercepcio.POSICIO]

        aux = list(new_pos.keys())
        new_pos = new_pos[aux[0]]

        if (tam[0] > new_pos[0] >= 0) and (tam[1] > new_pos[1] >= 0):
            if new_pos not in parets:
                return True

        return False

    def es_meta(self) -> bool:
        pos = self[ClauPercepcio.POSICIO]
        aux = list(pos.keys())
        pos = pos[aux[0]]
        return pos == self[ClauPercepcio.OLOR]

    @abc.abstractmethod
    def genera_fills(self) -> list:
        pass

    def __sigiente_casilla(self) -> tuple:
        pos: dict[str, tuple[int, int]] = self[ClauPercepcio.POSICIO]
        pos = pos[list(pos.keys())[0]]

        accio = self[AccionsRana]
        if accio is AccionsRana.ESPERAR:
            return pos

        step = 1
        if accio is AccionsRana.BOTAR:
            step = 2

        direccio = self[Direccio]
        pos = list(pos)

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

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value

    def __str__(self):
        return str(self.__info.values())
