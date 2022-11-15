import time

import pygame

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Direccio, AccionsRana, ClauPercepcio
from practica1.agent import Estat


class RanaProfunditat(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(RanaProfunditat, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def _cerca(self, estat: Estat):
        self.__oberts = []
        self.__tancats = set()

        self.__oberts.append(estat)

        max_profundidad = 120
        profundidad = 1

        actual = None
        while len(self.__oberts) > 0 and profundidad <= max_profundidad:
            actual = self.__oberts.pop()

            if actual in self.__tancats:
                continue

            if not actual.legal():
                self.__tancats.add(actual)
                continue

            estats_fills = actual.genera_fill()

            if actual.es_meta():
                break

            for estat_f in estats_fills:
                self.__oberts.append(estat_f)

            self.__tancats.add(actual)
            profundidad += 1

        if actual is None:
            raise ValueError("Error impossible")

        if actual.es_meta():
            accions = []
            iterador = actual

            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            self.__accions = accions

            return True
        else:
            self.__accions = [actual]
            return False

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        if self.esta_botant():
            return AccionsRana.ESPERAR

        estat = Estat(percep.to_dict())

        if self.__accions is None:
            self._cerca(estat=estat)

        if len(self.__accions) > 0:
            aux = self.__accions.pop()
            return aux[AccionsRana], aux[Direccio]
        else:
            aux = self.__tancats.pop()
            return aux[AccionsRana], aux[Direccio]
