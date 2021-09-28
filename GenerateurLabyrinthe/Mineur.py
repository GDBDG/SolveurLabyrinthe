import Labyrinthe.Labyrinthe as laby
import Labyrinthe.Case as Case
import random
import structlog
logger = structlog.getLogger(__name__)
from MesurePerformance.recorder import mesureTemps

class Mineur:
    """
    Le mineur va créer le labyrinthe selon l'algo du "mineur" :
    Le mineur casse un mur si la case à côté n'est pas déjà visitée,
    Il ne peut pas aller dans une case déjà visitée sauf en cas de demi tour
    Il fait demi tour si aucune direction n'est disponible
    Ses coordonées correspondent au point en bas à gauche de sa case.
    (pour correspondre aux clés des cases)
    """
    # @mesureTemps("init Mineur")
    def __init__(self, labyrinthe: laby.Labyrinthe):
        """
        Initialise le mineur, il part de la case de départ (0,0)
        :param labyrinthe:
        """
        self.labyrinthe = labyrinthe
        self.abscisse = 0
        self.ordonnee = 0
        # Il a exploré la case de départ
        self.labyrinthe.cases[(0, 0)].exploree = True
        self.abscissePrecedente = [0]
        self.ordonneePrecedente = [0]

    # @mesureTemps("getCaseVoisine")
    def getCaseVoisines(self) -> [Case.Case]:
        """
        Renvoie une liste des cases voisines (accessible ou non selon l'algo du mineur)
        :return:
        """
        cases = self.labyrinthe.cases
        voisins = []
        if self.abscisse > 0:
            voisins.append(cases[(self.abscisse - 1, self.ordonnee)])
        if self.abscisse < self.labyrinthe.nbLigne - 1:
            voisins.append(cases[self.abscisse + 1, self.ordonnee])
        if self.ordonnee > 0:
            voisins.append(cases[self.abscisse, self.ordonnee - 1])
        if self.ordonnee < self.labyrinthe.nbColonne - 1:
            voisins.append(cases[self.abscisse, self.ordonnee + 1])
        return voisins

    # @mesureTemps("getCasDisponible")
    def getCasesDisponibles(self):
        """
        Renvoie les cases accessible pour l'algo du mineur
        (les cases voisines qui n'ont pas encore été visitées)
        :return:
        """
        logger.debug(f"Cases dispos : {[(case.abscisse, case.ordonnee) for case in self.getCaseVoisines() if not case.exploree]}")
        return [case for case in self.getCaseVoisines() if not case.exploree]
    # @mesureTemps("deplacement Mineur")
    def deplacement(self)->bool:
        """
        Va déplacer le mineur d'une case (si possible)
        :return: True si le mineur a été deplacé, False sinon
        (dans le cas où il est de retour à la case de départ)
        """
        casesDispo = self.getCasesDisponibles()

        # Il y a des cases dispo, en choisi une aléatoire, et y va en cassant le mur
        if casesDispo:
            caseSuivante = random.choice(casesDispo)
            # Case du dessus
            if self.abscisse == caseSuivante.abscisse and self.ordonnee + 1 == caseSuivante.ordonnee:
                self.labyrinthe.cases[self.abscisse, self.ordonnee].supprimerMurHaut()
            # Case du dessous
            if self.abscisse == caseSuivante.abscisse and self.ordonnee - 1 == caseSuivante.ordonnee:
                self.labyrinthe.cases[self.abscisse, self.ordonnee].supprimerMurBas()
            # Case de gauche
            if self.abscisse - 1 == caseSuivante.abscisse and self.ordonnee == self.ordonnee:
                self.labyrinthe.cases[self.abscisse, self.ordonnee].supprimerMurGauche()
            # Case de droite
            if self.abscisse + 1 == caseSuivante.abscisse and self.ordonnee == self.ordonnee:
                self.labyrinthe.cases[self.abscisse, self.ordonnee].supprimerMurDroit()
            # Déplacement
            self.abscissePrecedente.append(self.abscisse)
            self.ordonneePrecedente.append(self.ordonnee)
            self.abscisse = caseSuivante.abscisse
            self.ordonnee = caseSuivante.ordonnee
            caseSuivante.exploree = True
            return True

        # Il n'y a pas de case dispo, demi-tour
        else:
            # Demi tour possible (le mineur n'est pas en 0,0):
            if self.ordonnee or self.abscisse:
                logger.debug(f"coordonées précédentes : {self.abscissePrecedente, self.ordonneePrecedente}")
                self.abscisse = self.abscissePrecedente.pop()
                self.ordonnee = self.ordonneePrecedente.pop()
                logger.debug(f"Coordonnées : {self.abscisse}, {self.ordonnee}")
                return True
            else:
                return False

    @mesureTemps("création du labyrinthe ")
    def creerLabyrinthe(self):
        """
        Fonction de création de labyrinthe, utilise l'algo du "mineur"
        :return:
        """
        continuer = True
        while continuer:
            logger.debug("Nouvelle itération")
            continuer = self.deplacement()
            logger.debug(f"Coordonnées : {self.abscisse}, {self.ordonnee}")
