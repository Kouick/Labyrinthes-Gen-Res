import numpy as np
from PIL import Image
from copy import *
from time import *
import imageio
import pickle


NAMEFILE=input("Nom du fichier pickle contenant le graphe à 'labyrinthiser' (avec l'extension) : ")
NAMSAV=input("Nom du fichier où sera sauvegardée l'image du labyrinthe créé : ")
NAMSAVTXT=input("Nom du fichier où sera enregistré le dictionnaire des portails : ")




def taille(gres):
    t=0
    for c in g:
        if t<max(len(gres[c][0]),len(gres[c][1])):
            t=max(len(gres[c][0]),len(gres[c][1]))
    return t

def entsortdic(g,INIT):   # Le format est {sommets: (liste des sommets desquels on peut arriver, liste des sommets vers lesquels on peut aller)}.
    gres={}
    nxt=g[INIT]
    cur=[]
    for c in g:
        gres[c]=([],[])
    for c in g:
        tmp=g[c]
        for i in tmp:
            gres[i][0].append(c)
        gres[c]=gres[c][0],deepcopy(tmp)
        nxt=nxt+tmp
    return gres


def motif(entsort):
    mot=np.full((6, 4, 3), [0, 0, 0], dtype=np.uint8)
    mot[5][2]=[254,254,254]
    return mot



def dicoord(dictidsom, g):
    dicaret={}
    for som in g:
        dicaret[(5,4*dictidsom[som]+2)]=[]
    for som in g:
        adj=g[som]
        for ar in adj:
            dicaret[(5,4*dictidsom[som]+2)].append((5,4*dictidsom[ar]+2))
    return dicaret



def GEN(g,NAMSAV,NAMSAVTXT):
    INIT=next(iter(g))
    gres=entsortdic(g,INIT)
    Imax=taille(gres)+10
    Jmax=len(g)*4
    tab=np.full((Imax, Jmax, 3), [0, 0, 0], dtype=np.uint8)
    n=0
    dictidsom={}
    id=0
    for c in gres:
        dictidsom[c]=id
        id+=1
        mot=motif(gres[c])
        for i in range(len(mot)):
            for j in range(len(mot[0])):
                tab[i][j+n*4]=mot[i][j]
        n+=1
    coord=dicoord(dictidsom,g)
    imageio.imwrite(NAMSAV+".png", tab)
    tf = open(NAMSAVTXT, "wb")
    pickle.dump(coord,tf)
    tf.close()


file = open(NAMEFILE, "rb")
g = pickle.load(file)
file.close()
GEN(g,NAMSAV,NAMSAVTXT)


