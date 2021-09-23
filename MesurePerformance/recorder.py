import time
import structlog
logger = structlog.getLogger(__name__)
listeTemps = {}


def mesureTemps(nom: str):
    """
    Décorateur qui va ajouter le temps passé par la fonction décorée dans listTemps,
    avec pour clé la variable  nom
    :param nom: Valeur de la clé (mettre un nom décrivant la fonction)
    """

    def decorator(func):
        def decorated(*args, **kwargs):
            t0 = time.time()
            res = func(*args, **kwargs)
            t1 = time.time()
            if nom in listeTemps.keys():
                listeTemps[nom] = 0
            listeTemps[nom] = t1 - t0
            return res

        return decorated

    return decorator


def getTempsTotal():
    """
    Renvoie la somme des temps dans listTemps
    """
    return sum(listeTemps)



