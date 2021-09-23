import matplotlib.pyplot as plt
import structlog as structlog

import Labyrinthe.Labyrinthe as laby

logger = structlog.getLogger(__name__)


class Case:
    """
    Une case contient un booléen pour chacun de ses 4 murs
    Les coordonées vont de 0 au nombre de case sur la ligne ou colonne du labyrinthe
    Les coordonnées désignent le point en bas à gauche de la case
    """

    def __init__(self, labyrinthe: laby.Labyrinthe, abscisse=0, ordonnee=0, murHaut=True, murGauche=True, murDroit=True,
                 murBas=True):
        """
        Constructeur d'une case
        :param abscisse: coordonée de l'abscisse du mur
        :param ordonnee: coordonée de l'ordonnée du mur
        :param murHaut: booléen indiquant si la case a un mur vers le haut (nord)
        :param murGauche: booléen indiquant si la case a un mur vers la gauche (ouest)
        :param murDroit: booléen indiquant si la case a un mur vers la droite (est)
        :param murBas: booléen indiquant si la case a un mur vers le bas (sud)
        """
        self.labyrinthe = labyrinthe
        self.abscisse = abscisse
        self.ordonnee = ordonnee
        self.murHaut = murHaut
        self.murBas = murBas
        self.murGauche = murGauche
        self.murDroit = murDroit
        self.exploree = False
        self.distance = float("inf")

    def supprimerMurHaut(self):
        """
        Permet de suppprimer le mur du haut, utile dans la génération de labyrinthe
        Doit vérifier que ce n'est pas une case de la dernière ligne du labyrinthe (il suffit de regarder s'il existe
        une case au dessus)
        Modifie aussi la case du dessus
        :return: None
        """
        assert (self.abscisse, self.ordonnee + 1) in self.labyrinthe.cases.keys()
        self.murHaut = False
        self.labyrinthe.cases[(self.abscisse, self.ordonnee + 1)].murBas = False

    def supprimerMurBas(self):
        """
        Permet de suppprimer le mur du bas, utile dans la génération de labyrinthe
        Doit vérifier que ce n'est pas une case de la première ligne du labyrinthe (il suffit de regarder s'il existe
        une case au dessous)
        :return: None
        """
        assert (self.abscisse, self.ordonnee - 1) in self.labyrinthe.cases.keys()
        self.murBas = False
        self.labyrinthe.cases[(self.abscisse, self.ordonnee - 1)].murHaut = False

    def supprimerMurGauche(self):
        """
        Permet de suppprimer le mur de gauche, utile dans la génération de labyrinthe
        Doit vérifier que ce n'est pas une case de la première colonne du labyrinthe (il suffit de regarder s'il existe
        une case à gauche)
        :return: None
        """
        assert (self.abscisse - 1, self.ordonnee) in self.labyrinthe.cases.keys()
        self.murGauche = False
        self.labyrinthe.cases[(self.abscisse - 1, self.ordonnee)].murDroit = False

    def supprimerMurDroit(self):
        """
        Permet de suppprimer le mur de droite, utile dans la génération de labyrinthe
        Doit vérifier que ce n'est pas une case de la première colonne du labyrinthe (il suffit de regarder s'il existe
        une case à droite)
        :return: None
        """
        assert (self.abscisse + 1, self.ordonnee) in self.labyrinthe.cases.keys()
        self.murDroit = False
        self.labyrinthe.cases[(self.abscisse + 1, self.ordonnee)].murGauche = False

    def ploterCase(self, opti=True):
        """
        Trace la case
        opti : mode optimisé, ne trace que les lignes du haut et celles de gauche, l'idée étant que les autres lignes
        seront tracées par les cases de droite et celles du dessous.
        :return:
        """
        if self.murHaut:
            plt.plot([self.abscisse, self.abscisse + 1], [self.ordonnee + 1, self.ordonnee + 1], color="black")
        if self.murGauche:
            plt.plot([self.abscisse, self.abscisse], [self.ordonnee, self.ordonnee + 1], color="black")
        if not opti:
            if self.murBas:
                plt.plot([self.abscisse, self.abscisse + 1], [self.ordonnee, self.ordonnee], color="black")
            if self.murDroit:
                plt.plot([self.abscisse + 1, self.abscisse + 1], [self.ordonnee, self.ordonnee + 1], color="black")

    def getVoisins(self):
        """
        Renvoie une liste des cases accessible directement (donc sans mur entre les deux, et de distance 1)
        """
        voisins = []
        cases = self.labyrinthe.cases
        if not self.murHaut:
            voisins.append(cases[self.abscisse, self.ordonnee + 1])
        if not self.murBas:
            voisins.append(cases[self.abscisse, self.ordonnee - 1])
        if not self.murGauche:
            voisins.append(cases[self.abscisse - 1, self.ordonnee])
        if not self.murDroit:
            voisins.append((cases[self.abscisse + 1, self.ordonnee]))
        return voisins

    def __str__(self):
        """
        Affiche les coordonées
        """
        return f"[{self.abscisse}, {self.ordonnee}]"