from collections import namedtuple
from FilePriorite import FilePriorite
import numpy as np

Noeud2d = namedtuple("Noeud2d", ["x", "y"])

def estAccessible(x, y, grille):
    """Renvoie False si un obstacle statique est présent en (x, y)"""

    return x >= 0 and y >= 0\
        and x < grille.shape[0] and y < grille.shape[1]\
        and not grille[x, y]


def voisins2d(n, grille):
    """Itère sur les voisin accessibles du noeud n"""

    (x, y) = n
    for voisin in [Noeud2d(x+1, y), Noeud2d(x-1, y), Noeud2d(x, y+1), Noeud2d(x, y-1)]:
        if estAccessible(voisin.x, voisin.y, grille):
            yield voisin


def distanceManhattan(n1, n2):
    return abs(n1.x - n2.x) + abs(n1.y - n2.y)


class BackwardAstar2d():
    def __init__(self, depart, arrivee, grille):
        self.depart = depart
        self.arrivee = arrivee
        self.grille = grille
        noeudArrivee = Noeud2d(arrivee.x, arrivee.y)
        self.distances = {noeudArrivee: 0}
        self.fermes = set()
        self.frontiere = FilePriorite()
        self.frontiere.inserer(noeudArrivee, distanceManhattan(noeudArrivee, depart))
        self.c = 0


    def distanceArrivee(self, cible):
        """Renvoie la distance entre (cible.x, cible.y) et l'arrivée"""

        noeudCible = Noeud2d(cible.x, cible.y)
        if noeudCible in self.fermes:
            return self.distances[noeudCible]

        while not self.frontiere.estVide():
            self.c += 1
            noeudMin = self.frontiere.popMinimum()
            d = self.distances[noeudMin]
            self.fermes.add(noeudMin)
            for voisin in voisins2d(noeudMin, self.grille):
                if voisin not in self.distances or self.distances[voisin] > d + 1:
                    self.frontiere.inserer(voisin, d + 1 + distanceManhattan(voisin, self.depart))
                    self.distances[voisin] = d + 1
            if noeudMin == noeudCible:
                return d

        raise Exception("Cible inaccessible")


    def matrice(self):
        resultat = np.zeros(self.grille.shape)
        for (n, d) in self.distances.items():
            resultat[n.x, n.y] = d
        return resultat

