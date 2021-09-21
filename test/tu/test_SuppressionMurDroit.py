import pytest
import structlog

import GenerateurLabyrinthe.Case as Case
import GenerateurLabyrinthe.Labyrinthe as laby

logger = structlog.getLogger(__name__)


def test_suppressionMurHaut():
    # Test suppression mur valide
    labyrinthe = laby.Labyrinthe(3, 3)
    labyrinthe.cases[(1, 1)].supprimerMurDroit()
    assert not labyrinthe.cases[(1, 1)].murDroit
    assert not labyrinthe.cases[(2, 1)].murGauche
    # Test suppression mur invalide
    with pytest.raises(Exception):
        labyrinthe.cases[(2, 1)].supprimerMurDroit()
