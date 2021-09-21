import pytest
import structlog

import GenerateurLabyrinthe.Case as Case
import GenerateurLabyrinthe.Labyrinthe as laby

logger = structlog.getLogger(__name__)


def test_suppressionMurHaut():
    # Test suppression mur valide
    labyrinthe = laby.Labyrinthe(3, 3)
    labyrinthe.cases[(1, 1)].supprimerMurBas()
    assert not labyrinthe.cases[(1, 1)].murBas
    assert not labyrinthe.cases[(1, 0)].murHaut
    # Test suppression mur invalide
    with pytest.raises(Exception):
        labyrinthe.cases[(1, 0)].supprimerMurBas()
