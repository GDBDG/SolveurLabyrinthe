import copy
import time
from sys import setrecursionlimit
import matplotlib.pyplot as plt
import statistics

import logging_config
from Labyrinthe.Labyrinthe import Labyrinthe
from Solveur.Solveur import Solveur
from constantes import RECURSION_LIMITE
import structlog

logger = structlog.getLogger(__name__)

def statsSolveurs():
    import GenerateurLabyrinthe.Mineur as Mineur
    setrecursionlimit(RECURSION_LIMITE)
    logging_config.config_logging()
    laby = Labyrinthe(5, 5)
    mineur = Mineur.Mineur(labyrinthe=laby)
    mineur.creerLabyrinthe()
    tempsParalleles = []
    tempsSequentiels = []
    for i in range(5,10):
        laby = Labyrinthe(i,i )
        logger.info(f"Mesures pour une taille de {i}")
        auxParallele = []
        auxSequentiel = []
        for _ in range(5):
            solveur = Solveur(copy.deepcopy(laby))
            t0 = time.time()
            solveur.numerotationTotaleParallele()
            t1 = time.time()
            auxParallele.append(t1 - t0)
            solveur = Solveur(copy.deepcopy(laby))
            t0 = time.time()
            solveur.numerotationTotaleSequentielle()
            t1 = time.time()
            auxSequentiel.append(t1 - t0)
        tempsParalleles.append(statistics.mean(auxParallele))
        tempsSequentiels.append(statistics.mean(auxSequentiel))
    plt.plot(range(5,10),tempsParalleles, label="Solveur parallèle")
    plt.plot(range(5,10),tempsSequentiels, label="Solveur séquentiel")
    plt.legend(loc = "upper left")
    plt.show()

if __name__ == '__main__':
    statsSolveurs()