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

        iterations = 0
        max_iterations = 1000

        actual = None
        while len(self.__oberts) > 0 and iterations < max_iterations:
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
            iterations += 1

        if actual is None:
            raise ValueError("Error impossible")

        if actual.es_meta():
            accions = []
            iterador = actual

            while iterador.pare is not None:
                pare, accio = iterador.pare

                print("pare", pare)
                print("accio", accio)

                accions.append(accio)
                iterador = pare
            self.__accions = accions
            return True
        else:
            return False

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estat = Estat(percep.to_dict())

        print("")
        print(self.__oberts)
        print(self.__tancats)
        print(self.__accions)

        if self.__accions is None:
            self._cerca(estat=estat)

        if self.__accions is not None:
            if len(self.__accions) > 0:
                return self.__accions.pop()
        else:
            estat = self.__tancats.pop()
            print(estat.__getitem__(AccionsRana), estat.__getitem__(Direccio))
            return estat.__getitem__(AccionsRana), estat.__getitem__(Direccio)

        """
        pos_rana = percep[ClauPercepcio.POSICIO][self.nom]
        pos_pizza = percep[ClauPercepcio.OLOR]

        if pos_rana == pos_pizza:
            return pygame.QUIT

        dif_x = pos_rana[0] - pos_pizza[0]
        dif_y = pos_rana[1] - pos_pizza[1]
        direccio = None
        if dif_x != 0:
            if dif_x > 0:
                direccio = Direccio.ESQUERRE
            if dif_x < 0:
                direccio = Direccio.DRETA
            return AccionsRana.MOURE, direccio
        if dif_y != 0:
            if dif_y > 0:
                direccio = Direccio.DALT
            if dif_y < 0:
                direccio = Direccio.BAIX
            return AccionsRana.MOURE, direccio
        """