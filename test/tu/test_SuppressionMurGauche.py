import pytest
import structlog

import GenerateurLabyrinthe.Case as Case
import GenerateurLabyrinthe.Labyrinthe as laby

logger = structlog.getLogger(__name__)


def test_suppressionMurGauche():
    # Test suppression mur valide
    labyrinthe = laby.Labyrinthe(3, 3)
    labyrinthe.cases[(1, 1)].supprimerMurGauche()
    assert not labyrinthe.cases[(1, 1)].murGauche
    assert not labyrinthe.cases[(0, 1)].murDroit
    # Test suppression mur invalide
    with pytest.raises(Exception):
        labyrinthe.cases[(0, 1)].supprimerMurGauche()
