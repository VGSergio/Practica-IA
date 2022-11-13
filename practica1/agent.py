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
        if info is None:
            info = {}

        self.__info = info
        self.__pare = pare

    def __hash__(self):
        return hash(tuple(self.__info.items()))

    def __getitem__(self, key):
        return self.__info[key]

    def __setitem__(self, key, value):
        self.__info[key] = value

    def __eq__(self, other):
        """Overrides the default implementation"""
        return (
                self[ClauPercepcio.POSICIO] == other[ClauPercepcio.POSICIO]
        )

    def legal(self) -> bool:
        pos = self[ClauPercepcio.POSICIO]
        nom = list(pos.keys())[0]
        pos = pos[nom]

        parets = self[ClauPercepcio.PARETS]

        tam = self[ClauPercepcio.MIDA_TAULELL]

        if pos not in parets and 0 <= pos[0] <= tam[0] and 0 <= pos[1] <= tam[1]:
            return True

        return False

    def es_meta(self) -> bool:
        return self[ClauPercepcio.POSICIO] == self[ClauPercepcio.OLOR]

    def genera_fill(self) -> list:
        estats_generats = []
        for accio in AccionsRana:
            if accio == AccionsRana.BOTAR:
                nou_estat = copy.deepcopy(self)
                nou_estat.pare = (self, accio)
                if not nou_estat.legal():
                    continue
                estats_generats.append(nou_estat)
            else:
                for move in Direccio:
                    nou_estat = copy.deepcopy(self)
                    nou_estat.pare = (self, tuple[accio, move])
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
