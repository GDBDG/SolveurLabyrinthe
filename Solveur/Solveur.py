import multiprocessing
import multiprocessing.pool
import os
from itertools import product

import daemon as daemon
import psutil
import toolbox as toolbox

import Labyrinthe.Labyrinthe as Labyrinthe
import multiprocessing as mp
from Labyrinthe.Case import Case
import structlog

logger = structlog.getLogger(__name__)


class Solveur:
    def __init__(self, labyrinthe: Labyrinthe):
        """
        :param labyrinthe: instance de labyrinthe à résoudre
        """
        logger.info("Instanciation d'un solveur")
        self.labyrinthe = labyrinthe

    def numerotationTotaleSequentielle(self):
        """
        Lance la numérotation de toutes les cases
        """
        logger.info("Appel de la numérotation des cases")
        self.numerotationSequentielle(self.labyrinthe.entree)

    def numerotationSequentielle(self, case: Case, distance=0):
        """
        Méthode récusrive qui ajoute à chaque case sa distance à la sortie
        Sur un appel : va appeler la méthode sur les cases accessibles depuis la case *case*, et qui n'ont pas encore été
        numérotée (il suffit de vérifier que la distance est supérieure à *case*
        :param case: case depuis laquelle est effectuée la numérotation
        :param pool: pool de multiprocessing qui est utillisé pour lancer les appels
        """
        case.distance = min(case.distance, distance)
        logger.debug(f"Case d'appel : {case}, de distance : {case.distance}")
        logger.debug(f"Voisins : {[str(voisin) for voisin in case.getVoisins()]}")
        logger.debug(f"Distance des voisins : {[str(voisin.distance) for voisin in case.getVoisins()]}")
        caseAExplorer = [voisin for voisin in case.getVoisins() if voisin.distance > case.distance]
        logger.debug(f"caseAExplorer : {[str(voisin) for voisin in caseAExplorer]}")
        if caseAExplorer:
            for voisin in caseAExplorer:
                logger.debug(f"Appel de numérotation pour la case {str(voisin)} depuis la case {str(case)}")
                self.numerotationSequentielle(voisin, distance + 1)

    def numerotationTotaleParallele(self):
        """
        listDistance : Array partagé avec les distances.
        LA distance de la case d'abscisse x et d'ordonnée y sera le y*nbColonne + x
        """
        process_id = os.getpid()
        manager = multiprocessing.Manager()
        listDistance = manager.list([float("inf") for _ in range(self.labyrinthe.nbLigne*self.labyrinthe.nbColonne)])
        listDistance[0] = 0
        numerotationParallele(process_id, self.labyrinthe.entree, self.labyrinthe, listDistance, distance=0)
        for x,y in product(range(self.labyrinthe.nbLigne), range(self.labyrinthe.nbColonne)):
            self.labyrinthe.cases[(x,y)].distance = listDistance[y*self.labyrinthe.nbColonne + x]
        logger.debug(
            f"Liste des distances : {[[self.labyrinthe.cases[x, y].distance for x in range(self.labyrinthe.nbLigne)] for y in range(self.labyrinthe.nbColonne)]}")

    def resolution(self):
        """
        Méthode qui crée la liste des cases à relier, correspondant au chemin vers la sortie
        Au vu de la méthode de génération, ce chemin est unique, cette hypothèse est nécessaire
        pour cette méthode
        """
        logger.info("Calcul des cases à relier")
        logger.debug(f"Distance à la sortie : {self.labyrinthe.sortie.distance}")
        caseARelier = [self.labyrinthe.sortie]
        derniereCase = self.labyrinthe.sortie
        while derniereCase != self.labyrinthe.entree:
            logger.debug(f"derniereCase : {str(derniereCase)}, de distance : {derniereCase.distance}")
            for voisin in derniereCase.getVoisins():
                if voisin.distance == derniereCase.distance - 1:
                    derniereCase = voisin
                    caseARelier.append(derniereCase)
                    break
        return caseARelier

    def ploterSolution(self):
        """
        Ne nécessite pas un labyrinthe déjà résolu (le fait)
        Ne trace pas le labyrinthe
        """
        logger.info("Affichage de la solution")
        casesARelier = self.resolution()
        for case1, case2 in zip(casesARelier[:-1], casesARelier[1:]):
            case1.relierCases(case2)


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    @property
    def _get_daemon(self):
        return False

    # @daemon.setter
    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class NoDaemonContext(type(multiprocessing.get_context())):
    Process = NoDaemonProcess


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    def __init__(self, *args, **kwargs):
        kwargs['context'] = NoDaemonContext()
        super(MyPool, self).__init__(*args, **kwargs)


def numerotationParallele(main_process_id, case: Case, labyrinthe, listDistance, distance=0):
    # case.distance = min(case.distance, distance)
    listDistance[case.abscisse + case.ordonnee*labyrinthe.nbColonne] = \
        min(listDistance[case.abscisse + case.ordonnee*labyrinthe.nbColonne], distance)
    logger.debug(
        f"Liste des distances : {listDistance}")
    logger.debug(f"Case d'appel : {case}, de distance : {case.distance}")
    logger.debug(f"Voisins : {[str(voisin) for voisin in case.getVoisins()]}")
    logger.debug(f"Distance des voisins : {[str(listDistance[voisin.abscisse + voisin.ordonnee*labyrinthe.nbColonne]) for voisin in case.getVoisins()]}")
    caseAExplorer = [voisin for voisin in case.getVoisins() if listDistance[voisin.abscisse + voisin.ordonnee*labyrinthe.nbColonne] > listDistance[case.abscisse + case.ordonnee*labyrinthe.nbColonne]]
    logger.debug(f"caseAExplorer : {[str(voisin) for voisin in caseAExplorer]}")
    if caseAExplorer:
        list_param = []
        for voisin in caseAExplorer:
            logger.debug(f"Appel de numérotation pour la case {str(voisin)} depuis la case {str(case)}")
            # find winnig feature
            list_param.append([main_process_id, voisin, labyrinthe,listDistance, distance + 1])

            pool = MyPool(multiprocessing.cpu_count())
            pool.starmap(numerotationParallele, (list_param))
            pool.close()
            pool.join()
