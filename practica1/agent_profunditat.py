import copy

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Direccio, AccionsRana, ClauPercepcio
from practica1.agent import Estat

from collections import deque


class RanaProfunditat(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(RanaProfunditat, self).__init__(*args, **kwargs)
        self.__accions = None

    def _cerca(self, estat: Estat):
        oberts = deque()
        tancats = set()

        oberts.append(estat)

        actual = None
        while len(oberts) > 0:
            actual = oberts.popleft()

            if actual.es_meta():
                break

            if actual in tancats:
                continue

            if not actual.legal():
                tancats.add(actual)
                continue

            estats_fills = actual.genera_fills()

            for estat_f in estats_fills:
                oberts.append(estat_f)

            tancats.add(actual)

        if actual is None:
            raise ValueError("Error impossible")

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

        estat = Estat(info=percep.to_dict() | {AccionsRana: AccionsRana.ESPERAR, Direccio: None})

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

    def genera_fills(self) -> list:
        fills = []

        for accio in AccionsRana:
            if accio != AccionsRana.ESPERAR:
                for move in Direccio:
                    padre = copy.deepcopy(self)
                    info = padre.__info | {AccionsRana: accio, Direccio: move}
                    nou_estat = Estat(info=info, pare=padre)
                    if nou_estat.legal():
                        fills.append(nou_estat)
        return fills
