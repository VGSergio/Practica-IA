from practica1 import agent_profunditat, agente_aestrella, agente_minimax, joc


def main():
    algo = 1
    rana = []
    match algo:
        case 0:
            rana.append(agent_profunditat.RanaProfunditat("Miquel"))
        case 1:
            rana.append(agente_aestrella.RanaAEstrella("Miquel"))
        case 2:
            rana = [agente_minimax.RanaMiniMax("Miquel"), agente_minimax.RanaMiniMax("Xavier")]
            pass
        case 3:
            print("No implementado")
            pass

    if len(rana) > 0:
        lab = joc.Laberint(rana, parets=True)
        lab.comencar()
    else:
        print("Elije un algoritmo a usar")


if __name__ == "__main__":
    main()
