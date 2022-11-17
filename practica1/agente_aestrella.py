from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Direccio, AccionsRana, ClauPercepcio
from practica1 import agent
from practica1.agent import Estat

import heapq


class RanaAEstrella(joc.Rana):

    def __init__(self, *args, **kwargs):
        super(RanaAEstrella, self).__init__(*args, **kwargs)
        self.__queue = heapq

    def _cerca(self, estat: Estat):
        pass

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass


class Estat(agent.Estat):

    def __init__(self, info: dict = None, pare=None):
        aux = {'Cost': 0}
        if info is None:
            info = aux
        else:
            info = info | aux

        self.__info = info
        self.__pare = pare

        super(Estat, self).__init__(info=info, pare=None)

    def __eq__(self, other):
        return (
                self['Cost'] == other['Cost']
                and super(Estat, self).__eq__(self, other)
        )

    def genera_fill(self) -> list:
        pass

    def heuristica(self):
        """
        cost = self['Cost']
        accio = self[AccionsRana]
        match accio:
            case AccionsRana.MOURE:
                cost += 1
            case AccionsRana.ESPERAR:
                cost += 0.5
            case AccionsRana.BOTAR:
                cost += 6
        """

        pizza = self[ClauPercepcio.OLOR]
        pos = self[ClauPercepcio.POSICIO]
        name = list(pos.keys())[0]
        pos = pos[name]

        pos = list(pos)
        pizza = list(pizza)

        heu = abs(pizza[0]-pos[0]) + abs(pizza[1]-pos[1])

        tuple(pos)

        return heu
