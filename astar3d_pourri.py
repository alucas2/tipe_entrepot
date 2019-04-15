from collections import namedtuple
from Vec2d import Vec2d
from FilePriorite import FilePriorite
from heuristique2d import distanceManhattan, estAccessible
from astar3d import Noeud, voisins3d, coutMouvement
from math import inf

#---------------------------Implémentation de l'algorithme A* avec heuristique pourrie---------------------------

import numpy as np
ResultatAstar3d_debug = namedtuple("ResultatAstar3d_debug", ["chemin", "volumeExplore", "surfaceExplore", "voxels"])

def astar3d_pourri_debug(depart, tDepart, arrivee, tArrivee, grille, tableReservation, pMax=1000):
    """Comme la fonction astar3d, mais renvoie en plus quelques informations"""

    if not estAccessible(arrivee.x, arrivee.y, grille):
        raise Exception("Arrivée inaccessible à cause d'un obstacle statique")

    noeudDepart = Noeud(depart.x, depart.y, tDepart)
    parents = {noeudDepart: None}
    distances = {noeudDepart: 0}
    frontiere = FilePriorite()
    frontiere.inserer(noeudDepart, distanceManhattan(noeudDepart, arrivee))
    noeudArrivee = None

    c = 0
    voxel = np.full((grille.shape[0], grille.shape[1], tArrivee-tDepart+1), False, dtype=bool)

    while not frontiere.estVide():
        c += 1
        noeudMin = frontiere.popMinimum()
        if noeudMin.t <= tArrivee:
            voxel[noeudMin.x, noeudMin.y, noeudMin.t - tDepart] = True
        if noeudMin.x == arrivee.x and noeudMin.y == arrivee.y and noeudMin.t >= tArrivee:
            noeudArrivee = noeudMin
            break
        d = distances[noeudMin]
        for voisin in voisins3d(noeudMin, grille, tableReservation):
            nouveau_d = d + coutMouvement(noeudMin, voisin)
            if distances.get(voisin, inf) > nouveau_d:
                h = distanceManhattan(voisin, arrivee)
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

    return ResultatAstar3d_debug(chemin, c, -1, voxel)
