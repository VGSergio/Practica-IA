"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""

import copy

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
        aux = {AccionsRana: AccionsRana.ESPERAR, Direccio: None}
        if info is None:
            info = aux
        else:
            info = info | aux

        self.__info = info
        self.__pare = pare

    def __hash__(self):
        return hash(tuple(frozenset(self.__info)))

    def __getitem__(self, key):
        return self.__info[key]

    def __setitem__(self, key, value):
        self.__info[key] = value

    def __eq__(self, other):
        pos_self = self[ClauPercepcio.POSICIO]
        pos_other = other[ClauPercepcio.POSICIO]
        name_self = list(pos_self.keys())[0]
        name_other = list(pos_other.keys())[0]
        pos_self = pos_self[name_self]
        pos_other = pos_other[name_other]
        return (
                pos_self == pos_other
                and name_self == name_other
                and self[AccionsRana] == other[AccionsRana]
                and self[Direccio] == other[Direccio]
        )

    def legal(self) -> bool:
        pos = self[ClauPercepcio.POSICIO]
        nom = list(pos.keys())[0]
        pos = pos[nom]

        parets = self[ClauPercepcio.PARETS]

        tam = self[ClauPercepcio.MIDA_TAULELL]

        accio = self[AccionsRana]
        if accio is AccionsRana.ESPERAR:
            return True
        else:
            step = 1
            if accio is AccionsRana.BOTAR:
                step = 2
            direccio = self[Direccio]
            pos = list(pos)
            match direccio:
                case Direccio.DALT:
                    pos[1] -= step
                case Direccio.DRETA:
                    pos[0] += step
                case Direccio.BAIX:
                    pos[1] += step
                case Direccio.ESQUERRE:
                    pos[0] -= step
                case _:
                    print("Error at agent.legal, move switch")
            pos = tuple(pos)

        if pos not in parets and 0 <= pos[0] < tam[0] and 0 <= pos[1] < tam[1]:
            return True

        return False

    def es_meta(self) -> bool:
        return self[ClauPercepcio.POSICIO] == self[ClauPercepcio.OLOR]

    def genera_fill(self) -> list:
        estats_generats = []
        for accio in AccionsRana:
            if accio != AccionsRana.ESPERAR:
                info = {AccionsRana: accio, Direccio: None}
                for move in Direccio:
                    nou_estat = copy.deepcopy(self)
                    nou_estat.__pare = self
                    info[Direccio] = move
                    nou_estat.__info = self.__info | info
                    if not nou_estat.legal():
                        continue
                    estats_generats.append(nou_estat)

        return estats_generats

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value

    def __str__(self):
        return str(self.__info.values())
