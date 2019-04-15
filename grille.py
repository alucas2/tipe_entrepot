import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def chargerGrilles(fichier):
    strArray = np.genfromtxt(fichier, dtype=str)
    grilleNormal = np.full((strArray.shape[1], strArray.shape[0]), False, dtype=bool)
    grilleEtageres = np.full((strArray.shape[1], strArray.shape[0]), False, dtype=bool)
    for x in range(grilleNormal.shape[0]):
        for y in range(grilleNormal.shape[1]):
            if strArray[y, x] == 'o':# 'o' pour un mur
                grilleNormal[x, y] = True
                grilleEtageres[x, y] = True
            elif strArray[y, x] == '=': # '=' pour une étagère
                grilleEtageres[x, y] = True

    return (grilleNormal, grilleEtageres)


def plotGrilles(ax, grilleNormal, grilleEtageres):
    xc = np.arange(0, grilleNormal.shape[0]+1)
    yc = np.arange(0, grilleNormal.shape[1]+1)
    x, y = np.meshgrid(xc, yc, indexing="ij")
    colors = np.empty(grilleNormal.shape, dtype=str)
    for ix in range(grilleNormal.shape[0]):
        for iy in range(grilleNormal.shape[1]):
            if grilleNormal[ix, iy]:
                colors[ix, iy] = 'b'
            elif grilleEtageres[ix, iy]:
                colors[ix, iy] = 'y'
            else:
                colors[ix, iy] = 'w'
    ax.plot_surface(x-0.5, y-0.5, np.zeros(x.shape), facecolors=colors, linewidth=0)


def randomCase(grille):
    while True:
        x = np.random.randint(0, grille.shape[0])
        y = np.random.randint(0, grille.shape[1])
        if not grille[x, y]:
            return (x, y)