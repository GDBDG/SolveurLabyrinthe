import Labyrinthe.Labyrinthe as laby
import GenerateurLabyrinthe.Mineur as Mineur

def test_CasesDisponibles():
    """
    Vérifie que les cases déjà explorées ne sont pas considérées comme disponible
    mais que les cases non explorées le sont.
    :return:
    """
    labyrinthe = laby.Labyrinthe(3, 3)
    mineur = Mineur.Mineur(labyrinthe)
    labyrinthe.cases[(1,0)].exploree = True
    assert (mineur.getCasesDisponibles()[0].abscisse, mineur.getCasesDisponibles()[0].ordonnee) == (0,1)