import GenerateurLabyrinthe.Labyrinthe as Labyrinthe
import GenerateurLabyrinthe.Mineur as Mineur


def test_deplacementHaut():
    """
    Vérifie que un déplacement vers le haut est faisable, et que les murs sont correctement détruits
    :return:
    """
    laby = Labyrinthe.Labyrinthe(3, 3)
    mineur = Mineur.Mineur(laby)
    mineur.abscisse, mineur.ordonnee = 1, 1
    laby.cases[(0, 1)].exploree = True
    laby.cases[(2, 1)].exploree = True
    laby.cases[(1, 0)].exploree = True
    mineur.deplacement()
    assert mineur.abscisse == 1
    assert mineur.ordonnee == 2
    assert mineur.abscissePrecedente == 1
    assert mineur.ordonneePrecedente == 1
    assert laby.cases[(1,2)].exploree
    assert not laby.cases[(1,1)].murHaut and not laby.cases[(1,2)].murBas

def test_deplacementBas():
    """
    Vérifie que un déplacement vers le bas est faisable, et que les murs sont correctement détruits
    :return:
    """
    laby = Labyrinthe.Labyrinthe(3, 3)
    mineur = Mineur.Mineur(laby)
    mineur.abscisse, mineur.ordonnee = 1, 1
    laby.cases[(0, 1)].exploree = True
    laby.cases[(2, 1)].exploree = True
    laby.cases[(1, 2)].exploree = True
    mineur.deplacement()
    assert mineur.abscisse == 1
    assert mineur.ordonnee == 0
    assert mineur.abscissePrecedente == 1
    assert mineur.ordonneePrecedente == 1
    assert laby.cases[(1,0)].exploree
    assert not laby.cases[(1,1)].murBas and not laby.cases[(1,0)].murHaut

def test_deplacementGauche():
    """
    Vérifie que un déplacement vers la gauche est faisable, et que les murs sont correctement détruits
    :return:
    """
    laby = Labyrinthe.Labyrinthe(3, 3)
    mineur = Mineur.Mineur(laby)
    mineur.abscisse, mineur.ordonnee = 1, 1
    laby.cases[(1, 2)].exploree = True
    laby.cases[(2, 1)].exploree = True
    laby.cases[(1, 0)].exploree = True
    mineur.deplacement()
    assert mineur.abscisse == 0
    assert mineur.ordonnee == 1
    assert mineur.abscissePrecedente == 1
    assert mineur.ordonneePrecedente == 1
    assert laby.cases[(0,1)].exploree
    assert not laby.cases[(1,1)].murGauche and not laby.cases[(0,1)].murDroit

def test_deplacementDroit():
    """
    Vérifie que un déplacement vers la droite est faisable, et que les murs sont correctement détruits
    :return:
    """
    laby = Labyrinthe.Labyrinthe(3, 3)
    mineur = Mineur.Mineur(laby)
    mineur.abscisse, mineur.ordonnee = 1, 1
    laby.cases[(1, 2)].exploree = True
    laby.cases[(0, 1)].exploree = True
    laby.cases[(1, 0)].exploree = True
    mineur.deplacement()
    assert mineur.abscisse == 2
    assert mineur.ordonnee == 1
    assert mineur.abscissePrecedente == 1
    assert mineur.ordonneePrecedente == 1
    assert laby.cases[(0,1)].exploree
    assert not laby.cases[(1,1)].murDroit and not laby.cases[(2,1)].murGauche
