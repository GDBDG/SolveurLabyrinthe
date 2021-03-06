from sys import setrecursionlimit

import logging_config
from Labyrinthe.Labyrinthe import Labyrinthe
from Solveur.Solveur import Solveur
import matplotlib.pyplot as plt
import MesurePerformance.recorder as recorder
from constantes import RECURSION_LIMITE

if __name__ == '__main__':
    import GenerateurLabyrinthe.Mineur as Mineur
    setrecursionlimit(RECURSION_LIMITE)
    logging_config.config_logging()
    laby = Labyrinthe(5, 5)
    mineur = Mineur.Mineur(labyrinthe=laby)
    mineur.creerLabyrinthe()
    laby.plot_labyrinthe()
    # plt.show()
    solveur = Solveur(laby)
    solveur.numerotationTotaleParallele()
    cases = laby.cases
    distances = [[cases[x,y].distance for x in range(laby.nbLigne)] for y in range(laby.nbColonne)]
    print(f"Liste des distances : {distances}")
    solveur.ploterSolution()
    print(f"temps de génération du labyrinthe : {[(key, valeur) for key, valeur in recorder.listeTemps.items()]}")
    plt.show()