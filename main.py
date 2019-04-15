from resolution import resolution
from grille import chargerGrilles, plotGrilles, randomCase
from Vec2d import Vec2d
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


grilleNormal, grilleEtageres = chargerGrilles("maps/map_32x32.txt")
nRobots = 10
listeRobotID = [i for i in range(1, nRobots+1)]
listeDeparts = [Vec2d(randomCase(grilleNormal)) for i in range(1, nRobots+1)]
listeArrivees = [Vec2d(randomCase(grilleNormal)) for i in range(1, nRobots+1)]
tDepart = 0
tArrivee = 64
listeChemins = resolution(listeRobotID, listeDeparts, tDepart, listeArrivees, tArrivee, grilleNormal)

fig = plt.figure()
ax = fig.gca(projection="3d")
ax.set_aspect("equal")
t = np.arange(tDepart, tArrivee+1)
for i in range(len(listeChemins)):
    c = np.array(listeChemins[i])
    ax.plot(c[:, 0], c[:, 1], t, marker='.', label=str(listeRobotID[i]))

l = max(grilleNormal.shape)
ax.set_xlim(0, l)
ax.set_ylim(0, l)
ax.set_zlim(0, max(l, tArrivee-tDepart))
plotGrilles(ax, grilleNormal, grilleEtageres)
plt.legend()
plt.show()