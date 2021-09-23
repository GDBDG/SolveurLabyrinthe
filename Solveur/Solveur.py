import toolbox as toolbox

import Labyrinthe.Labyrinthe as Labyrinthe
import multiprocessing as mp
from Labyrinthe.Case import Case
import structlog
logger = structlog.getLogger(__name__)

class Solveur:
    def __init__(self, labyrinthe:Labyrinthe):
        """
        :param labyrinthe: instance de labyrinthe à résoudre
        """
        self.labyrinthe = labyrinthe

    def resolution(self):
        """
        Méthode qui résout un labyrinthe, et trace le chemin
        """
        pass

    def numerotationTotaleSequentielle(self):
        """
        Lance la numérotation de toutes les cases
        """
        self.numerotationSequentielle(self.labyrinthe.entree)


    def numerotationSequentielle(self, case: Case, distance = 0):
        """
        Méthode récusrive qui ajoute à chaque case sa distance à la sortie
        Sur un appel : va appeler la méthode sur les cases accessibles depuis la case *case*, et qui n'ont pas encore été
        numérotée (il suffit de vérifier que la distance est supérieure à *case*
        :param case: case depuis laquelle est effectuée la numérotation
        :param pool: pool de multiprocessing qui est utillisé pour lancer les appels
        """
        case.distance = min(case.distance, distance)
        logger.debug(f"Case d'appel : {case}, de distance : {case.distance}")
        logger.debug(f"Voisins : { [str(voisin) for voisin in case.getVoisins()]}")
        logger.debug(f"Distance des voisins : { [str(voisin.distance) for voisin in case.getVoisins()]}")
        caseAExplorer = [voisin for voisin in case.getVoisins() if voisin.distance > case.distance]
        logger.debug(f"caseAExplorer : {[str(voisin) for voisin in caseAExplorer]}")
        if caseAExplorer:
            for voisin in caseAExplorer:
                logger.debug(f"Appel de numérotation pour la case {str(voisin)} depuis la case {str(case)}")
                self.numerotationSequentielle(voisin, distance + 1)
