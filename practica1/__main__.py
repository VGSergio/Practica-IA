from practica1 import agent_profunditat, agente_aestrella, joc


def main():
    algo = 0
    rana = None
    match algo:
        case 0:
            rana = agent_profunditat.RanaProfunditat("Miquel")
        case 1:
            rana = agente_aestrella.RanaAEstrella("Miquel")
        case 2:
            print("No implementado")
            pass
        case 3:
            print("No implementado")
            pass

    if rana:
        lab = joc.Laberint([rana], parets=True)
        lab.comencar()
    else:
        print("Elije un algoritmo a usar")


if __name__ == "__main__":
    main()
