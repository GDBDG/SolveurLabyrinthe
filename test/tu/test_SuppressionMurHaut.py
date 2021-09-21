import pytest
import structlog

import GenerateurLabyrinthe.Case as Case
import GenerateurLabyrinthe.Labyrinthe as laby

logger = structlog.getLogger(__name__)


def test_suppressionMurHaut():
    # Test suppression mur valide
    labyrinthe = laby.Labyrinthe(3, 3)
    labyrinthe.cases[(1, 1)].supprimerMurHaut()
    assert not labyrinthe.cases[(1, 1)].murHaut
    assert not labyrinthe.cases[(1, 2)].murBas
    # Test suppression mur invalide
    with pytest.raises(Exception):
        labyrinthe.cases[(1, 2)].supprimerMurHaut()
