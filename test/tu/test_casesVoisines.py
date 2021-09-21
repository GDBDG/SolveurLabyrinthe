import Labyrinthe.Labyrinthe as laby
import GenerateurLabyrinthe.Mineur as Mineur


def test_caseVoisine():
    """
    Vérifie la fonction qui récupère la liste des cases voisines du mineur

    :return:
    """
    # Cas entrée (couvre cas première ligne et colonne)
    labyrinthe = laby.Labyrinthe(3, 3)
    mineur = Mineur.Mineur(labyrinthe)
    assert set([(case.abscisse, case.ordonnee) for case in mineur.getCaseVoisines()]) == set([(0, 1), (1, 0)])

    # Cas sortie (couvre cas dernière ligne et dernière colonne)
    mineur.abscisse = labyrinthe.nbLigne - 1
    mineur.ordonnee = labyrinthe.nbColonne - 1
    assert set([(case.abscisse, case.ordonnee) for case in mineur.getCaseVoisines()]) == set([(labyrinthe.nbLigne - 1 -1, labyrinthe.nbColonne - 1), (labyrinthe.nbLigne - 1, labyrinthe.nbColonne - 1 -1)])

    # Cas quelconque : vérifier les 4 voisins
    mineur.abscisse = 1
    mineur.ordonnee = 1
    assert set([(case.abscisse, case.ordonnee) for case in mineur.getCaseVoisines()]) == set([(0,1),(2,1),(1,0),(1,2)])
