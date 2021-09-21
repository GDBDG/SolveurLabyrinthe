from itertools import product
import logging_config

CST_CROIX = 0.3
import matplotlib.pyplot as plt


class Labyrinthe:
    def __init__(self, nbLigne, nbColonne):
        import Labyrinthe.Case as Case
        """
        Crée une grille pleine
        """
        self.nbLigne = nbLigne
        self.nbColonne = nbColonne
        self.cases = {(abscisse, ordonnee): Case.Case(self, abscisse, ordonnee) for abscisse, ordonnee in
                      product(range(nbLigne), range(nbColonne))}

    def plot_labyrinthe(self):
        """
        Trace le labyrinthe via matplotlib
        :return:
        """
        # Tracer les cases
        for case in self.cases.values():
            case.ploterCase()
        # Ajout de la ligne du bas et de la colonne de droite
        plt.plot([0, self.nbLigne], [0, 0], color="black")
        plt.plot([self.nbLigne, self.nbLigne], [0, self.nbColonne], color="black")
        # Affichage de l'entrée (Croix noire)
        plt.plot([0 + CST_CROIX, 1 - CST_CROIX], [0 + CST_CROIX, 1 - CST_CROIX], color="black")
        plt.plot([0 + CST_CROIX, 1 - CST_CROIX], [1 - CST_CROIX, 0 + CST_CROIX], color="black")
        plt.plot([self.nbLigne - 1 + CST_CROIX, self.nbLigne - CST_CROIX], [self.nbColonne - 1 + CST_CROIX, self.nbColonne - CST_CROIX], color="red")
        plt.plot([self.nbLigne - 1 + CST_CROIX, self.nbLigne - CST_CROIX], [self.nbColonne  - CST_CROIX, self.nbColonne -1 + CST_CROIX], color="red")
        plt.show()


if __name__ == '__main__':
    import GenerateurLabyrinthe.Mineur as Mineur
    logging_config.config_logging()
    laby = Labyrinthe(100, 100)
    mineur = Mineur.Mineur(labyrinthe=laby)
    mineur.creerLabyrinthe()
    laby.plot_labyrinthe()
