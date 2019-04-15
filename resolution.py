from astar3d import astar3d
from TableReservation import TableReservation, Reservation

def resolution(listeRobotID, listeDeparts, tDepart, listeArrivees, tArrivee, grille):
    table = TableReservation(tDepart, tArrivee-tDepart+1)
    listeChemins = []
    for i in range(len(listeRobotID)):
        depart = listeDeparts[i]
        arrivee = listeArrivees[i]
        robotID = listeRobotID[i]
        chemin = astar3d(depart, tDepart, arrivee, tArrivee, grille, table)
        table.reserverChemin(Reservation(chemin, tDepart, robotID))
        listeChemins.append(chemin)
    return listeChemins
        