from collections import namedtuple

class Reservation:
    def __init__(self, chemin, tDepart, robotID):
        assert(robotID != 0)
        self.chemin = chemin
        self.tDepart = tDepart
        self.robotID = robotID


PositionKey = namedtuple("PositionKey", ["x", "y"])

class TableReservation:
    def __init__(self, t0, profondeur):
        self.t = t0
        self.profondeur = profondeur
        self.table = [{} for t in range(profondeur)]


    def getReservation(self, t, x, y):
        """Renvoie l'id du robot qui a réservé la position (x, y, t).
        Renvoie 0 si la position est libre.
        Renvoie 0 si t tombe en dehors des limites de la table (agit comme si la position était libre)"""
        
        if self._estHorsLimites(t): return 0
        d = t - self.t
        return self.table[d].get(PositionKey(x, y), 0)


    def mouvementAutorise(self, t, x1, y1, x2, y2):
        """Renvoie True si le mouvement de (x1, y1, t) vers (x2, y2 t+1) est autorisé"""
        
        arrivee_avant = self.getReservation(t, x2, y2)
        depart_apres = self.getReservation(t+1, x1, y1)
        arrivee_apres = self.getReservation(t+1, x2, y2)
        if arrivee_apres != 0:# case de destination occupée
            return False
        if arrivee_avant != 0 and arrivee_avant == depart_apres:# échange de position impossible
            return False
        return True


    def reserverChemin(self, reservation):
        """Réserve un chemin dans la table"""
        
        t = reservation.tDepart
        for p in reservation.chemin:
            self._reserverCase(t, p.x, p.y, reservation.robotID)
            t += 1


    def _reserverCase(self, t, x, y, robotID):
        if self._estHorsLimites(t): return
        d = t - self.t
        self.table[d][PositionKey(x, y)] = robotID


    def _estHorsLimites(self, t):
        return t < self.t or t >= self.t + self.profondeur