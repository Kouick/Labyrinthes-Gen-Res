import numpy as np
from PIL import Image
import imageio
import pickle


NAMEFILE=input("nom du fichier pickle contenant le graph du jeu a 'labyrinthiser' (avec l'extension)      ")
NAMSAV=input("nom du fichier ou sera sauvegardée l'image du labyrinthe créé      ")


#Le "reformeur" prend en entrée un fichier graphe généré par le script ayant l'effet inverse appliqué sur un labyrinthe sans portail.

def taille(g):
    i,j=0,0
    for c in g:
        if i<c[0]:
            i=c[0]
        if j<c[1]:
            j=c[1]
    return i,j


def GEN(NAMEFILE,NAMSAV,Ie=0,Je=0,Is=None,Js=None):
    file = open(NAMEFILE, "rb")
    g = pickle.load(file)
    file.close()
    Imax,Jmax=taille(g)
    if Is==None:
        Is=Imax
    if Js==None:
        Js=Jmax
    ta=np.full((Imax+1, Jmax+1, 3), [0, 0, 0], dtype=np.uint8)
    for c in g:
        i,j=c
        ta[i][j][0]=255
        ta[i][j][1]=255
        ta[i][j][2]=255
    ta[Ie][Je][0]=255
    ta[Ie][Je][1]=0
    ta[Ie][Je][2]=0
    ta[Is][Js][0]=0
    ta[Is][Js][1]=255
    ta[Is][Js][2]=0
    imageio.imwrite(NAMSAV+".png", ta)



GEN(NAMEFILE,NAMSAV)
