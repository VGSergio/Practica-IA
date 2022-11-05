"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Direccio, AccionsRana, ClauPercepcio


class RanaProfunditat(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(RanaProfunditat, self).__init__(*args, **kwargs)

    def pinta(self, display):
        pass

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pos_rana = percep[ClauPercepcio.POSICIO][self.nom]
        pos_pizza = percep[ClauPercepcio.OLOR]

        if pos_rana == pos_pizza:
            return AccionsRana.ESPERAR

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
