import statistics
import time
from sys import setrecursionlimit

import logging_config
from GenerateurLabyrinthe import Mineur
from Labyrinthe.Labyrinthe import Labyrinthe
from constantes import RECURSION_LIMITE
import matplotlib.pyplot as plt
import structlog
logger = structlog.getLogger(__name__)
def getStatsMineur(nbIteration=10, tailleMin=5, tailleMax=50):
    """
    :param nbIteration: nombre de labyrinthe généré par taille
    :tailleMin: taille minimum des labyrinthe testées (positif)
    :tailleMax: taille max
    """
    logging_config.config_logging()
    logger.info(f"Appel de getStatMineur avec {nbIteration} itération par valeur, entre les valeurs {tailleMin} et {tailleMax}.")
    setrecursionlimit(RECURSION_LIMITE)
    listeTemps = []
    for taille in range(tailleMin, tailleMax + 1):
        aux = []
        logger.info(f"Calculs pour la taille : {taille}")
        for _ in range(nbIteration):
            laby = Labyrinthe(tailleMin, tailleMax)
            mineur = Mineur.Mineur(labyrinthe=laby)
            t0 = time.time()
            mineur.creerLabyrinthe()
            t1 = time.time()
            aux.append(t1 - t0)
        listeTemps.append(statistics.mean(aux))
    plt.plot(list(range(tailleMin, tailleMax + 1)), listeTemps, )
    plt.show()

if __name__ == '__main__':
    getStatsMineur()