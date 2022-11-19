import copy
from queue import PriorityQueue

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Direccio, AccionsRana, ClauPercepcio
from practica1.agent import Estat

import heapq


class RanaAEstrella(joc.Rana):

    def __init__(self, *args, **kwargs):
        super(RanaAEstrella, self).__init__(*args, **kwargs)
        self.__accions = None

    def _cerca(self, estat: Estat):
        oberts = PriorityQueue()
        oberts.put((0, estat))

        tancats = set()

        actual = None
        while not oberts.empty():
            cost, actual = oberts.get()

            if actual.es_meta():
                break

            if actual in tancats:
                continue

            estats_fills = actual.genera_fills()

            for estat_f in estats_fills:
                oberts.put((estat_f["Coste"], estat_f))

            tancats.add(actual)

        if actual.es_meta():
            accions = [actual]
            iterador = actual

            while iterador.pare is not None:
                accio = iterador.pare

                accions.append(accio)
                iterador = iterador.pare
            self.__accions = accions

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        if self.esta_botant():
            return AccionsRana.ESPERAR

        estat = Estat(
            info=percep.to_dict() |
            {AccionsRana: AccionsRana.ESPERAR, Direccio: None, "Coste": 0})

        if self.__accions is None:
            self._cerca(estat=estat)

        if len(self.__accions) > 0:
            aux = self.__accions.pop()
            return aux[AccionsRana], aux[Direccio]
        else:
            return AccionsRana.ESPERAR


class Estat(Estat):

    def __init__(self, info: dict = None, pare=None):
        super(Estat, self).__init__(info, pare)
        self.heuristica()

    def __lt__(self, other):
        if self["Coste"] + self["Heuristica"] == other["Coste"] + other["Heuristica"]:
            return self["Heuristica"] < other["Heuristica"]
        return self["Coste"] + self["Heuristica"] < other["Coste"] + other["Heuristica"]

    def heuristica(self):
        pizza = self[ClauPercepcio.OLOR]
        pos = self[ClauPercepcio.POSICIO]
        name = list(pos.keys())[0]
        pos = pos[name]

        pos = list(pos)
        pizza = list(pizza)

        self["Heuristica"] = abs(pizza[0] - pos[0]) + abs(pizza[1] - pos[1])

    def genera_fills(self) -> list:
        fills = []

        for accio in AccionsRana:
            if accio != AccionsRana.ESPERAR:
                for move in Direccio:
                    coste = 1
                    if accio == AccionsRana.BOTAR:
                        coste = 6

                    padre = copy.deepcopy(self)
                    coste = coste + padre["Coste"]
                    info = padre.__info | {AccionsRana: accio, Direccio: move, "Coste": coste}
                    nou_estat = Estat(info=info, pare=padre)
                    if nou_estat.legal():
                        fills.append(nou_estat)

            else:
                padre = copy.deepcopy(self)
                coste = coste + padre["Coste"]
                info = padre.__info | {AccionsRana: accio, Direccio: None, "Coste": 0.5}
                nou_estat = Estat(info=info, pare=padre)
                if nou_estat.legal():
                    fills.append(nou_estat)

        return fills
