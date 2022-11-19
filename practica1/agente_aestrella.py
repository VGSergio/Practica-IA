import copy
from queue import PriorityQueue

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Direccio, AccionsRana, ClauPercepcio
from practica1 import agent
from practica1.agent import Estat

import heapq


class RanaAEstrella(joc.Rana):

    def __init__(self, *args, **kwargs):
        super(RanaAEstrella, self).__init__(*args, **kwargs)
        self.__accions = None

    def _cerca(self, estat: Estat):
        frontier = PriorityQueue()
        frontier.put(estat, 0)
        came_from = dict()
        cost_so_far = dict()
        came_from[estat] = None
        cost_so_far[estat] = 0

        current = None
        while not frontier.empty():
            current = frontier.get()
            print(current)
            if current.es_meta():
                break

            fills = current.genera_fills()

            for fill in fills:
                print(fill)
                new_cost = fill["Coste"] + fill["Heuristica"]
                if fill not in cost_so_far or new_cost < cost_so_far[fill]:
                    cost_so_far[fill] = new_cost
                    priority = new_cost + fill["Heuristica"]
                    frontier.put(fill, priority)
                    came_from[fill] = current

        if current.es_meta():
            accions = [current]
            iterador = current

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


class Estat(agent.Estat):

    def __init__(self, info: dict = None, pare=None):
        super(Estat, self).__init__(info, pare)
        self.heuristica()

    def heuristica(self):
        pizza = self[ClauPercepcio.OLOR]
        pos = self[ClauPercepcio.POSICIO]
        name = list(pos.keys())[0]
        pos = pos[name]

        pos = list(pos)
        pizza = list(pizza)

        heu = abs(pizza[0] - pos[0]) + abs(pizza[1] - pos[1])

        self["Heuristica"] = heu

    def genera_fills(self) -> list:
        fills = []

        for accio in AccionsRana:

            coste = None
            match accio:
                case AccionsRana.MOURE:
                    coste = 1
                case AccionsRana.ESPERAR:
                    coste = 0.5
                case AccionsRana.BOTAR:
                    coste = 6

            padre = copy.deepcopy(self)
            coste = coste + padre["Coste"]
            info = padre.__info | {AccionsRana: accio, Direccio: None, "Coste": coste}
            if accio != AccionsRana.ESPERAR:
                for move in Direccio:
                    info[Direccio] = move
                    nou_estat = Estat(info=info, pare=padre)
                    nou_estat[ClauPercepcio.POSICIO] = nextpos
                    if nou_estat.legal():
                        fills.append(nou_estat)
            else:
                pass
        return fills
