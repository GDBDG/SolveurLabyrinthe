from itertools import product
import structlog

from constantes import COULEUR_MUR, COULEUR_ENTREE, COULEUR_SORTIE, CST_CROIX

logger = structlog.getLogger(__name__)

import matplotlib.pyplot as plt


class Labyrinthe:
    def __init__(self, nbLigne, nbColonne):
        import Labyrinthe.Case as Case
        """
        Crée une grille pleine
        """
        logger.debug("Instanciatoin d'un labyrinthe")
        self.nbLigne = nbLigne
        self.nbColonne = nbColonne
        self.cases = {(abscisse, ordonnee): Case.Case(self, abscisse, ordonnee) for abscisse, ordonnee in
                      product(range(nbLigne), range(nbColonne))}
        self.sortie = self.cases[self.nbLigne - 1, self.nbColonne - 1]
        self.entree = self.cases[0, 0]
        self.entree.distance = 0

    def plot_labyrinthe(self):
        """
        Trace le labyrinthe via matplotlib
        :return:
        """
        logger.info("Plotage d'un labyrinthe")
        # Tracer les cases
        for case in self.cases.values():
            case.ploterCase()
        # Ajout de la ligne du bas et de la colonne de droite
        plt.plot([0, self.nbLigne], [0, 0], color=COULEUR_MUR)
        plt.plot([self.nbLigne, self.nbLigne], [0, self.nbColonne], color=COULEUR_MUR)
        # Affichage de l'entrée (Croix noire)
        plt.plot([0 + CST_CROIX, 1 - CST_CROIX], [0 + CST_CROIX, 1 - CST_CROIX], color=COULEUR_ENTREE)
        plt.plot([0 + CST_CROIX, 1 - CST_CROIX], [1 - CST_CROIX, 0 + CST_CROIX], color=COULEUR_ENTREE)
        plt.plot([self.nbLigne - 1 + CST_CROIX, self.nbLigne - CST_CROIX],
                 [self.nbColonne - 1 + CST_CROIX, self.nbColonne - CST_CROIX],
                 color=COULEUR_SORTIE,
                 )
        plt.plot([self.nbLigne - 1 + CST_CROIX, self.nbLigne - CST_CROIX],
                 [self.nbColonne - CST_CROIX, self.nbColonne - 1 + CST_CROIX],
                 color=COULEUR_SORTIE,
                 )
