from sys import setrecursionlimit

import logging_config
from Labyrinthe.Labyrinthe import Labyrinthe
from Solveur.Solveur import Solveur
import matplotlib.pyplot as plt

from constantes import RECURSION_LIMITE

if __name__ == '__main__':
    import GenerateurLabyrinthe.Mineur as Mineur
    setrecursionlimit(RECURSION_LIMITE)
    logging_config.config_logging()
    laby = Labyrinthe(50, 50)
    mineur = Mineur.Mineur(labyrinthe=laby)
    mineur.creerLabyrinthe()
    laby.plot_labyrinthe()
    solveur = Solveur(laby)
    solveur.numerotationTotaleSequentielle()
    cases = laby.cases
    distances = [[cases[x,y].distance for x in range(laby.nbLigne)] for y in range(laby.nbColonne)]
    print(f"Liste des distances : {distances}")
    solveur.ploterSolution()
    plt.show()