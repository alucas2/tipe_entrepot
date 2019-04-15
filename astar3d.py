from collections import namedtuple
from Vec2d import Vec2d
from FilePriorite import FilePriorite
from heuristique2d import BackwardAstar2d, estAccessible
from math import inf

Noeud = namedtuple("Noeud3d", ["x", "y", "t"])

def voisins3d(n, grille, tableReservation):
    """Itère sur les voisin accessibles du noeud n"""

    (x, y, t) = n
    for voisin in [Noeud(x, y, t+1), 
                   Noeud(x+1, y, t+1), 
                   Noeud(x-1, y, t+1), 
                   Noeud(x, y+1, t+1), 
                   Noeud(x, y-1, t+1)]:
        if estAccessible(voisin.x, voisin.y, grille)\
            and tableReservation.mouvementAutorise(t, x, y, voisin.x, voisin.y):
            yield voisin


def coutMouvement(n1, n2):
    """Renvoie le cout du mouvement du noeud n1 vers le noeud n2"""

    if n1.x == n2.x and n1.y == n2.y:
        return 0
    else:
        return 1


#---------------------------Implémentation de l'algorithme A*---------------------------

def astar3d(depart, tDepart, arrivee, tArrivee, grille, tableReservation, pMax=1000):
    """Renvoie un chemin de (depart.x, depart.y, tDepart) vers la position 
    la plus proche de (arrivee.x, arrivee.y, tArrivee).
    La longueur du chemin renvoyé est tArrivee-tDepart+1"""

    if not estAccessible(arrivee.x, arrivee.y, grille):
        raise Exception("Arrivée inaccessible à cause d'un obstacle statique")

    heuristique = BackwardAstar2d(depart, arrivee, grille)
    noeudDepart = Noeud(depart.x, depart.y, tDepart)
    parents = {noeudDepart: None}
    distances = {noeudDepart: 0}
    frontiere = FilePriorite()
    frontiere.inserer(noeudDepart, heuristique.distanceArrivee(noeudDepart))
    noeudArrivee = None

    while not frontiere.estVide():
        noeudMin = frontiere.popMinimum()
        if noeudMin.x == arrivee.x and noeudMin.y == arrivee.y and noeudMin.t >= tArrivee:
            noeudArrivee = noeudMin
            break
        d = distances[noeudMin]
        for voisin in voisins3d(noeudMin, grille, tableReservation):
            nouveau_d = d + coutMouvement(noeudMin, voisin)
            if distances.get(voisin, inf) > nouveau_d:
                h = heuristique.distanceArrivee(voisin)
                if noeudMin.t <= tArrivee + pMax:
                    frontiere.inserer(voisin, nouveau_d + h)
                distances[voisin] = nouveau_d
                parents[voisin] = noeudMin

    if noeudArrivee is None:
        raise Exception("Arrivée probablement inaccessible")

    chemin = []
    n = noeudArrivee
    while n is not None:
        if n.t <= tArrivee:
            chemin.insert(0, Vec2d(n.x, n.y))
        n = parents[n]

    return chemin
