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

        count = 0
        actual = None
        while not len(self.__oberts) == 0:
            actual = self.__oberts.pop()
            count += 1

            if actual and actual.es_meta():
                explored = []
                while actual.pare:
                    explored.append(actual)
                    actual = actual.pare
                break

            estats_fills = actual.genera_fill()

            for estat_f in estats_fills:
                if estat_f not in self.__tancats:
                    self.__oberts.append(estat_f)

            self.__tancats.add(actual)

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
            return False

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        if self.esta_botant():
            return AccionsRana.ESPERAR

        estat = Estat(percep.to_dict())
        self.__estat = estat

        if self.__accions is None:
            self._cerca(estat=estat)

        if self.__accions:
            print("1")
            aux = self.__accions.pop()
            return aux[AccionsRana], aux[Direccio]
        else:
            print("2")
            aux = self.__tancats.pop()
            print(aux[ClauPercepcio.POSICIO])
            while not aux.legal():
                aux = self.__tancats.pop()
                print(aux[ClauPercepcio.POSICIO])
            return aux[AccionsRana], aux[Direccio]
